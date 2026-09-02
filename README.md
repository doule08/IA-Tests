# ToDo List API (FastAPI + PostgreSQL)

Application ToDo List en Python développée avec **FastAPI**, **Pydantic v2**, **SQLAlchemy 2.0 (Async)** et **PostgreSQL** avec le driver **asyncpg**. L'application est conçue selon une architecture en couches propre (**Controller - Service - Repository**) garantissant scalabilité et haute maintenabilité.

---

## 🚀 Fonctionnalités

- **Ajouter une tâche** (`POST /api/v1/todos/`)
- **Lister les tâches** (`GET /api/v1/todos/`) avec filtre optionnel par statut (`is_completed`)
- **Consulter une tâche par ID** (`GET /api/v1/todos/{todo_id}`)
- **Modifier une tâche** (`PUT /api/v1/todos/{todo_id}`)
- **Supprimer une tâche** (`DELETE /api/v1/todos/{todo_id}`)
- **Interface Swagger OpenAPI interactive** (`http://127.0.0.1:8000/docs`)

---

## 🏗️ Architecture du Projet

```
IA-Tests/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   └── todos.py        # Controller FastAPI (Endpoints REST)
│   │       └── router.py           # Agrégateur des routes v1
│   ├── core/
│   │   └── config.py               # Configuration & variables d'environnement
│   ├── db/
│   │   └── session.py              # Connexion & Session Async SQLAlchemy
│   ├── models/
│   │   └── todo.py                 # Modèle ORM SQLAlchemy (table `todos`)
│   ├── repositories/
│   │   ├── base.py                 # Interface abstraite du Repository
│   │   ├── json_repository.py      # Implémentation JSON (fallback)
│   │   └── postgres_repository.py  # Implémentation PostgreSQL (AsyncSession)
│   ├── schemas/
│   │   └── todo.py                 # Schémas de données Pydantic v2
│   ├── services/
│   │   └── todo_service.py         # Couche métier
│   └── main.py                     # Application FastAPI et Lifespan DB
├── tests/
│   └── test_todos.py               # Suite de tests unitaires Pytest (SQLite in-memory)
├── .env.example                    # Modèle de variables d'environnement
├── pyproject.toml                  # Dépendances gérées par uv
└── README.md
```

---

## 🛢️ Configuration de la Base de Données (PostgreSQL)

L'application lit la configuration depuis un fichier `.env` à la racine du projet.

### 1. Création du fichier `.env`
Dupliquez le fichier `.env.example` en `.env` :

```bash
cp .env.example .env
```

### 2. Variables de connexion
Renseignez les accès de votre instance PostgreSQL dans `.env` :

```env
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=votre_mot_de_passe
POSTGRES_DB=todo_db

# Alternative via chaîne de connexion complète :
# DATABASE_URL=postgresql+asyncpg://postgres:votre_mot_de_passe@localhost:5432/todo_db
```

> **Note :** La table `todos` est créée automatiquement dans PostgreSQL au démarrage de l'application FastAPI via le gestionnaire de `lifespan`.

---

## 🛠️ Installation et Lancement avec `uv`

### 1. Installation du venv et des dépendances
```bash
uv sync
```

### 2. Démarrage du serveur Uvicorn
```bash
uv run uvicorn app.main:app --reload
```

L'API sera accessible sur **`http://127.0.0.1:8000`**.

### 3. Documentation Swagger interactive
Rendez-vous sur **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)** pour tester les endpoints interactivement.

---

## 🧪 Exécution des Tests Automatisés

Les tests unitaires s'exécutent avec une base de données **SQLite en mémoire** (`sqlite+aiosqlite:///:memory:`). Vous n'avez pas besoin d'avoir un serveur PostgreSQL démarré pour exécuter les tests.

Exécuter les tests :
```bash
uv run pytest
```

Exécuter les tests avec affichage détaillé (`verbose`) :
```bash
uv run pytest -v
```
