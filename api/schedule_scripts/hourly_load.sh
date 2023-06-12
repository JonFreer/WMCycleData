#!/bin/bash

curl -X 'POST' \
  'localhost/load_vivacity/' \
  -H 'accept: application/json' \
  -H "access_token: ${EXTERNAL_API_TOKEN}" \
  -d ''

# echo "access_token: ${EXTERNAL_API_TOKEN}"