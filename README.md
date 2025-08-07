# ASA Product Intent API

FastAPI wrapper around `get_products_for_user_intent` that calls the upstream Constructor intent endpoint and returns structured product results.

## Features
- POST `/intent` accepts a natural language query and returns first 5 + all collected products
- GET `/health` for liveness
- CORS enabled for all origins (adjust for production)

## Project Structure
```
asa_api.py        # Core function calling upstream streaming API
server.py         # FastAPI application
requirements.txt  # Python dependencies
run.sh            # Helper script to create venv, install deps, start server
```

## Requirements
- Python 3.12
- Network access to `https://agent.cnstrc.com`

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
Provide the API key in the JSON body field `key` of the `/intent` request (current implementation). Example uses placeholder key.

(Optional future hardening: move key to `X-API-Key` header or environment variable.)

## Endpoint Details
### POST /intent
Request body:
```json
{
  "query": "show me espresso machines with grinder",
  "domain": "explorer",            // optional (default: explorer)
  "thread_id": "optional-thread",  // optional
  "key": "<YOUR_API_KEY>"          // required
}
```
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
curl -X POST http://localhost:8000/intent \
  -H "Content-Type: application/json" \
  -d '{"query":"show me espresso machines with grinder","domain":"explorer","key":"key_Ru5fP55OKVtjZQyP"}'
```

## Error Handling
- 500 if upstream call fails (propagated message truncated only by Python exception message)
- Upstream non-200 currently raises and is returned as 500 with the message

## CORS
All origins, headers, and methods allowed (development friendly). Tighten for production:
```
allow_origins=["https://yourdomain.com"]
```

## Development Notes
- Streaming SSE lines are iterated inside `get_products_for_user_intent`; products deduplicated by ID.
- Function returns only after stream completion.
- If you need partial / incremental streaming to the client, convert endpoint to an async generator / `StreamingResponse`.

## Future Improvements
- Move API key to header or env var + dependency injection
- Add structured error surface (status code passthrough)
- Add logging & request IDs
- Optional pagination / limit parameter
- Implement streaming response passthrough

## License
Internal / Unspecified (add a license file if distributing externally).
