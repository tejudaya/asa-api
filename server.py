from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
import os
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware

from asa_api import get_products_for_user_intent

app = FastAPI(title="ASA Product Intent API", version="1.0.0")

# CORS (allow all origins; adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Models
# -----------------------------
class IntentRequest(BaseModel):
    query: str
    thread_id: Optional[str] = None
    domain: str = "explorer"
    key: str = None

class Product(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    link: Optional[str] = None
    image: Optional[str] = None

class IntentResponse(BaseModel):
    first_five_products: List[Product]
    all_products: List[Product]


# -----------------------------
# Routes
# -----------------------------
@app.post("/intent", response_model=IntentResponse, summary="Get products for a natural language intent")
def intent_endpoint(payload: IntentRequest):
    try:
        data = get_products_for_user_intent(
            query=payload.query,
            thread_id=payload.thread_id,
            domain=payload.domain,
            api_key=payload.key,
        )
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", summary="Health check")
def health():
    return {"status": "ok"}

# -----------------------------
# Local dev helper
# -----------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
