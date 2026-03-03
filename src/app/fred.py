from __future__ import annotations

from datetime import date
from typing import Any

import httpx

from app.settings import get_fred_api_key


FRED_BASE = "https://api.stlouisfed.org/fred"


async def fetch_latest_cpi() -> dict[str, Any]:
    """
    Fetch the latest CPI (CPIAUCSL) observation from FRED.
    Returns a dict with: {"series": "...", "date": "...", "value": "..."} or {"error": "..."}.
    """
    api_key = get_fred_api_key()
    if not api_key:
        return {"error": "FRED_API_KEY not set"}

    params = {
        "series_id": "CPIAUCSL",
        "api_key": api_key,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 1,
    }

    url = f"{FRED_BASE}/series/observations"
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url, params=params)
            r.raise_for_status()
            data = r.json()

        obs = data.get("observations", [])
        if not obs:
            return {"error": "No observations returned from FRED"}

        latest = obs[0]
        return {
            "series": "CPIAUCSL",
            "date": latest.get("date", str(date.today())),
            "value": latest.get("value"),
        }
    except Exception as e:
        return {"error": f"FRED request failed: {e}"}