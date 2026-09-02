# ToDo List API (FastAPI)

Application ToDo List en Python développée avec **FastAPI**, **Pydantic** et une architecture en couches propre (**Controller - Service - Repository**) prête pour la production et la scalabilité.

## 🚀 Fonctionnalités

- **Ajouter une tâche** (`POST /api/v1/todos/`)
- **Lister les tâches** (`GET /api/v1/todos/`) avec filtre optionnel par statut (`is_completed`)
- **Consulter une tâche** (`GET /api/v1/todos/{todo_id}`)
- **Modifier une tâche** (`PUT /api/v1/todos/{todo_id}`)
- **Supprimer une tâche** (`DELETE /api/v1/todos/{todo_id}`)
- **Interface Swagger interactive** (`http://127.0.0.1:8000/docs`)

## 🏗️ Architecture

```
IA-Tests/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   └── todos.py        # Controller FastAPI
│   │       └── router.py           # Agrégateur des routes v1
│   ├── core/
│   │   └── config.py               # Configuration de l'application
│   ├── repositories/
│   │   ├── base.py                 # Interface abstraite du Repository
│   │   └── json_repository.py      # Implémentation de persistance JSON
│   ├── schemas/
│   │   └── todo.py                 # Modèles de données Pydantic v2
│   ├── services/
│   │   └── todo_service.py         # Couche métier
│   └── main.py                     # Point d'entrée de l'application
├── data/
│   └── todos.json                  # Stockage JSON persistant
├── tests/
│   ├── test_todos.py
├── pyproject.toml
└── README.md
```

## 🛠️ Installation et Lancement avec `uv`

### 1. Installation du venv et des dépendances
```bash
uv sync
```
ou si vous préférez installer le venv manuellement :
```bash
uv venv
uv pip install -e .
```

### 2. Démarrage du serveur uvicorn
```bash
uv run uvicorn app.main:app --reload
```

L'API sera accessible sur `http://127.0.0.1:8000`.

### 3. Utilisation Swagger
Rendez-vous sur [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) pour tester les endpoints interactivement.

### 4. Exécution des tests unitaires avec Pytest
Pour exécuter les tests unitaires et vérifier le bon fonctionnement de l'API :
```bash
uv run pytest
```
Pour afficher des détails supplémentaires sur l'exécution des tests :
```bash
uv run pytest -v
```

