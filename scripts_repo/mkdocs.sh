#!/bin/bash
set -e
set -x

# mkdocs
mkdocs build

# Copy Contribute to Github Contributing
cp ~/twitter_star_task_service/docs/index.md ~/twitter_star_task_service/README.md


mkdocs gh-deploy