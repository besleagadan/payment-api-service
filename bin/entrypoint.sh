#!/bin/bash
set -e

echo "Starting server..."
exec uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
