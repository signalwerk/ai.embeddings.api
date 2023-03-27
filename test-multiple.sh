#!/bin/bash

# Load variables from .env file
source .env

curl http://0.0.0.0:5003/v1/embeddings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "input": ["Your text goes here", "Your second text goes here"],
    "model": "text-embedding-multilingual-001"
  }'