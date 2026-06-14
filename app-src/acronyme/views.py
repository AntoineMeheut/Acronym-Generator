"""Vues de l'application ``acronyme``.

Ce module fournit deux vues :

- :func:`home` — rend la page d'accueil avec le menu de navigation.
- :func:`acronyme_page` — rend la page de génération d'acronymes : sélection
  d'un mot de base puis, pour chaque lettre, choix d'un mot au ton corporate
  pour assembler la phrase finale.

Les listes affichées dans les combos sont triées par ordre alphabétique
français (insensible aux accents et à la casse) via :func:`_sort_key`. Les
fichiers de données :mod:`resources.initlist` et :mod:`resources.wordlist`
ne sont pas modifiés : le tri est appliqué au moment du rendu.
"""

import unicodedata

from django.shortcuts import render

from resources.initlist import GROS_MOTS
from resources.wordlist import MOTS_PAR_LETTRE


def _sort_key(word):
    """Clé de tri alphabétique insensible aux accents et à la casse.

    Normalise la chaîne en forme NFD puis retire les caractères combinants
    (accents), ce qui permet de placer ``Élégance`` correctement entre
    ``Education`` et ``Emotion`` au lieu de le rejeter après ``Z``.

    Args:
        word: Mot à transformer en clé de tri.

    Returns:
        La forme minuscule du mot, sans accents, utilisable comme clé de
        tri alphabétique français.
    """
    normalized = unicodedata.normalize('NFD', word)
    stripped = ''.join(c for c in normalized if not unicodedata.combining(c))
    return stripped.lower()


def home(request):
    """Rend la page d'accueil du site.

    Args:
        request: Requête HTTP entrante.

    Returns:
        Réponse HTTP rendant ``acronyme/home.html``.
    """
    return render(request, 'acronyme/home.html')


def acronyme_page(request):
    """Rend la page de sélection d'un mot et des mots-clés par lettre.

    Le paramètre GET ``word`` désigne le mot de base. Il est normalisé en
    majuscules et validé contre :data:`resources.initlist.GROS_MOTS`. Si le
    mot est inconnu, il est ignoré (``selected`` vaut ``None``).

    Pour chaque lettre du mot sélectionné, un dropdown est construit à
    partir de :data:`resources.wordlist.MOTS_PAR_LETTRE`. Les choix sont
    relus depuis les paramètres GET ``letter_0``, ``letter_1``, … et
    invalidés si le mot proposé n'appartient pas à la liste pour la lettre.

    La phrase finale n'est produite que si **tous** les choix de lettres
    sont valides.

    Args:
        request: Requête HTTP entrante. Paramètres GET acceptés :
            ``word`` et ``letter_<index>``.

    Returns:
        Réponse HTTP rendant ``acronyme/acronyme.html`` avec le contexte :

        - ``words`` : liste triée des mots de base ;
        - ``selected_word`` : mot retenu, ou ``None`` ;
        - ``letter_choices`` : liste de dictionnaires (un par lettre)
          contenant ``index``, ``letter``, ``words`` (triés) et ``chosen`` ;
        - ``sentence`` : phrase générée si tous les choix sont valides,
          sinon chaîne vide.
    """
    selected = (request.GET.get('word') or '').upper()
    if selected not in GROS_MOTS:
        selected = None

    letter_choices = []
    chosen_words = []
    if selected:
        for index, letter in enumerate(selected):
            available = sorted(MOTS_PAR_LETTRE.get(letter, []), key=_sort_key)
            chosen = request.GET.get(f'letter_{index}', '')
            if chosen not in available:
                chosen = ''
            letter_choices.append({
                'index': index,
                'letter': letter,
                'words': available,
                'chosen': chosen,
            })
            chosen_words.append(chosen)

    sentence = ' '.join(chosen_words) if selected and all(chosen_words) else ''

    return render(request, 'acronyme/acronyme.html', {
        'words': sorted(GROS_MOTS, key=_sort_key),
        'selected_word': selected,
        'letter_choices': letter_choices,
        'sentence': sentence,
    })
