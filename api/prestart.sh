#!/bin/bash

echo "Running pre start"
# db-init

uvicorn API.main:app --host 0.0.0.0 --port 80 --reload