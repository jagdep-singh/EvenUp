# EvenUp

Group expense tracker. Split bills, track debts, settle up.

---

## Monorepo Structure

```
EvenUp/
├── mobile-app/             # React Native mobile client (Expo)
├── Backend/                # FastAPI REST API
├── web-app/ 
└── README.md
```

Each directory has its own README with setup instructions, project structure, and tech details.

---

## Stack

| | Technology |
|--|------------|
| Mobile | React Native (Expo) · TypeScript |
| Backend | FastAPI · Python 3.11+ |
| Database | PostgreSQL |
| Cache / Queue | Redis · Celery |
| Auth | JWT (access + refresh) |

---

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11+
- Docker + Docker Compose
- Expo CLI (`npm install -g expo-cli`)

### 1. Backend

```bash
cd backend

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Start Postgres + Redis
docker compose up -d

# Run migrations
alembic upgrade head

# Dev server
uvicorn app.main:app --reload --port 8000
```

API docs → `http://localhost:8000/docs`

### 2. App

```bash
cd app

npm install

# Point to your local backend
echo "EXPO_PUBLIC_API_URL=http://localhost:8000" > .env

npx expo start
```

Press `i` for iOS simulator, `a` for Android emulator.

---

## Features

- Personal expense tracking
- Group expense splitting (equal / exact / percentage)
- Automatic balance calculation per group
- Debt simplification via min-cash-flow algorithm
- Settlement recording
- Group expenses auto-synced to personal tracker

---

## Contributing

1. Branch off `main` — `feat/your-feature` or `fix/your-fix`
2. Keep `app/` and `backend/` changes in separate commits
3. PR against `main`, link any related issues
