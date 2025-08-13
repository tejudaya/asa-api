# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ASA API is a FastAPI wrapper around Constructor's intent-based product search service. It processes natural language queries and returns structured product results by consuming Server-Sent Events (SSE) from an upstream API.

## Development Commands

```bash
# Start the server (recommended - handles virtual environment)
./run.sh

# Run server with auto-reload during development
uvicorn server:app --host 0.0.0.0 --port 8000 --reload

# Install/update dependencies
pip install -r requirements.txt
```

## Architecture

### Core Components

1. **server.py** - FastAPI application with two endpoints:
   - `GET /intent` - Main product search endpoint with query parameters
   - `GET /health` - Simple health check

2. **asa_api.py** - Core logic for:
   - Making streaming requests to Constructor API
   - Parsing SSE responses
   - Deduplicating products by ID
   - Structuring the response with first 5 products separated

### Request Flow

1. Client sends GET to `/intent` with query parameters (query, key, domain, thread_id)
2. FastAPI validates query parameters using Query validators
3. `get_products_for_user_intent()` streams data from Constructor API
4. Products are collected, deduplicated, and returned in structured format

### Key Design Decisions

- API key passed as query parameter for simplicity and GET method compatibility
- Stateless design - no database or session management
- Returns both `first_five_products` and `all_products` for flexible UI rendering
- CORS enabled with wildcard origin (should be restricted in production)

## Testing & Validation

Currently no test suite exists. When adding tests:
- Use pytest as the testing framework
- Test both successful API calls and error scenarios
- Mock the upstream Constructor API responses
- Validate Pydantic model serialization/deserialization

## Common Tasks

### Adding New Query Parameters
1. Add new query parameter to the `intent_endpoint` function signature with Query validator
2. Pass new parameters to `get_products_for_user_intent()` in asa_api.py
3. Include parameters in the Constructor API request

### Modifying Response Structure
1. Update the response handling in `get_products_for_user_intent()` (asa_api.py:64-89)
2. Adjust the return format in the `/intent` endpoint (server.py:43-61)

### Debugging Streaming Issues
- Check SSE parsing logic in asa_api.py:51-63
- Log raw response chunks before JSON parsing
- Verify Constructor API is returning expected format

## Important Notes

- The Constructor API endpoint is: `https://agent.cnstrc.com/v1/intent`
- Default domain is "explorer" but can be overridden per request
- Product deduplication uses the `id` field from Constructor's response
- Empty or malformed SSE data chunks are silently skipped