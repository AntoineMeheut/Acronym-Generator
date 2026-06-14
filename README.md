<p align="center">
    <img src="https://socialify.git.ci/AntoineMeheut/Acronym-Generator/image?custom_description=Acronym+Generator+%21&description=1&language=1&name=1&pattern=Circuit+Board&theme=Dark" alt="AntoineMeheut" width="700" height="300" />
</p>

<div align="center">
  <img src="https://img.shields.io/github/stars/AntoineMeheut/Acronym-Generator" />
</div>

<br/>

Acronyme Generator
------------------

Générateur d'acronymes corporate : choisissez un mot de base (un gros mot, un juron, une insulte argotique…), puis pour chaque lettre choisissez un mot au ton « comité de direction » pour assembler une phrase finale à consonance sérieuse.

## Table des matières
1. [Présentation](#presentation)
2. [Structure du projet](#structure)
3. [Prérequis](#prerequis)
4. [Installation](#install)
5. [Démarrage](#usage)
6. [Tests et couverture](#tests)
7. [Documentation du code](#docs)
8. [Contacts](#contacts)
9. [Licence](#licence)

## Présentation <a name="presentation"></a>

Application Django 5.2 qui propose :

- une page d'accueil avec un menu de navigation ;
- une page **Acronyme** (`/acronyme/`) avec une combo listant les mots de base (`resources/initlist.py`) ;
- une fois un mot choisi, autant de dropdowns que de lettres, chacun rempli depuis `resources/wordlist.py` ;
- un bouton **Valider** qui affiche la phrase finale.

Les listes affichées dans les combos sont **triées par ordre alphabétique français** (insensible aux accents et à la casse) au moment du rendu — les fichiers de données conservent leurs regroupements thématiques.

Documentation OpenAPI/Swagger disponible sur `/swagger/` (UI Swagger), `/swagger/redoc/` (Redoc) et `/swagger/schema/` (schéma brut), exposés via `drf-spectacular`.

## Structure du projet <a name="structure"></a>

Code source sous `app-src/` (racine d'import — `pythonpath = ["", "app-src"]` dans `pytest.ini`).

| Package                | Rôle                                                                  |
|------------------------|-----------------------------------------------------------------------|
| `app-src/config/`      | projet Django (settings, urls, wsgi, asgi)                            |
| `app-src/acronyme/`    | app Django (vues, urls, templates) — pages d'accueil et acronyme      |
| `app-src/resources/`   | données pures : `initlist.GROS_MOTS` et `wordlist.MOTS_PAR_LETTRE`    |
| `app-src/logger/`      | formatters JSON in-tree (`JsonFormatter`, `LegacyFormatter`)          |
| `tests/`               | suite pytest : `test_acronyme/` et `test_logger/`                     |

Le module `logger` est référencé dans `LOGGING` (`config/settings.py`) via la classe `logger.formatter.JsonFormatter` — les logs console sortent ainsi directement au format JSON.

### Vue d'ensemble du flux

1. L'utilisateur arrive sur `/acronyme/` et choisit un mot dans la combo (sélection envoyée en paramètre GET `word`).
2. La vue [`acronyme_page`](app-src/acronyme/views.py) normalise la saisie en majuscules et la valide contre `GROS_MOTS`.
3. Pour chaque lettre, un dropdown trié alphabétiquement est construit depuis `MOTS_PAR_LETTRE`.
4. Les choix utilisateur sont relus dans `letter_0`, `letter_1`, … et invalidés s'ils sortent de la liste autorisée.
5. La phrase finale est concaténée et affichée si — et seulement si — **tous** les choix sont valides.

## Prérequis <a name="prerequis"></a>

- Python ≥ 3.11
- `pip` et `venv`
- Facultatif : PostgreSQL (sinon fallback automatique sur SQLite)

## Installation <a name="install"></a>

1. Cloner le repo.

2. Créer le virtualenv et installer les dépendances (runtime + dev) :
   ```shell
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   python -m pip install -r app-src/requirements.txt
   python -m pip install -r app-src/requirements-dev.txt
   ```

3. (Optionnel) Copier le template d'environnement local :
   ```shell
   cp app-src/.env.dist app-src/.env
   ```
   Les valeurs par défaut de `.env.dist` permettent un démarrage immédiat (DEBUG=True, SQLite).

## Démarrage <a name="usage"></a>

Depuis la **racine** du projet :

```shell
source .venv/bin/activate
ENV_PATH=app-src/.env.dist python app-src/manage.py runserver 127.0.0.1:8000
```

> `ENV_PATH` est obligatoire si vous lancez depuis la racine — sans lui, `settings.py` cherche `.env.dist` dans le répertoire courant et ne le trouve pas.

L'application est disponible sur :

| URL                                   | Page                                    |
|---------------------------------------|-----------------------------------------|
| http://127.0.0.1:8000/                | Accueil                                 |
| http://127.0.0.1:8000/acronyme/       | Générateur d'acronyme                   |
| http://127.0.0.1:8000/swagger/        | Documentation Swagger UI                |
| http://127.0.0.1:8000/swagger/redoc/  | Documentation Redoc                     |
| http://127.0.0.1:8000/swagger/schema/ | Schéma OpenAPI brut                     |

Sanity check Django (sans démarrer le serveur) :

```shell
cd app-src && ENV_PATH=.env.dist ../.venv/bin/python manage.py check
```

## Tests et couverture <a name="tests"></a>

Le projet utilise `pytest`, `pytest-django`, `pytest-env` et `pytest-cov`. Configuration dans `pytest.ini` et `.coveragerc`.

**Lancer la suite de tests** :
```shell
source .venv/bin/activate
pytest
```

**Lancer la suite avec couverture (rapport terminal)** :
```shell
pytest --cov --cov-report=term-missing
```

**Générer un rapport HTML détaillé** (créé dans `htmlcov/`) :
```shell
pytest --cov --cov-report=html
open htmlcov/index.html
```

**Échouer le build si la couverture passe sous le seuil** (utile en CI — seuil 80%) :
```shell
pytest --cov --cov-fail-under=80
```

État actuel : **50 tests** verts. Périmètre couvert (`.coveragerc`) : `app-src/` à l'exception de `manage.py`, `config/{wsgi,asgi,settings}.py`, `migrations/` et `resources/` (données pures).

## Documentation du code <a name="docs"></a>

Tous les modules Python du projet sont documentés via des docstrings (format Google / reST). Quelques points d'entrée utiles :

- [`acronyme/views.py`](app-src/acronyme/views.py) — les deux vues `home` et `acronyme_page`, et la clé de tri alphabétique français `_sort_key`.
- [`acronyme/urls.py`](app-src/acronyme/urls.py) — routes de l'app.
- [`config/settings.py`](app-src/config/settings.py) — paramètres Django, `LOGGING`, `SPECTACULAR_SETTINGS`.
- [`config/urls.py`](app-src/config/urls.py) — routes racine + Swagger.
- [`logger/formatter.py`](app-src/logger/formatter.py) — `JsonFormatter` et `LegacyFormatter`, avec helpers module-level.
- [`resources/initlist.py`](app-src/resources/initlist.py) et [`resources/wordlist.py`](app-src/resources/wordlist.py) — données du générateur.

Pour générer une documentation HTML à partir des docstrings, on peut utiliser un outil tiers (Sphinx, pdoc, mkdocs-material…) en pointant vers `app-src/` ; aucune configuration n'est fournie par défaut.

## Contacts <a name="contacts"></a>

- [Antoine Meheut](mailto:github.contacts@protonmail.com)

## Licence <a name="licence"></a>

Voir le fichier [`LICENSE`](LICENSE) à la racine du projet.

## Crédits

Ce projet a été généré avec Cookiecutter.

* [Cookiecutter](https://github.com/audreyr/cookiecutter)
