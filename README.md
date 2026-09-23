# Copilote GRC - assistant IA pour EBIOS RM et ISO/IEC 27001

Prototype d assistant d analyse de risques et de conformite, construit autour d un modele
de langage execute en local. Aucune donnee d analyse ne quitte le poste de travail.

Projet personnel realise dans le cadre d un Master 2 Management de la Cybersecurite (ECE Paris).

## Ce que fait l outil

1. Questions-reponses sourcees sur le guide EBIOS RM de l ANSSI et un referentiel de
   controles ISO/IEC 27001 Annexe A, avec citation des pages.
2. Mapping automatique d une mesure de securite vers les controles de l Annexe A,
   avec score de similarite semantique et verdict par controle.
3. Tableau de bord : taux de couverture, score de maturite pondere, controles non couverts.
4. Rapport de conformite genere en Markdown, entierement calcule par le code.

## Architecture

| Brique | Technologie | Role |
|---|---|---|
| Modele de langage | Ollama + llama3.2:3b | Analyse qualitative |
| Embeddings | nomic-embed-text (768 dimensions) | Recherche semantique |
| Base vectorielle | ChromaDB locale | 157 fragments indexes |
| Orchestration | LangChain | Chargement des modeles |
| Interface | Streamlit | Application web locale |

## Principes de conception

Le modele de langage ne decide pas et ne calcule pas.

- Les indicateurs chiffres sont produits exclusivement par le code Python.
- Dans le mapping, le modele emet un avis par controle ; la liste finale est compilee par le code.
- Un seuil de similarite de 0,55 ecarte les controles hors sujet avant analyse.
- Toute question hors du perimetre documentaire declenche un refus explicite.
- Chaque sortie porte la mention "a valider par un analyste".

## Limites identifiees

- Generation de synthese retiree. Le modele reinterpretait les indicateurs : identifiants
  de controles transformes en pourcentages, score pondere presente comme un decompte.
  Apres trois tentatives de correction, la fonctionnalite a ete supprimee. Un rapport de
  conformite contenant une phrase fausse est plus dangereux qu un rapport sans synthese.
- Citations approximatives : le modele cite parfois une seule source alors qu il en utilise
  plusieurs. Les sources reellement consultees sont donc affichees separement.
- Format de sortie non garanti avec un modele de 3 milliards de parametres.
- Referentiel partiel : 15 controles sur 93, en reformulation personnelle.

## Propriete intellectuelle

La norme ISO/IEC 27001 est payante et protegee. Aucun extrait ne figure dans ce depot :
data/annexe_a.csv contient uniquement les references des controles et des reformulations
personnelles. Le guide EBIOS RM de l ANSSI n est pas versionne et doit etre telecharge
separement depuis cyber.gouv.fr.

## Installation

Prerequis : Python 3.11 ou superieur et Ollama (ollama.com).

    ollama pull llama3.2:3b
    ollama pull nomic-embed-text
    python -m venv .venv
    .venv\Scripts\activate
    pip install langchain langchain-community langchain-ollama chromadb pypdf streamlit
    python src/indexer.py
    streamlit run src/app.py

## Utilisation en ligne de commande

    python src/chat_grc.py "A quoi sert l atelier 1 de la methode EBIOS RM ?"
    python src/mapping_iso.py "Revoir trimestriellement les droits d acces sur Active Directory"
    python src/rapport.py

## Structure

    data/annexe_a.csv    Referentiel de controles
    data/mesures.csv     Plan d action du perimetre de test
    src/indexer.py       Indexation et vectorisation
    src/chat_grc.py      Moteur de questions-reponses sourcees
    src/mapping_iso.py   Mapping mesure vers controles ISO
    src/rapport.py       Generation du rapport de conformite
    src/app.py           Interface Streamlit

## Pistes d evolution

- Elargir le referentiel aux 93 controles de l Annexe A.
- Assister la conduite des ateliers EBIOS RM pas a pas.
- Evaluer la qualite des reponses sur un jeu de questions de reference.
