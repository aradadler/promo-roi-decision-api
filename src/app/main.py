from fastapi import FastAPI
from app.fred import fetch_latest_cpi

from app.roi import PromoInputs, calculate_promo_roi
from app.schemas import PromoRequest, PromoResponse, RecommendResponse

app = FastAPI(title="Promo ROI Decision API", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}

def round_financials(data: dict) -> dict:
    return {
        "baseline_revenue": round(data["baseline_revenue"], 2),
        "baseline_profit": round(data["baseline_profit"], 2),
        "promo_revenue": round(data["promo_revenue"], 2),
        "promo_profit": round(data["promo_profit"], 2),
        "incremental_profit": round(data["incremental_profit"], 2),
        "roi": round(data["roi"], 3),
        "break_even_uplift_pct": round(data["break_even_uplift_pct"], 3),
    }

@app.post("/simulate", response_model=PromoResponse)
def simulate(req: PromoRequest):
    inputs = PromoInputs(**req.model_dump())
    r = calculate_promo_roi(inputs)
    rounded = round_financials(r.__dict__)
    return PromoResponse(**rounded)


@app.post("/recommend", response_model=dict)
async def recommend(req: PromoRequest):
    inputs = PromoInputs(**req.model_dump())
    r = calculate_promo_roi(inputs)

    # simple decision rule
    if r.incremental_profit <= 0:
        decision = "NO-GO"
        rationale = "Promo loses money under the current assumptions (incremental_profit <= 0)."
    elif r.roi >= 0.2:
        decision = "GO"
        rationale = "Promo is profitable and meets the ROI threshold (roi >= 0.20)."
    else:
        decision = "REVIEW"
        rationale = "Promo is profitable but ROI is below target; review assumptions and alternatives."

    market_context = await fetch_latest_cpi()

    return {
    **round_financials(r.__dict__),
    "decision": decision,
    "rationale": rationale,
    "market_context": market_context,
    }