#!/bin/bash
set -e
set -x

# run isort recursively
# isort -rc .

# Update pre-commit
pre-commit autoupdate
#run pre-commit
pre-commit run -a

# bash scripts/test.sh --cov-report=html ${@}
# python3 -m pytest
# python3 -m pytest -v -s # verbose
python3 -m pytest

# create coverage-badge
coverage-badge -o ../coverage.svg -f

# document all libraries and their dependencies
pip3 freeze > requirements/all_libraries_used.txt

# generate flake8 report
flake8 --tee . > flake8_report/report.txt

