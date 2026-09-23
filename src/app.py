import csv
import chromadb
import streamlit as st
from langchain_ollama import ChatOllama, OllamaEmbeddings

LLM_MODEL = "llama3.2:3b"
EMBED_MODEL = "nomic-embed-text"
SEUIL = 0.55

st.set_page_config(page_title="Copilote GRC", layout="wide")

@st.cache_resource
def charger():
    emb = OllamaEmbeddings(model=EMBED_MODEL)
    client = chromadb.PersistentClient(path="chroma_db")
    col = client.get_collection("grc")
    llm = ChatOllama(model=LLM_MODEL, temperature=0)
    return emb, col, llm

@st.cache_data
def lire(chemin):
    with open(chemin, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))

def cos(a, b):
    ps = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    return ps / (na * nb) if na and nb else 0.0

embeddings, collection, llm = charger()

st.title("Copilote GRC")
st.caption("Assistant EBIOS RM et ISO/IEC 27001. Modele execute en local : aucune donnee ne quitte le poste. "
           "Propositions automatiques, a valider par un analyste.")

t1, t2, t3 = st.tabs(["Questions sur le referentiel", "Mapping ISO 27001", "Tableau de bord"])

with t1:
    question = st.text_input("Votre question", placeholder="Que fait-on dans l atelier 3 d EBIOS RM ?")
    if st.button("Interroger", type="primary") and question:
        with st.spinner("Recherche dans les documents indexes..."):
            v = embeddings.embed_query(question)
            res = collection.query(query_embeddings=[v], n_results=5)
            docs, metas = res["documents"][0], res["metadatas"][0]
            blocs = []
            for n, (d, m) in enumerate(zip(docs, metas), start=1):
                if m.get("type") == "controle":
                    ref = "ISO 27001 controle " + str(m.get("controle"))
                else:
                    ref = str(m.get("source")) + ", page " + str(m.get("page"))
                blocs.append("[Source " + str(n) + "] (" + ref + ")" + chr(10) + d)
            gabarit = ("Reponds UNIQUEMENT a partir des extraits. Si absent, dis : "
                       "Je ne trouve pas cette information dans les documents indexes. "
                       "Cite les sources [Source N]. Reponds en francais." + chr(10) + chr(10)
                       + "EXTRAITS :" + chr(10) + (chr(10) + chr(10)).join(blocs) + chr(10) + chr(10)
                       + "QUESTION : " + question + chr(10) + chr(10) + "REPONSE :")
            st.markdown(llm.invoke(gabarit).content)
            with st.expander("Sources consultees"):
                for n, m in enumerate(metas, start=1):
                    if m.get("type") == "controle":
                        st.write(n, "- ISO 27001 controle", m.get("controle"))
                    else:
                        st.write(n, "-", m.get("source"), "page", m.get("page"))

with t2:
    controles = lire("data/annexe_a.csv")
    mesure = st.text_area("Decrivez une mesure de securite", height=100,
                          placeholder="Revoir tous les trimestres les droits d acces sur Active Directory")
    if st.button("Rechercher les controles", type="primary") and mesure:
        with st.spinner("Analyse controle par controle..."):
            textes = [c["titre"] + " : " + c["description"] + ". " + c["mots_cles"] for c in controles]
            vecs = embeddings.embed_documents(textes)
            v = embeddings.embed_query(mesure)
            tops = sorted([(cos(v, w), c) for w, c in zip(vecs, controles)],
                          key=lambda x: x[0], reverse=True)[:4]
            tops = [(s, c) for s, c in tops if s >= SEUIL]
            if not tops:
                st.warning("Aucun controle ne depasse le seuil de similarite. Mesure hors perimetre du referentiel.")
            retenus = []
            for score, c in tops:
                rep = llm.invoke("Mesure : " + mesure + chr(10) + "Controle " + c["id"] + " - "
                                 + c["titre"] + " : " + c["description"] + chr(10)
                                 + "La mesure satisfait-elle ce controle ? Commence par OUI ou NON, "
                                 + "puis une phrase de justification en francais.").content
                oui = rep.strip().upper().startswith("OUI")
                c1, c2 = st.columns([1, 6])
                c1.metric(c["id"], round(score, 2))
                if oui:
                    c2.success(rep)
                    retenus.append(c["id"])
                else:
                    c2.info(rep)
            if retenus:
                st.markdown("**Controles retenus (decision calculee par le code) : " + ", ".join(retenus) + "**")

with t3:
    controles = lire("data/annexe_a.csv")
    mesures = lire("data/mesures.csv")
    poids = {"Applique": 1.0, "En cours": 0.5, "Non demarre": 0.0}
    couverts = {}
    for m in mesures:
        for cid in [x.strip() for x in m["controles"].split(",") if x.strip()]:
            couverts.setdefault(cid, []).append(m)
    scores = [max([poids.get(m["statut"], 0) for m in couverts.get(c["id"], [])], default=0.0)
              for c in controles]
    a, b, d = st.columns(3)
    a.metric("Controles couverts", str(len(couverts)) + " / " + str(len(controles)))
    b.metric("Taux de couverture", str(round(100 * len(couverts) / len(controles), 1)) + " %")
    d.metric("Maturite ponderee", str(round(100 * sum(scores) / len(scores), 1)) + " / 100")
    st.caption("Indicateurs calcules par le code, sans intervention du modele de langage.")
    st.subheader("Plan d action")
    st.dataframe(mesures, use_container_width=True)
    st.subheader("Controles sans mesure associee")
    st.write(", ".join(c["id"] + " " + c["titre"] for c in controles if c["id"] not in couverts) or "Aucun")
