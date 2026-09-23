import csv, os, glob
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
import chromadb

EMBED_MODEL = "nomic-embed-text"
morceaux = []

splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=150)

for chemin in glob.glob("data/sources/*.pdf"):
    nom = os.path.basename(chemin)
    reader = PdfReader(chemin)
    print("Lecture de", nom, "-", len(reader.pages), "pages")
    for i, page in enumerate(reader.pages, start=1):
        texte = (page.extract_text() or "").strip()
        if len(texte) < 100:
            continue
        for bout in splitter.split_text(texte):
            morceaux.append((bout, {"source": nom, "page": i, "type": "guide"}))

if os.path.exists("data/annexe_a.csv"):
    with open("data/annexe_a.csv", encoding="utf-8-sig", newline="") as f:
        for ligne in csv.DictReader(f, delimiter=";"):
            texte = ("Controle ISO 27001 " + ligne["id"] + " (" + ligne["theme"] + ") - "
                     + ligne["titre"] + " : " + ligne["description"]
                     + ". Mots cles : " + ligne["mots_cles"])
            morceaux.append((texte, {"source": "ISO 27001 Annexe A",
                                     "controle": ligne["id"], "type": "controle"}))

print("Morceaux a indexer :", len(morceaux))
if not morceaux:
    raise SystemExit("Aucun document trouve. Verifiez data/sources et data/annexe_a.csv")

embeddings = OllamaEmbeddings(model=EMBED_MODEL)
client = chromadb.PersistentClient(path="chroma_db")
try:
    client.delete_collection("grc")
except Exception:
    pass
collection = client.create_collection("grc")

lot = 50
for debut in range(0, len(morceaux), lot):
    paquet = morceaux[debut:debut + lot]
    textes = [t for t, _ in paquet]
    metas = [m for _, m in paquet]
    vecteurs = embeddings.embed_documents(textes)
    ids = ["doc-" + str(debut + k) for k in range(len(paquet))]
    collection.add(ids=ids, documents=textes, embeddings=vecteurs, metadatas=metas)
    print("Indexes :", debut + len(paquet), "/", len(morceaux))

print("Termine. Total dans la base :", collection.count())
