<p align="center">
    <img src="https://socialify.git.ci/AntoineMeheut/Acronym-Generator/image?custom_description=Acronym+Generator+%21&description=1&language=1&name=1&pattern=Circuit+Board&theme=Dark" alt="AntoineMeheut" width="700" height="300" />
</p>

<div align="center">
  <img src="https://img.shields.io/github/stars/AntoineMeheut/Acronym-Generator" />
</div>

<br/>

Acronyme Generator
------------------

Générateur d'acronymes corporate : choisissez un mot de base, puis pour chaque lettre choisissez un mot au ton « comité de direction » pour assembler la phrase finale.

## Table des matières
1. [Présentation](#presentation)
2. [Structure du projet](#structure)
3. [Prérequis](#prerequis)
4. [Installation](#install)
5. [Démarrage](#usage)
6. [Tests et couverture](#tests)
7. [Liens utiles](#links)
8. [Contacts](#contacts)
9. [Licence](#licence)

## Présentation <a name="presentation"></a>

Application Django 5.2 qui propose :

- une page d'accueil avec un menu de navigation,
- une page **Acronyme** (`/acronyme/`) avec une combo listant les mots de base (`resources/initlist.py`),
- une fois un mot choisi, autant de dropdowns que de lettres, chacun rempli depuis `resources/wordlist.py`,
- un bouton **Valider** qui affiche la phrase finale.

Documentation OpenAPI/Swagger disponible sur `/swagger/`.

## Structure du projet <a name="structure"></a>

Code source sous `app-src/` (qui sert de racine d'import — `pythonpath = ["", "app-src"]`).

| Package                | Rôle                                                              |
|------------------------|-------------------------------------------------------------------|
| `app-src/config/`      | projet Django (settings, urls, wsgi, asgi)                        |
| `app-src/acronyme/`    | app Django (vues, urls, templates) — pages d'accueil et acronyme  |
| `app-src/resources/`   | données pures : `initlist.GROS_MOTS` et `wordlist.MOTS_PAR_LETTRE`|
| `app-src/logger/`      | formatter JSON in-tree (`JsonFormatter`, `LegacyFormatter`)       |
| `tests/`               | suite pytest : `test_acronyme/` et `test_logger/`                 |

Le module `logger` est référencé dans `LOGGING` (`config/settings.py`) via la classe `logger.formatter.JsonFormatter`.

## Prérequis <a name="prerequis"></a>

- Python ≥ 3.11
- `pip` et `venv`
- Facultatif : PostgreSQL (sinon fallback automatique sur SQLite)

## Installation <a name="install"></a>

1. Cloner le repo

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

État actuel : **92% de couverture** sur 50 tests.

Périmètre couvert (`.coveragerc`) : `app-src/` à l'exception de `manage.py`, `config/{wsgi,asgi,settings}.py`, `migrations/` et `resources/` (données pures).

## Contacts <a name="contacts"></a>

- [Antoine Meheut](mailto:<github.contacts@protonmail.com)

## Licence <a name="licence"></a>

Voir le fichier [`LICENSE`](LICENSE) à la racine du projet.

## Crédits

Ce projet a été généré avec Cookiecutter.

* [Cookiecutter](https://github.com/audreyr/cookiecutter)
