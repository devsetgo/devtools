#!/bin/bash
set -e
set -x
#delete db
rm ~/twitter_star/app/sqlite_db/api.db
#delete logs
rm ~/twitter_star/app/log/app_log.log
# run dev
uvicorn main:app --port 5000 --reload --log-level debug

