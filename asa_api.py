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
                prod_id = prod.get('data', {}).get('id')
                if not prod_id or prod_id in seen_ids:
                    continue
                seen_ids.add(prod_id)
                info = {
                    'id': prod_id,
                    'title': prod.get('value'),
                    'link': prod.get('data', {}).get('url'),
                    'image': prod.get('data', {}).get('image_url'),
                }
                all_products.append(info)
                # Distribute into first 5 vs rest
                if len(first_five) < 5:
                    first_five.append(info)
                    # print(f"Product {len(first_five)}: {info}")

        except json.JSONDecodeError:
            # fallback to raw text
            print(payload, file=sys.stderr)

    # After full stream completes, show counts
    # print(f"First 5 products collected: {len(first_five)}")
    # print(f"Total products collected: {len(all_products)}")
    return {
        "first_five_products": first_five, 
        "all_products": all_products
    }