# ASA Product Intent API

FastAPI wrapper around `get_products_for_user_intent` that calls the upstream Constructor intent endpoint and returns structured product results.

## Features
- GET `/intent` accepts a natural language query and returns first 5 + all collected products
- GET `/health` for liveness
- CORS enabled for all origins (adjust for production)

## Project Structure
```
asa_api.py        # Core function calling upstream streaming API
server.py         # FastAPI application
requirements.txt  # Python dependencies
```

## Install & Run
Using helper script (recommended):
```
./run.sh
```
(First make executable if needed: `chmod +x run.sh`)

Manual steps:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

## Authentication
Provide the API key as a query parameter `key` in the `/intent` request. Example uses placeholder key.

## Endpoint Details
### GET /intent
Query parameters:
- `query` (required): Natural language query for product search
- `key` (required): API key for authentication
- `domain` (optional): Domain for the search (default: "explorer")
- `thread_id` (optional): Thread ID for conversation context

Example: `/intent?query=show me espresso machines with grinder&key=<YOUR_API_KEY>`
Response body example shape:
```json
{
  "first_five_products": [
    {"id": "123", "title": "...", "link": "https://...", "image": "https://..."}
  ],
  "all_products": [ {"id": "123", ...}, {"id": "456", ...} ]
}
```

### GET /health
```
{"status": "ok"}
```

## Example cURL
Single line:
```
curl "https://asa-api.onrender.com/intent?query=show%20me%20espresso%20machines%20with%20grinder&key=key_Ru5fP55OKVtjZQyP&domain=explorer"
```

With all parameters:
```
curl "https://asa-api.onrender.com/intent?query=coffee%20makers&key=key_Ru5fP55OKVtjZQyP&domain=explorer&thread_id=thread123"
```
