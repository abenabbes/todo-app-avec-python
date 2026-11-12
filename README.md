# ✅ Gestionnaire de Tâches — FastAPI + SQLAlchemy async + Streamlit

Projet pédagogique : une **API REST** de gestion de tâches (FastAPI +
SQLAlchemy asynchrone) et un **dashboard interactif** (Streamlit) qui la
consomme, dockerisé et déployé sur Render.

## 🏗️ Architecture

┌─────────────────┐     HTTP/REST      ┌──────────────┐      async      ┌────────────┐
│   Streamlit     │ ─────────────────► │   FastAPI    │ ──────────────► │ PostgreSQL │
│  (dashboard)    │   (requests)       │   (API)      │  (SQLAlchemy)   │    (BDD)   │
└─────────────────┘                    └──────────────┘                 └────────────┘

| Composant | Rôle | Port local |
|-----------|------|------------|
| Streamlit | Interface utilisateur, visualisation | 8501 |
| FastAPI | Endpoints CRUD, validation Pydantic | 8000 |
| SQLAlchemy async | ORM non-bloquant (sessions, modèles) | — |
| SQLite / PostgreSQL | Persistance (SQLite en dev, PostgreSQL en prod) | 5432 |

## 📁 Structure

todo-app/
├── api/
│   ├── main.py           # Point d'entrée FastAPI (lifespan, CORS)
│   ├── config.py         # Configuration via pydantic-settings + .env
│   ├── database.py       # Engine async, session, get_db, init_db
│   ├── models.py         # Modèle Task (SQLAlchemy 2.0 typé)
│   ├── schemas.py        # Schémas Pydantic (validation entrée/sortie)
│   ├── routers/tasks.py  # Endpoints CRUD
│   └── Dockerfile
├── frontend/
│   ├── app.py            # Dashboard Streamlit
│   └── Dockerfile
├── tests/test_api.py     # Tests API avec httpx
├── docker-compose.yml    # 3 services : db, api, frontend
├── requirements.txt
└── .env                  # Variables locales (non committé)

## 🔌 Endpoints de l'API

| Méthode | Route | Description | Code succès |
|---------|-------|-------------|-------------|
| GET | `/health` | Vérification de santé | 200 |
| GET | `/tasks/` | Lister toutes les tâches | 200 |
| POST | `/tasks/` | Créer une tâche | 201 |
| GET | `/tasks/{id}` | Détail d'une tâche | 200 |
| PATCH | `/tasks/{id}` | Modifier (titre, description, done) | 200 |
| DELETE | `/tasks/{id}` | Supprimer | 204 |

Documentation interactive : **`/docs`** (Swagger UI générée automatiquement).

## 🚀 Lancement local (sans Docker)

# 1. Environnement virtuel
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows

# 2. Dépendances
pip install -r requirements.txt

# 3. Lancer (2 terminaux)
python -m uvicorn api.main:app --reload      # Terminal 1 — API
python -m streamlit run frontend/app.py      # Terminal 2 — Frontend

- API : http://localhost:8000/docs
- Dashboard : http://localhost:8501

Par défaut, la base est **SQLite** (fichier `todo.db`, créé automatiquement).
Personnalisable via `.env` :

DATABASE_URL=sqlite+aiosqlite:///./todo.db

## 🐳 Lancement avec Docker

docker compose up --build

Démarrage de **3 services** :
- `db` : PostgreSQL 16 (données persistées dans le volume `pgdata`)
- `api` : FastAPI connecté à la base via `postgresql+asyncpg://todo:todo@db:5432/todo`
- `frontend` : Streamlit pointant vers `http://api:8000`

> 💡 Dans Docker, les services se joignent par **nom de service** (`db`, `api`),
> pas par `localhost` — c'est le réseau interne Docker qui résout ces noms.

Arrêt : `Ctrl+C` puis `docker compose down`. Les données survivent grâce au volume.

## ☁️ Déploiement sur Render

3 services séparés, tous depuis le même repo GitHub :

1. **PostgreSQL** : New + → PostgreSQL (plan Free) → copier l'*Internal Database URL*
2. **API** : New + → Web Service → repo GitHub
   - Docker Root Directory : `api`
   - Variable d'environnement `DATABASE_URL` = Internal URL avec le schéma
     `postgresql+asyncpg://` (au lieu de `postgres://`)
   - L'API se redéploie automatiquement à chaque `git push`
3. **Frontend** : New + → Web Service → même repo
   - Docker Root Directory : `frontend`
   - Variable `API_URL` = l'URL publique de l'API (ex: `https://todo-api.onrender.com`)

> ⚠️ Plan gratuit Render : les services s'endorment après ~15 min d'inactivité
> (première requête lente au réveil), et la base free a une durée limitée.

## 🧪 Tests

pytest tests/

## 🛠️ Problèmes rencontrés & solutions (Windows)

- `uvicorn.exe : Accès refusé` sous PowerShell → lancer via le module Python :
  `python -m uvicorn api.main:app --reload` (idem pour streamlit)
- `{"detail":"Not Found"}` sur la racine `/` → normal, la route racine n'existe
  pas ; utiliser `/docs`, `/health` ou `/tasks/`

## 📚 Concepts appris

- Environment virtuel (`venv`) et gestion des dépendances
- FastAPI : routage, injection de dépendances (`Depends`), validation Pydantic
- SQLAlchemy 2.0 async : moteur, sessions, modèles typés (`Mapped`)
- Pattern config : `pydantic-settings` + `.env` (12-factor app)
- CORS : pourquoi le frontend a besoin de l'autoriser côté API
- Docker : Dockerfile, image vs conteneur, docker-compose, réseaux, volumes, healthchecks
- Déploiement : Git/GitHub, services managés, variables d'environnement en prod
