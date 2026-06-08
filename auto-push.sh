#!/bin/bash

cd /home/ubuntu/sentinel-ops-suite || exit

# Only run if there are changes
if [[ -n $(git status --porcelain) ]]; then
    git add .
    git commit -m "auto update $(date)"
    git push origin main
fi
