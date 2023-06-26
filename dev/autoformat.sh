#!/bin/bash

(
    cd api/
    autoflake --recursive --remove-all-unused-imports --in-place API/
    isort \
        --multi-line=3 \
        --trailing-comma \
        --force-grid-wrap=0 \
        --use-parentheses \
        --line-width=88 \
        API/
    black API/
)

(
    cd web/
    npx prettier --write .
)