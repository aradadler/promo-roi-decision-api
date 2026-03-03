from dataclasses import dataclass


@dataclass
class PromoInputs:
    baseline_units: float
    price: float
    cogs_per_unit: float
    discount_pct: float
    uplift_pct: float
    cannibalization_pct: float
    duration_weeks: int


@dataclass
class PromoResults:
    baseline_revenue: float
    baseline_profit: float
    promo_revenue: float
    promo_profit: float
    incremental_profit: float
    roi: float
    break_even_uplift_pct: float


def calculate_promo_roi(inputs: PromoInputs) -> PromoResults:
    # Baseline
    baseline_revenue = inputs.baseline_units * inputs.price * inputs.duration_weeks
    baseline_profit = (
        (inputs.price - inputs.cogs_per_unit)
        * inputs.baseline_units
        * inputs.duration_weeks
    )

    # Promo mechanics
    discounted_price = inputs.price * (1 - inputs.discount_pct)

    uplift_units = inputs.baseline_units * inputs.uplift_pct
    cannibalized_units = uplift_units * inputs.cannibalization_pct
    net_incremental_units = uplift_units - cannibalized_units

    total_units_during_promo = (
        inputs.baseline_units + net_incremental_units
    ) * inputs.duration_weeks

    promo_revenue = total_units_during_promo * discounted_price
    promo_profit = (
        (discounted_price - inputs.cogs_per_unit) * total_units_during_promo
    )

    incremental_profit = promo_profit - baseline_profit

    promo_cost = baseline_profit - (
        (discounted_price - inputs.cogs_per_unit)
        * inputs.baseline_units
        * inputs.duration_weeks
    )

    roi = incremental_profit / promo_cost if promo_cost != 0 else 0.0

    # break-even uplift (simplified approximation)
    unit_margin_loss = inputs.price - discounted_price
    baseline_margin = inputs.price - inputs.cogs_per_unit
    new_margin = discounted_price - inputs.cogs_per_unit

    if new_margin <= 0:
        break_even_uplift_pct = float("inf")
    else:
        break_even_uplift_pct = unit_margin_loss / new_margin

    return PromoResults(
        baseline_revenue=baseline_revenue,
        baseline_profit=baseline_profit,
        promo_revenue=promo_revenue,
        promo_profit=promo_profit,
        incremental_profit=incremental_profit,
        roi=roi,
        break_even_uplift_pct=break_even_uplift_pct,
    )