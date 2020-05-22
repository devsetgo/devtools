#!/bin/bash
set -e
set -x
CAL_VER=$(TZ=America/New_York date +"%y-%m-%d_%H:%M:%S")
# run of Alembic
echo "Alembic: Start"
alembic init alembic || true

echo "Alembic: Revision"
alembic revision -m $CAL_VER

echo "Alembic: Update Head"
alembic upgrade head