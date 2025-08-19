from fastapi import FastAPI, Header, HTTPException, Depends, Query
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
    url: Optional[str] = None
    image_url: Optional[str] = None
    matched_terms: Optional[List[str]] = None
    is_slotted: Optional[bool] = None
    labels: Optional[dict] = None
    variation_id: Optional[str] = None
    description: Optional[str] = None
    product_blurb: Optional[str] = None
    product_info: Optional[str] = None
    lowest_price: Optional[float] = None
    highest_price: Optional[float] = None
    sale_price_min: Optional[float] = None
    sale_price_max: Optional[float] = None
    regular_price_min: Optional[float] = None
    regular_price_max: Optional[float] = None
    product_price_type: Optional[str] = None
    swatch_prices: Optional[dict] = None
    min_avl_now_pl: Optional[str] = None
    leader_sku: Optional[str] = None
    leader_sku_image: Optional[str] = None
    thumb_image: Optional[str] = None
    thumb_image_parent: Optional[str] = None
    image_override: Optional[str] = None
    alt_images: Optional[List[str]] = None
    hover_images: Optional[List[str]] = None
    image_roll_overs: Optional[List[str]] = None
    swatches_display: Optional[dict] = None
    group_ids: Optional[List[str]] = None
    facets: Optional[List[dict]] = None
    flags: Optional[List[str]] = None
    pip_type: Optional[str] = None
    eligible_for_quick_buy: Optional[bool] = None

class IntentResponse(BaseModel):
    first_five_products: List[Product]
    all_products: List[Product]


# -----------------------------
# Routes
# -----------------------------
@app.get("/intent", response_model=IntentResponse, summary="Get products for a natural language intent")
def intent_endpoint(
    query: str = Query(..., description="Natural language query for product search"),
    key: str = Query(..., description="API key for authentication"),
    thread_id: Optional[str] = Query(None, description="Optional thread ID for conversation context"),
    domain: str = Query("explorer", description="Domain for the search")
):
    try:
        data = get_products_for_user_intent(
            query=query,
            thread_id=thread_id,
            domain=domain,
            api_key=key,
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
