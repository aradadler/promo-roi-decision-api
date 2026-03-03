from pydantic import BaseModel, Field


class PromoRequest(BaseModel):
    baseline_units: float = Field(..., gt=0)
    price: float = Field(..., gt=0)
    cogs_per_unit: float = Field(..., ge=0)
    discount_pct: float = Field(..., ge=0, le=1)
    uplift_pct: float = Field(..., ge=0)
    cannibalization_pct: float = Field(..., ge=0, le=1)
    duration_weeks: int = Field(..., ge=1)


class PromoResponse(BaseModel):
    baseline_revenue: float
    baseline_profit: float
    promo_revenue: float
    promo_profit: float
    incremental_profit: float
    roi: float
    break_even_uplift_pct: float


class RecommendResponse(PromoResponse):
    decision: str
    rationale: str