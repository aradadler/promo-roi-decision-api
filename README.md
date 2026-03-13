# Promo ROI Decision API

A decision intelligence API for evaluating retail promotion profitability under varying pricing, uplift, and cost assumptions — enriched with real-time macroeconomic context (CPI via FRED).

## Problem context

Retail promotion planning often relies on:

- **Spreadsheet-based ROI modeling**
- **Historical promotion heuristics**
- **Static assumptions about uplift and margin**

However, promotions operate within broader macroeconomic conditions that influence:

- **Cost structures**
- **Consumer purchasing power**
- **Price elasticity**
- **Competitive pricing behavior**

This project demonstrates how structured financial modeling and macro context can be combined into a repeatable, API-driven decision system.

## What this system does

Given promotion assumptions (price, discount, uplift, cannibalization, COGS), the API:

- **Computes** baseline revenue and profit
- **Computes** promotional revenue and profit
- **Calculates** incremental profit and ROI
- **Determines** break-even uplift
- **Generates** a recommendation:
  - **GO**
  - **NO-GO**
  - **REVIEW**
- **Enriches** the output with real-time CPI data (FRED)
- **Compares** two promotion scenarios side-by-side to determine the stronger strategy

## Why CPI integration?

Inflation affects:

- **Unit economics** (COGS pressure)
- **Consumer demand sensitivity**
- **Pricing strategy flexibility**
- **ROI thresholds**

While CPI does not yet modify the ROI math directly, the system integrates macro context to support more informed decision-making.

Future enhancements could:

- **Adjust COGS** dynamically based on CPI trends
- **Modify uplift expectations** under inflationary pressure
- **Introduce macro-adjusted ROI thresholds**

This reflects how promotion decisions should evolve from isolated spreadsheet math to macro-aware decision systems.

## Architecture

```text
Client
  ↓
FastAPI layer
  ↓
ROI financial engine
  ↓
Decision logic layer
  ↓
External macro integration (FRED CPI)
  ↓
Structured JSON response
```

## API endpoints

### `POST /simulate`

Returns financial metrics for a single promotion scenario.

### `POST /recommend`

Returns:

- financial metrics
- decision (GO / NO-GO / REVIEW)
- rationale
- macroeconomic context (latest CPI)

### `POST /compare`

Compares two promotion scenarios and returns:

- financial results for **Scenario A**
- financial results for **Scenario B**
- the **better scenario based on incremental profit**
- a short comparison rationale

## Example output

```json
{
  "incremental_profit": 16137.4,
  "roi": 1.617,
  "decision": "GO",
  "rationale": "Promo is profitable and meets the ROI threshold (roi >= 0.20).",
  "market_context": {
    "series": "CPIAUCSL",
    "date": "2026-01-01",
    "value": "326.588"
  }
}
```

## Technical stack

- **Python 3.11**
- **FastAPI**
- **Pydantic**
- **uv** (environment management)
- **Pytest**
- **FRED API integration**

## Running locally

```bash
uv sync
export FRED_API_KEY=YOUR_KEY
uv run uvicorn app.main:app --reload --app-dir src
```

Then open:

`http://127.0.0.1:8000/docs`

## Testing

```bash
uv run pytest -q
```

## Future extensions

- **Inflation-adjusted COGS modeling**
- **Sensitivity analysis endpoint**
- **Elasticity modeling**
- **Monte Carlo simulation**
- **Cloud deployment**

## What this project demonstrates

- **Financial modeling rigor**
- **Decision framework abstraction**
- **API-first architecture**
- **Macro-data integration**
- **Reproducible engineering practices**
- **Product-oriented system thinking**
