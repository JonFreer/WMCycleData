#!/bin/sh

set -e

exec 1>&2

(
    cd api/
    autoflake --recursive --remove-all-unused-imports --check API/
    isort --check \
        --multi-line=3 \
        --trailing-comma \
        --force-grid-wrap=0 \
        --use-parentheses \
        --line-width=88 \
        API/
    black --check API/
    # mypy app
)

(
    cd web/
    npx prettier --check .
)