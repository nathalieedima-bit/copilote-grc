import csv, datetime

LLM_MODEL = "llama3.2:3b"
POIDS = {"Applique": 1.0, "En cours": 0.5, "Non demarre": 0.0}

def lire(chemin):
    with open(chemin, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))

controles = lire("data/annexe_a.csv")
mesures = lire("data/mesures.csv")

couverts = {}
for m in mesures:
    for cid in [c.strip() for c in m["controles"].split(",") if c.strip()]:
        couverts.setdefault(cid, []).append(m)

total_ctrl = len(controles)
nb_couverts = len([c for c in controles if c["id"] in couverts])
taux_couverture = 100.0 * nb_couverts / total_ctrl if total_ctrl else 0

scores = []
for c in controles:
    liees = couverts.get(c["id"], [])
    if not liees:
        scores.append(0.0)
    else:
        scores.append(max(POIDS.get(m["statut"], 0.0) for m in liees))
maturite = 100.0 * sum(scores) / len(scores) if scores else 0

par_statut = {}
for m in mesures:
    par_statut[m["statut"]] = par_statut.get(m["statut"], 0) + 1

par_theme = {}
for c, s in zip(controles, scores):
    t = c["theme"]
    par_theme.setdefault(t, []).append(s)

non_couverts = [c for c in controles if c["id"] not in couverts]

lignes = []
lignes.append("# Rapport de conformite ISO/IEC 27001 - perimetre de test")
lignes.append("")
lignes.append("Genere le " + datetime.date.today().isoformat()
              + " par le copilote GRC. Document de travail, a valider par un analyste.")
lignes.append("")
lignes.append("## Indicateurs de pilotage")
lignes.append("")
lignes.append("| Indicateur | Valeur |")
lignes.append("|---|---|")
lignes.append("| Controles du referentiel | " + str(total_ctrl) + " |")
lignes.append("| Controles couverts par au moins une mesure | " + str(nb_couverts) + " |")
lignes.append("| Taux de couverture | " + str(round(taux_couverture, 1)) + " % |")
lignes.append("| Score de maturite pondere | " + str(round(maturite, 1)) + " / 100 |")
lignes.append("| Mesures au plan d action | " + str(len(mesures)) + " |")
for s, n in sorted(par_statut.items()):
    lignes.append("| Mesures - " + s + " | " + str(n) + " |")
lignes.append("")
lignes.append("## Maturite par thematique")
lignes.append("")
lignes.append("| Thematique | Score moyen | Controles |")
lignes.append("|---|---|---|")
for t, vals in sorted(par_theme.items()):
    moy = 100.0 * sum(vals) / len(vals)
    lignes.append("| " + t + " | " + str(round(moy, 1)) + " | " + str(len(vals)) + " |")
lignes.append("")
lignes.append("## Controles sans mesure associee")
lignes.append("")
if non_couverts:
    for c in non_couverts:
        lignes.append("- **" + c["id"] + "** " + c["titre"] + " (" + c["theme"] + ")")
else:
    lignes.append("Aucun.")
lignes.append("")
lignes.append("## Plan d action")
lignes.append("")
lignes.append("| Mesure | Statut | Controles | Responsable | Echeance |")
lignes.append("|---|---|---|---|---|")
for m in mesures:
    lignes.append("| " + m["mesure"] + " | " + m["statut"] + " | " + m["controles"]
                  + " | " + m["responsable"] + " | " + m["echeance"] + " |")

non_demarrees = [m for m in mesures if m["statut"] == "Non demarre"]
if maturite < 40:
    niveau = "faible"
elif maturite < 70:
    niveau = "partiel"
else:
    niveau = "satisfaisant"

lignes.append("")
lignes.append("## Constat")
lignes.append("")
lignes.append("Section calculee automatiquement a partir des donnees du plan d action.")
lignes.append("")
lignes.append("- Sur les " + str(total_ctrl) + " controles du perimetre, "
              + str(nb_couverts) + " disposent d au moins une mesure, soit "
              + str(round(taux_couverture, 1)) + " % de couverture.")
lignes.append("- Le niveau de mise en oeuvre reel est " + niveau
              + " : le score de maturite pondere atteint "
              + str(round(maturite, 1)) + " sur 100. "
              + "L ecart avec le taux de couverture s explique par les mesures "
              + "planifiees mais non encore appliquees.")
lignes.append("- " + str(len(non_demarrees)) + " mesures sur " + str(len(mesures))
              + " ne sont pas demarrees.")
if non_couverts:
    lignes.append("- Aucune mesure ne couvre a ce jour : "
                  + ", ".join(c["titre"] + " (" + c["id"] + ")" for c in non_couverts) + ".")
lignes.append("")
lignes.append("Note de conception : la redaction automatique de cette synthese par le modele "
              "de langage a ete retiree apres plusieurs essais. Le modele reinterpretait les "
              "indicateurs chiffres (confusion entre identifiants de controles et pourcentages, "
              "entre score pondere et decompte). Les chiffres d un rapport de conformite sont "
              "desormais produits exclusivement par le code. Le modele de langage reste utilise "
              "pour la recherche documentaire et l analyse qualitative, ou ses erreurs sont "
              "verifiables par les sources citees.")
lignes.append("")

with open("docs/rapport_conformite.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lignes))

print("Rapport genere : docs/rapport_conformite.md")
print("Taux de couverture :", round(taux_couverture, 1), "%")
print("Score de maturite :", round(maturite, 1), "/100")
