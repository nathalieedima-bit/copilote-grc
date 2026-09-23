import sys
import chromadb
from langchain_ollama import ChatOllama, OllamaEmbeddings

LLM_MODEL = "llama3.2:3b"
EMBED_MODEL = "nomic-embed-text"
K = 5

embeddings = OllamaEmbeddings(model=EMBED_MODEL)
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection("grc")
llm = ChatOllama(model=LLM_MODEL, temperature=0)

GABARIT = """Tu es un assistant specialise en gestion des risques et en conformite.
Reponds UNIQUEMENT a partir des extraits ci-dessous.
Si les extraits ne contiennent pas la reponse, dis exactement :
"Je ne trouve pas cette information dans les documents indexes."
Cite tes sources sous la forme [Source N] dans le corps de la reponse.
Reponds en francais, de maniere structuree et concise.

EXTRAITS :
{contexte}

QUESTION : {question}

REPONSE :"""

def repondre(question):
    vecteur = embeddings.embed_query(question)
    res = collection.query(query_embeddings=[vecteur], n_results=K)
    docs = res["documents"][0]
    metas = res["metadatas"][0]

    blocs = []
    for n, (doc, meta) in enumerate(zip(docs, metas), start=1):
        if meta.get("type") == "controle":
            ref = "ISO 27001 Annexe A - controle " + str(meta.get("controle"))
        else:
            ref = str(meta.get("source")) + ", page " + str(meta.get("page"))
        blocs.append("[Source " + str(n) + "] (" + ref + ")\n" + doc)

    contexte = "\n\n".join(blocs)
    reponse = llm.invoke(GABARIT.format(contexte=contexte, question=question))

    print("\n===== REPONSE =====")
    print(reponse.content)
    print("\n===== SOURCES CONSULTEES =====")
    for n, meta in enumerate(metas, start=1):
        if meta.get("type") == "controle":
            print("[" + str(n) + "] ISO 27001 Annexe A - controle", meta.get("controle"))
        else:
            print("[" + str(n) + "]", meta.get("source"), "- page", meta.get("page"))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        repondre(" ".join(sys.argv[1:]))
    else:
        print("Copilote GRC. Tapez votre question, ou 'quitter' pour sortir.")
        while True:
            q = input("\nQuestion > ").strip()
            if q.lower() in ("quitter", "exit", "q", ""):
                break
            repondre(q)
