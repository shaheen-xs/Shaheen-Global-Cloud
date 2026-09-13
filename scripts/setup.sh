#!/usr/bin/env bash
set -euo pipefail

echo "=== Shaheen Global Cloud — Setup ==="

# Backend
echo "[1/4] Installing backend dependencies..."
cd backend
pip install -r requirements.txt -r requirements-dev.txt
cd ..

# Frontend
echo "[2/4] Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Infrastructure
echo "[3/4] Checking OpenTofu..."
if command -v tofu &>/dev/null; then
  cd infrastructure/environments/production
  tofu init
  cd ../../..
  echo "  OpenTofu initialized."
else
  echo "  OpenTofu not found — skipping init (mock provider works without it)."
fi

# Dagger
echo "[4/4] Checking Dagger..."
if command -v dagger &>/dev/null; then
  echo "  Dagger CLI found."
else
  echo "  Dagger CLI not found — install from https://docs.dagger.io"
fi

echo ""
echo "=== Setup complete ==="
echo "Start the stack with:    docker compose up -d"
echo "Run backend only:        cd backend && uvicorn app.main:app --reload"
echo "Run worker only:        cd backend && python -m app.worker"
echo "Run frontend only:       cd frontend && npm run dev"
