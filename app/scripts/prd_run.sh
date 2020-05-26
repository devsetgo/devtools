#!/bin/bash
set -e
set -x

# run dev
gunicorn -c gunicorn_cfg.py main:app
