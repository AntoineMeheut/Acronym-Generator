"""Mots de base du générateur d'acronymes.

Expose :data:`GROS_MOTS`, un tuple de gros mots, jurons, insultes et
expressions argotiques françaises servant de mots de base pour la
génération d'acronymes corporate.

Les mots sont écrits **en majuscules sans accents** : la vue
:func:`acronyme.views.acronyme_page` normalise la saisie utilisateur en
majuscules avant de la valider contre ce tuple. L'ordre d'écriture suit
des regroupements thématiques (jurons, insultes générales, insultes plus
crues…), mais l'affichage dans la combo est trié par ordre alphabétique
français au moment du rendu.
"""

GROS_MOTS = (
    # Jurons / interjections (du plus fort au plus doux)
    "MERDE",
    "PUTAIN",
    "BORDEL",
    "FOUTRE",
    "CHIER",
    "ZUT",
    "FLUTE",
    "MINCE",
    "PUNAISE",
    "CREVINDIEU",
    "SAPRISTI",
    "SACREBLEU",
    "MORBLEU",
    "PARBLEU",
    "FICHTRE",
    "DIANTRE",
    "BIGRE",

    # Insultes générales (personne)
    "CON",
    "CONNARD",
    "CONNASSE",
    "CRETIN",
    "ABRUTI",
    "DEBILE",
    "IMBECILE",
    "IDIOT",
    "COUILLON",
    "ANDOUILLE",
    "CRUCHE",
    "BUSE",
    "NIAIS",
    "BOULET",
    "TOCARD",
    "GLAND",
    "BLAIREAU",
    "BOUFFON",
    "GUIGNOL",
    "BOLOSS",

    # Registre méprisant / moral
    "SALAUD",
    "SALOPE",
    "ORDURE",
    "FUMIER",
    "CRAPULE",
    "VAURIEN",
    "GREDIN",
    "FRIPOUILLE",
    "CANAILLE",
    "CHAROGNE",
    "ENFOIRE",
    "ENFLURE",
    "POURRITURE",
    "BATARD",
    "GOUJAT",
    "MUFLE",
    "RUSTRE",
    "BUTOR",

    # Qualificatifs dévalorisants
    "NUL",
    "NAZE",
    "MINABLE",
    "MINUS",
    "FOIREUX",
    "RIPOU",
    "POURRI",
    "RELOU",
    "CHIANT",
    "EMMERDANT",

    # Crudités anatomiques / sexuelles
    "CUL",
    "BITE",
    "ZOB",
    "COUILLE",
    "CHATTE",
    "NICHON",
    "PUTE",
    "PETASSE",
    "GARCE",
    "POUFIASSE",
    "TRAINEE",
    "CATIN",
    "GRUE",
    "COCU",
    "BRANLEUR",
    "EMMERDEUR",
    "CHIEUR",

    # Scatologique
    "BOUSE",
    "CACA",
    "PISSE",
    "PROUT",
    "PIPEAU",
)
