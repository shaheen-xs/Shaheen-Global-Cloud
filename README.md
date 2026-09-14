<div align="center">

<img src="assets/xhhz80.png" alt="Shaheen Global Cloud" width="420">

# **Shaheen-Global-Cloud**

### Modern Cloud Infrastructure Platform


_____

# Shaheen Global Cloud

A premium cloud infrastructure management platform for provisioning, monitoring, and scaling virtual machines.

## Architecture

```
Frontend (React + Vite + TypeScript)
  → FastAPI (Python backend)
    → Redis Job Queue
      → Worker (async processor)
        → Dagger (CI/CD engine)
          → OpenTofu (Infrastructure as Code)
            → Mock Provider (Phase 1)
```

## Project Structure

```
Shaheen-Global-Cloud/
├── frontend/               # React + Vite + TypeScript + Tailwind
│   ├── src/
│   │   ├── components/     # LandingPage, Dashboard, ServerList, ServerDetails, CreateServerForm, Navigation
│   │   ├── services/       # API client, server service, types
│   │   ├── App.tsx         # Root component with hash-based routing
│   │   ├── main.tsx        # Entry point
│   │   └── index.css       # Global styles + Tailwind
│   ├── Dockerfile
│   └── package.json
├── backend/                # FastAPI + SQLAlchemy + Redis
│   ├── app/
│   │   ├── api/v1/         # REST endpoints (health, servers, jobs, metadata)
│   │   ├── core/           # Logging, security
│   │   ├── database/       # SQLAlchemy models, base, session
│   │   ├── providers/      # Mock infrastructure provider
│   │   ├── queue/          # Redis job queue
│   │   ├── services/       # Business logic (dagger, job, provider, server)
│   │   ├── config.py       # Pydantic settings
│   │   ├── main.py         # FastAPI app
│   │   └── worker.py       # Async job worker
│   ├── tests/              # pytest + httpx
│   ├── Dockerfile
│   ├── requirements.txt
│   └── pytest.ini
├── dagger/                 # Dagger module (Python SDK)
│   ├── main.py             # Provision, destroy, start, stop, restart, validate
│   └── dagger.json
├── infrastructure/         # OpenTofu (Terraform-compatible)
│   ├── modules/ubuntu-vm/  # Reusable VM module
│   └── environments/production/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       ├── versions.tf
│       └── terraform.tfvars
├── scripts/
│   ├── setup.sh
│   └── test.sh
├── docker-compose.yml      # Full stack: postgres, redis, backend, worker, frontend
├── .env.example
└── README.md
```

## Quick Start

### Docker Compose (recommended)

```
cp .env.example .env
docker compose up -d
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Manual Setup

```
# 1. Start PostgreSQL and Redis
docker run -d --name pg -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=shaheen postgres:16-alpine
docker run -d --name redis -p 6379:6379 redis:7-alpine

# 2. Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# 3. Worker (separate terminal)
cd backend
python -m app.worker

# 4. Frontend
cd frontend
npm install
npm run dev
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/servers` | List all servers |
| POST | `/api/v1/servers` | Create a server |
| GET | `/api/v1/servers/{id}` | Get server details |
| DELETE | `/api/v1/servers/{id}` | Delete a server |
| POST | `/api/v1/servers/{id}/start` | Start a server |
| POST | `/api/v1/servers/{id}/stop` | Stop a server |
| POST | `/api/v1/servers/{id}/restart` | Restart a server |
| GET | `/api/v1/jobs` | List jobs |
| GET | `/api/v1/jobs/{id}` | Get job details |
| GET | `/api/v1/plans` | List available plans |
| GET | `/api/v1/regions` | List available regions |
| GET | `/api/v1/images` | List available OS images |

## Server Plans

| Plan | vCPU | Memory | Disk | $/hr |
|------|------|--------|------|------|
| Micro | 1 | 1 GB | 20 GB | $0.005 |
| Small | 2 | 2 GB | 40 GB | $0.012 |
| Medium | 4 | 4 GB | 80 GB | $0.024 |
| Large | 8 | 8 GB | 160 GB | $0.048 |
| X-Large | 16 | 16 GB | 320 GB | $0.096 |

## Phase 1 — MVP

Phase 1 uses a **mock provider** — no real cloud resources are created. The full pipeline (Frontend → FastAPI → Redis → Worker → Dagger → OpenTofu → Mock Provider) is functional end-to-end with simulated infrastructure.

## Development

```
# Run tests
./scripts/test.sh

# Validate OpenTofu
cd infrastructure/environments/production
tofu init && tofu validate

# Run backend tests only
cd backend && pytest -v
```

## License

Proprietary — Shaheen Global Cloud
</div>
