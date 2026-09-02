# 📝 ToDo List Application Fullstack (FastAPI + PostgreSQL + React TypeScript)

Application ToDo List moderne et performante, développée avec un backend en **Python FastAPI**, **Pydantic v2**, **SQLAlchemy 2.0 Async**, **PostgreSQL** et un frontend dynamique en **React 18**, **TypeScript**, **Vite** et **Lucide Icons**.

L'application repose sur une **Clean Architecture** (Controller -> Service -> Repository Pattern) garantissant le découplage, la testabilité et la scalabilité.

---

## 🌟 Fonctionnalités

- ✨ **Ajouter une tâche** : Titre obligatoire et description facultative.
- 📋 **Lister & Filtrer les tâches** : Onglets réactifs (*Toutes*, *En cours*, *Terminées*).
- ✏️ **Édition en ligne** : Modification dynamique du titre et de la description sans rechargement.
- ✅ **Cocher / Décocher** : Mise à jour instantanée du statut d'accomplissement.
- 🗑️ **Supprimer une tâche** : Suppression définitive avec animation de transition.
- 📊 **Statistiques en temps réel** : Compteur dynamique de tâches restantes et réalisées.
- 📖 **Documentation API OpenAPI / Swagger** : Disponible sur `http://127.0.0.1:8000/docs`.

---

## 🏗️ Architecture du Projet

```
IA-Tests/
├── app/                            # Backend FastAPI (Python)
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/todos.py  # Path Operation Functions (Controller API)
│   │       └── router.py           # Agrégateur des routes v1
│   ├── core/
│   │   └── config.py               # Settings Pydantic & variables d'environnement
│   ├── db/
│   │   └── session.py              # Connexion & session Async SQLAlchemy (asyncpg)
│   ├── models/
│   │   └── todo.py                 # Modèle ORM SQLAlchemy (table `todos`)
│   ├── repositories/
│   │   ├── base.py                 # Interface d'abstraction Repository Pattern
│   │   ├── json_repository.py      # Implémentation JSON de secours
│   │   └── postgres_repository.py  # Implémentation PostgreSQL (AsyncSession)
│   ├── schemas/
│   │   └── todo.py                 # Schémas de validation Pydantic v2
│   ├── services/
│   │   └── todo_service.py         # Couche logique métier (Business Logic)
│   └── main.py                     # Application FastAPI et initialisation Lifespan
├── frontend/                       # Frontend React + TypeScript + Vite
│   ├── src/
│   │   ├── components/             # Header, TodoForm, TodoList, TodoItem, TodoFilter
│   │   ├── services/
│   │   │   └── api.ts              # Client d'appel API REST typé
│   │   ├── types/
│   │   │   └── todo.ts             # Interfaces TypeScript (Todo, TodoCreate, etc.)
│   │   ├── App.tsx                 # Composant racine
│   │   ├── index.css               # Design réactif moderne (Thème sombre)
│   │   └── main.tsx                # Point d'entrée DOM React
│   ├── vite.config.ts              # Configuration Vite avec proxy vers http://127.0.0.1:8000
│   ├── tsconfig.json               # Configuration du compilateur TypeScript
│   └── package.json                # Dépendances frontend
├── tests/
│   └── test_todos.py               # Tests unitaires Pytest (SQLite in-memory)
├── .env.example                    # Fichier modèle pour les variables d'environnement
├── pyproject.toml                  # Dépendances backend gérées par uv
└── README.md
```

---

## 🛢️ 1. Configuration & Démarrage du Backend (FastAPI)

### a. Pré-requis
- Python `>= 3.10`
- `uv` (Gestionnaire d'environnement Python ultra-rapide)
- Une instance **PostgreSQL** active (ex: locale ou Docker)

### b. Configuration des variables d'environnement
Dupliquez le fichier `.env.example` à la racine pour créer votre fichier `.env` :

```bash
cp .env.example .env
```

Modifiez le fichier `.env` avec vos identifiants PostgreSQL :

```env
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=votre_mot_de_passe
POSTGRES_DB=todo_db
```

### c. Installation et Lancement
1. Installez les dépendances backend :
   ```bash
   uv sync
   ```
2. Lancez le serveur Uvicorn :
   ```bash
   uv run uvicorn app.main:app --reload
   ```

Le backend sera accessible sur **`http://127.0.0.1:8000`**.  
La documentation interactive Swagger OpenAPI est disponible sur **`http://127.0.0.1:8000/docs`**.

> **Note :** Les tables PostgreSQL sont créées automatiquement au premier lancement du serveur via le gestionnaire de `lifespan`.

---

## 💻 2. Lancement du Frontend (React + TypeScript + Vite)

### a. Pré-requis
- Node.js `>= 18` et `npm`

### b. Installation et Lancement
1. Accédez au dossier frontend :
   ```bash
   cd frontend
   ```
2. Installez les dépendances npm :
   ```bash
   npm install
   ```
3. Démarrez le serveur de développement Vite :
   ```bash
   npm run dev
   ```

L'application web sera accessible dans votre navigateur sur **`http://localhost:3000`**.

### c. Commandes utiles Frontend
- `npm run dev` : Lance le serveur de développement Vite.
- `npm run typecheck` : Vérifie le typage TypeScript (`tsc --noEmit`).
- `npm run build` : Compile l'application pour la production (`dist/`).

---

## 🧪 3. Exécution des Tests Automatisés Backend

Les tests unitaires utilisent une base **SQLite en mémoire** (`sqlite+aiosqlite:///:memory:`) et s'exécutent de manière totalement autonome sans nécessiter de serveur PostgreSQL démarré.

Exécuter la suite de tests avec Pytest :
```bash
uv run pytest
```

Exécuter les tests avec affichage détaillé :
```bash
uv run pytest -v
```

---

## 🛠️ 4. Dépannage & Résolution des Problèmes Courants (FAQ)

### Erreur `'vite' n'est pas reconnu` ou `Pre-transform error` (Windows / File Locks)
Si vous obtenez un message indiquant que `vite` n'est pas reconnu ou qu'un module est introuvable après l'arrêt d'un processus :

1. **Arrêtez tous les serveurs Node/Vite en cours** (`Ctrl + C` dans les terminaux ou fermez les terminaux ouverts).
2. Rendez-vous dans le dossier `frontend` :
   ```bash
   cd frontend
   ```
3. Supprimez les fichiers de cache et réinstallez proprement :
   ```bash
   # Sur Windows (PowerShell)
   Remove-Item -Recurse -Force node_modules, package-lock.json -ErrorAction SilentlyContinue
   npm install
   ```
4. Relancez ensuite :
   ```bash
   npm run dev
   ```
