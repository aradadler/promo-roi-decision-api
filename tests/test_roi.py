import math

from app.roi import PromoInputs, calculate_promo_roi


def test_baseline_math_matches_expected():
    inputs = PromoInputs(
        baseline_units=10000,
        price=4.99,
        cogs_per_unit=2.20,
        discount_pct=0.20,
        uplift_pct=0.35,
        cannibalization_pct=0.10,
        duration_weeks=2,
    )
    r = calculate_promo_roi(inputs)

    assert math.isclose(r.baseline_revenue, 99800.0, rel_tol=1e-9)
    assert math.isclose(r.baseline_profit, 55800.0, rel_tol=1e-9)


def test_no_discount_no_uplift_means_no_change():
    inputs = PromoInputs(
        baseline_units=1000,
        price=10.0,
        cogs_per_unit=6.0,
        discount_pct=0.0,
        uplift_pct=0.0,
        cannibalization_pct=0.0,
        duration_weeks=1,
    )
    r = calculate_promo_roi(inputs)

    assert math.isclose(r.incremental_profit, 0.0, abs_tol=1e-9)


def test_discount_without_uplift_should_reduce_profit():
    inputs = PromoInputs(
        baseline_units=1000,
        price=10.0,
        cogs_per_unit=6.0,
        discount_pct=0.10,  # discount price -> lower margin
        uplift_pct=0.0,     # no volume lift
        cannibalization_pct=0.0,
        duration_weeks=1,
    )
    r = calculate_promo_roi(inputs)

    assert r.incremental_profit < 0