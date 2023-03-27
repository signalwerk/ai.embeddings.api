# API for embeddings

Generates sentence embeddings from a input string with the [Sentence-BERT Multi-Lingual Model `distiluse-base-multilingual-cased-v1`](https://www.sbert.net/docs/pretrained_models.html#multi-lingual-models).

## Example requests

The API request is the same like for the [OpenAI API](https://platform.openai.com/docs/guides/embeddings/what-are-embeddings).

The `input` can be a string or a list of strings.  
The `model` is the name of the model. Available: `text-embedding-multilingual-001`

```bash
curl http://0.0.0.0:5003/v1/embeddings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "input": "Your text goes here",
    "model": "text-embedding-multilingual-001"
  }'
```

## Development

```bash
python3 -m venv embeddings # create virtual environment
source embeddings/bin/activate # activate virtual environment
pip install … # install dependencies
pip freeze > requirements.txt # save dependencies
python app.py # run app
deactivate # deactivate virtual environment
```

## Thanks

This implementation started with the [API-Server from AnzorGozalishvili](https://github.com/AnzorGozalishvili/sentence_transformers_serving)
