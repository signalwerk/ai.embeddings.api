#!/usr/bin/env python

import os
import sys

from flask import Flask, jsonify, request, render_template
from sentence_transformers import SentenceTransformer
from waitress import serve
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
model_name_or_path = os.environ.get('SENTENCE_MODEL', "sentence-transformers/distiluse-base-multilingual-cased-v1")
model_name_short = os.environ.get('SENTENCE_MODEL_SHORT', "text-embedding-multilingual-001")
debug = os.environ.get('DEBUG', "false").lower() == "true"
api_keys = os.environ.get('API_KEY', '').split(',')
port = int(os.environ.get('PORT', 5003))

if not all(len(api_key) >= 8 for api_key in api_keys):
    print("API_KEY is not set or too short (must be at least 8 characters long).")
    sys.exit(1)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route('/')
def home():
    return render_template('index.html', model_name_short=model_name_short)

@app.route('/v1/embeddings', methods=['POST'])
def encode():
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not any(f'Bearer {api_key}' in auth_header for api_key in api_keys):
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    input_text = data.get("input", "")
    requested_model = data.get("model")

    if requested_model != model_name_short:
        return jsonify({'error': f'Model {requested_model} not supported'}), 400

    if isinstance(input_text, str):
        input_text = [input_text]

    if not isinstance(input_text, list):
        return jsonify({'error': 'Invalid input format'}), 400

    embeddings = encoder.encode(input_text)
    embeddings = [x.tolist() for x in embeddings]

    tokenizer = encoder.tokenizer
    tokens_count = sum(len(tokenizer.encode_plus(text, add_special_tokens=False)['input_ids']) for text in input_text)
    # tokens_count = sum(len(text.split()) for text in input_text), # fast alternative

    response = {
        "data": [
            {
                "embedding": embedding,
                "index": i,
                "object": "embedding"
            }
            for i, embedding in enumerate(embeddings)
        ],
        "model": model_name_short,
        "object": "list",
        "usage": {
            "prompt_tokens": tokens_count,
            "total_tokens": tokens_count
        }
    }

    return jsonify(response)

if __name__ == '__main__':

    sentence_cache_path = os.environ.get("SENTENCE_TRANSFORMERS_HOME")
    print(f"Sentence Cache Path (SENTENCE_TRANSFORMERS_HOME): {sentence_cache_path}")

    encoder = SentenceTransformer(model_name_or_path, cache_folder=sentence_cache_path)

    print(f"Server starting on port {port}...")

    if debug:
        app.run(debug=True, use_reloader=True, host='0.0.0.0', port=port)
    else:
        serve(app, host='0.0.0.0', port=port)
