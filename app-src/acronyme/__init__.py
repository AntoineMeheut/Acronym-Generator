"""Application Django ``acronyme``.

Expose les pages du générateur d'acronymes corporate :

- la page d'accueil (``home``) avec un menu de navigation,
- la page **Acronyme** (``acronyme_page``) qui propose la sélection d'un mot de
  base puis, pour chacune de ses lettres, le choix d'un mot au ton « comité de
  direction » pour assembler la phrase finale.

Les données sources sont importées depuis le package :mod:`resources` :

- :data:`resources.initlist.GROS_MOTS` — la liste des mots de base,
- :data:`resources.wordlist.MOTS_PAR_LETTRE` — les mots disponibles par lettre.
"""
