#!/bin/bash
set -e
set -x

# mkdocs
mkdocs build
CUR_DIR=$(pwd)
# Copy Contribute to Github Contributing
cp $CUR_DIR/docs/index.md $CUR_DIR/README.md


mkdocs gh-deploy