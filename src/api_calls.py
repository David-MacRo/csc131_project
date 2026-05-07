from typing import Optional, Any
import json
import time
import urllib.request
import urllib.parse
import urllib.error
from config import BASE_URL


def _get(endpoint: str, params: Optional[dict] = None) -> Any:
    url = f"{BASE_URL}/{endpoint.lstrip('/')}"

    if params:
        url += "?" + urllib.parse.urlencode(params)
    
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "CSC131-ConflictScraper/1.0"})

    while True:
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body)
        except urllib.error.HTTPError as exc:
            print(f"  [HTTP {exc.code}] {url}")
            time.sleep(2)
        except Exception as exc:
            print(f"  [ERROR] {url} – {exc}")
            time.sleep(2)
    
def _get_all(endpoint: str, extra_params: Optional[dict] = None) -> list:
    """
    Transparently page through all results for an endpoint that supports
    OData $top / $skip.
    """
    results = []
    skip = 0
    while True:
        params = {"$top": 1000, "$skip": skip}
        if extra_params:
            params.update(extra_params)
        batch = _get(endpoint, params)
        if not batch:
            break
        results.extend(batch)
        if len(batch) < 1000:
            break          # last page
        skip += 1000
        time.sleep(0.3)
    return results