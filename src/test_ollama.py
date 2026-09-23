from langchain_ollama import ChatOllama, OllamaEmbeddings

LLM_MODEL = "llama3.2:3b"
EMBED_MODEL = "nomic-embed-text"

llm = ChatOllama(model=LLM_MODEL, temperature=0)
reponse = llm.invoke("En deux phrases, a quoi sert l atelier 1 de la methode EBIOS RM ?")
print("--- Reponse du modele ---")
print(reponse.content)

embeddings = OllamaEmbeddings(model=EMBED_MODEL)
vecteur = embeddings.embed_query("controle d acces et moindre privilege")
print("--- Embeddings ---")
print("Dimension du vecteur :", len(vecteur))
