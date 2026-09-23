import csv, re, sys
from langchain_ollama import ChatOllama, OllamaEmbeddings

LLM_MODEL = "llama3.2:3b"
EMBED_MODEL = "nomic-embed-text"
SEUIL = 0.55

def cosinus(a, b):
    ps = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    return ps / (na * nb) if na and nb else 0.0

controles = []
with open("data/annexe_a.csv", encoding="utf-8-sig", newline="") as f:
    for ligne in csv.DictReader(f, delimiter=";"):
        controles.append(ligne)

embeddings = OllamaEmbeddings(model=EMBED_MODEL)
textes = [c["titre"] + " : " + c["description"] + ". " + c["mots_cles"] for c in controles]
vecteurs = embeddings.embed_documents(textes)
llm = ChatOllama(model=LLM_MODEL, temperature=0)

GABARIT = """Tu es auditeur en conformite ISO/IEC 27001.
Mesure de securite evaluee : "{mesure}"

Controle candidat : {ident} - {titre} : {description}

La mesure contribue-t-elle directement a satisfaire ce controle ?
Repond sur DEUX lignes exactement, sans introduction :
VERDICT : OUI ou NON
JUSTIFICATION : une seule phrase en francais."""

def mapper(mesure, top=4):
    v = embeddings.embed_query(mesure)
    scores = sorted(
        [(cosinus(v, vec), c) for vec, c in zip(vecteurs, controles)],
        key=lambda x: x[0], reverse=True
    )[:top]
    scores = [(s, c) for s, c in scores if s >= SEUIL]

    if not scores:
        print("\nAucun controle ne depasse le seuil de", SEUIL, "- mesure hors perimetre du referentiel.")
        return

    print("\n===== ANALYSE CONTROLE PAR CONTROLE =====")
    retenus = []
    for score, c in scores:
        rep = llm.invoke(GABARIT.format(mesure=mesure, ident=c["id"],
                                        titre=c["titre"], description=c["description"]))
        texte = rep.content
        verdict = "OUI" if re.search(r"VERDICT\s*:\s*OUI", texte, re.I) else "NON"
        just = ""
        m = re.search(r"JUSTIFICATION\s*:\s*(.+)", texte, re.I)
        if m:
            just = m.group(1).strip()
        marque = "[X]" if verdict == "OUI" else "[ ]"
        print(marque, c["id"].ljust(6), "sim=" + str(round(score, 3)), "-", c["titre"])
        print("     ", just)
        if verdict == "OUI":
            retenus.append(c["id"])

    print("\n===== CONTROLES RETENUS (calcul par le code) =====")
    print(", ".join(retenus) if retenus else "aucun")
    print("\nRappel : proposition automatique, a valider par un analyste.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        mapper(" ".join(sys.argv[1:]))
    else:
        print("Mapping de mesures vers ISO 27001. 'quitter' pour sortir.")
        while True:
            m = input("\nMesure > ").strip()
            if m.lower() in ("quitter", "exit", "q", ""):
                break
            mapper(m)
