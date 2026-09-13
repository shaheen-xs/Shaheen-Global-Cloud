#!/usr/bin/env bash
set -euo pipefail

echo "=== Shaheen Global Cloud — Tests ==="

echo "[1/3] Running frontend build..."
cd frontend
npm run build
cd ..

echo "[2/3] Running backend tests..."
cd backend
python -m pytest -v
cd ..

echo "[3/3] Validating OpenTofu..."
if command -v tofu &>/dev/null; then
  cd infrastructure/environments/production
  tofu validate
  cd ../../..
else
  echo "  OpenTofu not installed — skipping validation."
fi

echo ""
echo "=== All tests passed ==="
