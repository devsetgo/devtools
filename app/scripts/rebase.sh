#!/bin/bash
set -e
set -x

# run of git rebase
echo "Rebase"
git rebase origin/main
