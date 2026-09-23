import re
chemin = "src/rapport.py"
code = open(chemin, encoding="utf-8").read()

ancien_resume = code[code.index('resume_chiffres = ('):code.index('llm = ChatOllama')]
nouveau_resume = '''resume_chiffres = (
    "Deux tiers environ des controles du referentiel disposent d une mesure, "
    "mais le niveau de mise en oeuvre reel reste faible : "
    + str(round(maturite)) + " sur 100. "
    "Trois mesures sur huit ne sont pas demarrees. "
    "Les domaines sans aucune mesure associee sont : "
    + ", ".join(c["titre"] for c in non_couverts) + "."
)

'''
code = code.replace(ancien_resume, nouveau_resume)

ancien_prompt = code[code.index('prompt = ('):code.index('synthese = llm.invoke')]
nouveau_prompt = '''prompt = (
    "Tu es RSSI. Redige une synthese de 4 phrases maximum pour un comite de direction, "
    "en francais, a partir du constat ci-dessous. "
    "REGLES STRICTES : n invente aucun chiffre, ne cite aucun pourcentage, "
    "n utilise aucun identifiant de controle. Reformule uniquement le constat. "
    "Termine par les deux priorites a traiter en premier.\\n\\nCONSTAT :\\n" + resume_chiffres
)

'''
code = code.replace(ancien_prompt, nouveau_prompt)
open(chemin, "w", encoding="utf-8").write(code)
print("rapport.py corrige")
