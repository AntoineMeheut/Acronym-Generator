"""Package ``resources`` — données du générateur d'acronymes.

Regroupe les deux jeux de données utilisés par l'application :

- :mod:`resources.initlist` — :data:`~resources.initlist.GROS_MOTS`,
  la liste des mots de base servant d'acronymes (jurons, insultes,
  injures argotiques…) ;
- :mod:`resources.wordlist` — :data:`~resources.wordlist.MOTS_PAR_LETTRE`,
  un dictionnaire ``{lettre: [mots]}`` recensant les mots au ton
  « comité de direction » pour chaque lettre de l'alphabet.

Ces deux structures sont des constantes Python pures (aucun I/O), donc
exclues de la couverture de tests (cf. ``.coveragerc``).
"""
