# Rapport de conformite ISO/IEC 27001 - perimetre de test

Genere le 2026-09-23 par le copilote GRC. Document de travail, a valider par un analyste.

## Indicateurs de pilotage

| Indicateur | Valeur |
|---|---|
| Controles du referentiel | 15 |
| Controles couverts par au moins une mesure | 10 |
| Taux de couverture | 66.7 % |
| Score de maturite pondere | 30.0 / 100 |
| Mesures au plan d action | 8 |
| Mesures - Applique | 3 |
| Mesures - En cours | 2 |
| Mesures - Non demarre | 3 |

## Maturite par thematique

| Thematique | Score moyen | Controles |
|---|---|---|
| Organisationnel | 8.3 | 6 |
| Personnes | 100.0 | 1 |
| Physique | 0.0 | 1 |
| Technologique | 42.9 | 7 |

## Controles sans mesure associee

- **5.1** Politiques de securite de l information (Organisationnel)
- **5.7** Renseignement sur les menaces (Organisationnel)
- **5.23** Securite des services cloud (Organisationnel)
- **7.2** Controle des acces physiques (Physique)
- **8.7** Protection contre les logiciels malveillants (Technologique)

## Plan d action

| Mesure | Statut | Controles | Responsable | Echeance |
|---|---|---|---|---|
| Revue trimestrielle des droits d acces sur Active Directory | En cours | 8.2,5.15 | Equipe IT | 2027-03-31 |
| Scan de vulnerabilites hebdomadaire et correction des failles critiques sous 15 jours | Applique | 8.8 | RSSI | 2026-12-31 |
| Clause de securite signee par les prestataires accedant au SI | Non demarre | 5.19 | Juridique | 2027-06-30 |
| Campagne de sensibilisation au phishing deux fois par an | Applique | 6.3 | RSSI | 2026-11-30 |
| Sauvegarde quotidienne et test de restauration trimestriel | En cours | 8.13 | Equipe IT | 2027-02-28 |
| Centralisation des journaux et conservation 12 mois | Non demarre | 8.15,8.16 | Equipe IT | 2027-09-30 |
| Chiffrement des postes portables | Applique | 8.24 | Equipe IT | 2026-10-31 |
| Procedure de gestion de crise cyber testee annuellement | Non demarre | 5.24 | RSSI | 2027-12-31 |

## Constat

Section calculee automatiquement a partir des donnees du plan d action.

- Sur les 15 controles du perimetre, 10 disposent d au moins une mesure, soit 66.7 % de couverture.
- Le niveau de mise en oeuvre reel est faible : le score de maturite pondere atteint 30.0 sur 100. L ecart avec le taux de couverture s explique par les mesures planifiees mais non encore appliquees.
- 3 mesures sur 8 ne sont pas demarrees.
- Aucune mesure ne couvre a ce jour : Politiques de securite de l information (5.1), Renseignement sur les menaces (5.7), Securite des services cloud (5.23), Controle des acces physiques (7.2), Protection contre les logiciels malveillants (8.7).

Note de conception : la redaction automatique de cette synthese par le modele de langage a ete retiree apres plusieurs essais. Le modele reinterpretait les indicateurs chiffres (confusion entre identifiants de controles et pourcentages, entre score pondere et decompte). Les chiffres d un rapport de conformite sont desormais produits exclusivement par le code. Le modele de langage reste utilise pour la recherche documentaire et l analyse qualitative, ou ses erreurs sont verifiables par les sources citees.
