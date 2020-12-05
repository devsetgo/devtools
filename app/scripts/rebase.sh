#!/bin/bash
set -e
set -x
CAL_VER=$(TZ=America/New_York date +"%y-%m-%d_%H:%M:%S")
# run of Alembic
echo "Rebase"
git rebase origin/main
