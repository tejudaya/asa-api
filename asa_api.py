import requests
import json
import sys
from urllib.parse import quote_plus


def get_products_for_user_intent(query: str, thread_id: str|None = None, domain: str = "explorer", api_key: str|None = None) -> dict:
    """
    This tools helps fetch products for a Natural Language query made by the user.

    Args:
    - query: str -> Natural Language query made by the user
    
    Return -> dict:
    - first_five_products: List of first five products
    - all_products: List of all the products including the first five
    """
    if not api_key:
        raise NotImplementedError("API key is required to access the product search service.")
    
    base_url = "https://agent.cnstrc.com/v1/intent"
    # URL-encode query so spaces/special chars don’t break the path
    path     = f"{base_url}/{quote_plus(query)}"
    params   = {
        "key":       api_key,
        "domain":    domain,
    }
    if thread_id:
        params["thread_id"] = thread_id

    
    headers  = {
        "Accept": "text/event-stream",
    }

    resp = requests.get(path, params=params, headers=headers, stream=True)
    resp.raise_for_status()

    messages = []
    all_products = []
    first_five = []
    seen_ids = set()
    # Each line in the SSE is like "data: { ... }"
    for raw in resp.iter_lines():
        if not raw:
            continue
        line = raw.decode("utf-8")
        if not line.startswith("data:"):
            continue

        payload = line[len("data:"):].strip()
        # Sometimes the stream sends “[DONE]” or similar keep-alive lines
        if payload in ("[DONE]", ""):
            continue

        try:
            obj = json.loads(payload)
            messages.append(obj)

            # Extract products if present
            results = obj.get('response', {}).get('results', [])
            for prod in results:
                data = prod.get('data', {})
                prod_id = data.get('id')
                if not prod_id or prod_id in seen_ids:
                    continue
                seen_ids.add(prod_id)
                
                # Extract all available product attributes
                info = {
                    'id': prod_id,
                    'title': prod.get('value'),
                    'matched_terms': prod.get('matched_terms', []),
                    'is_slotted': prod.get('is_slotted', False),
                    'labels': prod.get('labels', {}),
                    
                    # Basic product info
                    'url': data.get('url'),
                    'image_url': data.get('image_url'),
                    'variation_id': data.get('variation_id'),
                    'description': data.get('description'),
                    'product_blurb': data.get('productBlurb'),
                    'product_info': data.get('prodinfo'),
                    
                    # Pricing information
                    'lowest_price': data.get('lowestPrice'),
                    'highest_price': data.get('highestPrice'),
                    'sale_price_min': data.get('salePriceMin'),
                    'sale_price_max': data.get('salePriceMax'),
                    'regular_price_min': data.get('regularPriceMin'),
                    'regular_price_max': data.get('regularPriceMax'),
                    'product_price_type': data.get('productPriceType'),
                    'swatch_prices': data.get('swatchPrices'),
                    
                    # Availability
                    'min_avl_now_pl': data.get('minAvlNowPL'),
                    
                    # Images
                    'leader_sku': data.get('leaderSku'),
                    'leader_sku_image': data.get('leaderSkuImage'),
                    'thumb_image': data.get('thumb_image'),
                    'thumb_image_parent': data.get('thumb_image_parent'),
                    'image_override': data.get('imageOverride'),
                    'alt_images': data.get('altImages'),
                    'hover_images': data.get('hoverImages'),
                    'image_roll_overs': data.get('imageRollOvers'),
                    
                    # Product variants/swatches
                    'swatches_display': data.get('swatchesDisplay'),
                    
                    # Categories and groups
                    'group_ids': data.get('group_ids', []),
                    
                    # Facets (detailed product attributes)
                    'facets': data.get('facets', []),
                    
                    # Flags
                    'flags': data.get('flags', []),
                    
                    # Purchase info
                    'pip_type': data.get('pipType'),
                    'eligible_for_quick_buy': data.get('eligibleForQuickBuy', False),
                }
                
                all_products.append(info)
                # Distribute into first 5 vs rest
                if len(first_five) < 5:
                    first_five.append(info)
                    
        except json.JSONDecodeError:
            # fallback to raw text
            print(payload, file=sys.stderr)
    
        # After full stream completes, show counts
        # print(f"First 5 products collected: {len(first_five)}")
        # print(f"Total products collected: {len(all_products)}")
    
    return {
        "first_five_products": first_five, 
        "all_products": all_products,
        # "messages": messages  # Include raw messages for debugging if needed
    }


if __name__ == "__main__":
    query = "coffee makers with small capacity"
    api_key = "key_PysinTjKriGSD1Zl"
    result = get_products_for_user_intent(query, api_key=api_key)
    print(result['first_five_products'])
