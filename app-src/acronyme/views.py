"""Vues du projet."""

from django.shortcuts import render

from resources.initlist import GROS_MOTS
from resources.wordlist import MOTS_PAR_LETTRE


def home(request):
    """Page d'accueil du site."""
    return render(request, 'acronyme/home.html')


def acronyme_page(request):
    """Page de sélection d'un mot et des mots-clés par lettre."""
    selected = (request.GET.get('word') or '').upper()
    if selected not in GROS_MOTS:
        selected = None

    letter_choices = []
    chosen_words = []
    if selected:
        for index, letter in enumerate(selected):
            available = MOTS_PAR_LETTRE.get(letter, [])
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
        'words': GROS_MOTS,
        'selected_word': selected,
        'letter_choices': letter_choices,
        'sentence': sentence,
    })
