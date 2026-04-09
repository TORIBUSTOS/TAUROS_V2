# TORO_Prime

Motor de análisis financiero inteligente. Reconstrucción profesional del MVP TAUROS.

## Estructura

```
toro-prime/
├── backend/               # FastAPI + SQLAlchemy
│   ├── src/
│   │   ├── api/          # Routes (FastAPI)
│   │   ├── services/     # Business logic
│   │   ├── models/       # SQLAlchemy ORM
│   │   ├── core/         # Config
│   │   └── main.py       # App entry
│   ├── tests/            # Pytest
│   └── requirements.txt
└── frontend/             # Next.js (futuro)
```

## Setup Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

## Run Tests

```bash
pytest -v --cov=src
```

## Run Server

```bash
python -m uvicorn src.main:app --reload --port 9000
```

API docs: http://localhost:9000/docs

## Protocolo

- Protocolo TORO LAB v2 (Gates + Bloques Negros)
- BN-001: Parser + Categorización (en desarrollo)
- Ver `prd/` para documentación completa
