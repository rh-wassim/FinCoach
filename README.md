# 💰 FinCoach — AI Financial Coach

> Application web de finances personnelles : suivez vos dépenses, importez vos relevés, fixez des objectifs d'épargne et recevez des recommandations financières générées par IA.

FinCoach aide un utilisateur à reprendre le contrôle de son budget. Les transactions sont **catégorisées automatiquement** (règles + IA), un **tableau de bord** résume les revenus / dépenses / épargne, et un **coach IA** fournit des conseils personnalisés ainsi qu'un chatbot.

---

## ✨ Fonctionnalités

- **Authentification** sécurisée (JWT + bcrypt)
- **Tableau de bord** : KPIs du mois (revenus, dépenses, solde, taux d'épargne), graphiques (camembert par catégorie, évolution mensuelle)
- **Transactions** : ajout manuel, **import CSV**, filtres, recherche, modification, suppression
- **Catégorisation intelligente** : règles par mots-clés, puis repli sur l'IA (Groq / DeepSeek / Hugging Face)
- **Objectifs d'épargne** : création, suivi de progression, contributions
- **Recommandations IA** : 3 conseils mensuels basés sur les dépenses réelles
- **Chatbot / assistant** financier
- **Analytics** avancés (Recharts)
- **Multilingue** (FR / EN), **thème clair / sombre**, **multi-devises**

---

## 🏗️ Architecture

```
┌──────────────┐      REST/HTTP     ┌──────────────┐     Sequelize     ┌─────────────────┐
│  Frontend    │ ───────────────▶  │   Backend    │ ───────────────▶ │  Supabase        │
│ React + Vite │ ◀───────────────  │   Express    │ ◀─────────────── │  PostgreSQL      │
│  :3000       │                    │   :5050      │                   └─────────────────┘
└──────────────┘                    └──────┬───────┘
                                           │ HTTP
                                           ▼
                                    ┌──────────────┐
                                    │  ML Service  │
                                    │ Flask + sklearn
                                    │  :5001       │
                                    └──────────────┘
```

| Couche | Technologie | Port |
|--------|-------------|------|
| Frontend | React 19 · Vite · Tailwind CSS v3 · Recharts · React Router | `3000` |
| Backend | Node.js · Express 5 · Sequelize · JWT · Multer | `5050` |
| Service ML | Python · Flask · scikit-learn (TF-IDF + régression logistique) | `5001` |
| Base de données | Supabase PostgreSQL (hébergée) | — |

---

## 📁 Structure du projet

```
.
├── backend/                 # API REST Express
│   ├── config/              # connexion Sequelize + Supabase
│   ├── controllers/         # auth, transactions, dashboard, goals, recommandations, chatbot
│   ├── middlewares/         # vérification JWT
│   ├── models/              # User, Transaction, Category, SavingGoal, Recommendation
│   ├── routes/              # définition des routes /api/*
│   ├── utils/               # catégorisation IA, parsing CSV, moteurs chatbot/reco
│   └── server.js            # point d'entrée
├── frontend/                # application React
│   └── src/
│       ├── pages/           # Dashboard, Transactions, Goals, Analytics, Landing, ...
│       ├── components/      # design system (fincoach/, ui/)
│       ├── context/         # Auth, Theme, I18n, Currency
│       └── services/        # appels API (axios)
├── ml-service/              # microservice de classification
│   ├── app.py               # serveur Flask (/health, /predict)
│   ├── model.py             # modèle scikit-learn
│   └── data/                # données d'entraînement
└── docker-compose.yml       # orchestration des 3 services
```

---

## 🚀 Démarrage rapide

### Prérequis
- **Node.js** ≥ 18
- **Python** ≥ 3.10
- Le fichier `backend/.env` (jamais commité — voir ci-dessous)

### 1. Cloner le dépôt
```bash
git clone git@github.com:rh-wassim/FinCoach.git
cd FinCoach
```

### 2. Variables d'environnement
Créez `backend/.env` à partir de l'exemple :
```bash
cp backend/.env.example backend/.env
```
Puis renseignez les valeurs (voir [Variables d'environnement](#-variables-denvironnement)).

### 3. Backend
```bash
cd backend
npm install
node server.js          # http://localhost:5050
```

### 4. Frontend
```bash
cd frontend
npm install
npm run dev             # http://localhost:3000
```

### 5. Service ML
```bash
cd ml-service
pip install -r requirements.txt
python app.py           # http://localhost:5001
```

### 6. Docker (optionnel)
```bash
docker-compose up --build
```

> 💡 La base de données est hébergée sur **Supabase** — aucun PostgreSQL local n'est nécessaire.

---

## 🔐 Variables d'environnement

`backend/.env` (à ne **jamais** committer) :

| Variable | Description |
|----------|-------------|
| `PORT` | Port du backend (par défaut `5050`) |
| `DATABASE_URL` | Chaîne de connexion PostgreSQL (Supabase) |
| `SUPABASE_URL` | URL du projet Supabase |
| `SUPABASE_ANON_KEY` | Clé publique Supabase |
| `JWT_SECRET` | Secret de signature des tokens JWT |
| `ML_SERVICE_URL` | URL du microservice ML (`http://localhost:5001/`) |
| `GROQ_API_KEY` | Clé API Groq (catégorisation / IA) — optionnel |
| `HF_TOKEN` | Token Hugging Face — optionnel |
| `HF_MODEL` | Modèle Hugging Face utilisé — optionnel |

> Au moins un fournisseur IA (`GROQ_API_KEY`, `HF_TOKEN` ou `DEEPSEEK_API_KEY`) est nécessaire pour la catégorisation IA et les recommandations. Sans clé, le projet retombe sur la catégorisation par mots-clés.

---

## 🔌 Aperçu de l'API

Toutes les routes (sauf auth) requièrent l'en-tête `Authorization: Bearer <token>`.

| Méthode | Route | Description |
|---------|-------|-------------|
| `POST` | `/api/auth/register` | Créer un compte |
| `POST` | `/api/auth/login` | Se connecter (retourne un JWT) |
| `GET` | `/api/transactions` | Lister les transactions |
| `POST` | `/api/transactions` | Créer une transaction |
| `POST` | `/api/transactions/upload` | Importer un CSV |
| `GET` | `/api/dashboard/summary` | KPIs du mois |
| `GET` | `/api/dashboard/by-category` | Répartition par catégorie |
| `GET` | `/api/goals` | Lister les objectifs |
| `POST` | `/api/goals/:id/contribute` | Contribuer à un objectif |
| `GET` | `/api/recommendations` | Recommandations IA |
| `POST` | `/api/chatbot` | Discuter avec l'assistant |

Service ML : `POST /predict` `{ "description": "..." }` → `{ "category": "...", "confidence": 0.9 }`

---

## 🧪 Tests

```bash
# Backend (Jest)
cd backend && npm test

# Frontend (Vitest + Testing Library)
cd frontend && npm test
```

---

## 👥 Équipe

| Membre | Rôle |
|--------|------|
| **Wassim Rhilane** | Dashboard, analytics, modèle ML, intégration finale |
| **Mohamed Hajita** | Backend Express, auth JWT, IA, chatbot, sécurité |
| **Ilyasse Dbiza** | Service ML Flask, endpoint `/predict` |
| **Israe El Hilali** | UI, landing page, responsive, thème clair/sombre |
| **Oumayma Mektane** | Tests, QA, documentation, pages documents/profil |

---

## 📄 Licence

Projet académique — usage éducatif.
