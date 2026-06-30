# AI Opportunity Identifier — Enterprise Process Assessment

**Evaluates enterprise business processes for AI automation potential, recommends implementation approaches, estimates impact, and generates phased roadmaps.**

> Built as a portfolio project by Hammad Mirza — June 2026

---

## Overview

Enterprise IT teams need a structured way to assess which business processes are strong candidates for AI automation and which are not. This tool provides that framework — scoring processes based on their characteristics, classifying the AI opportunity type, recommending specific technology approaches, and estimating ROI.

## What It Does

Input a business process and the tool outputs:

- **AI Opportunity Score** — 0-100 based on automation level, frequency, volume, time investment, and pain points
- **AI Classification** — Full Automation, AI-Assisted Decision Support, Intelligent Triage, or Monitor & Optimize
- **Recommended AI Approach** — specific technology recommendation with Copilot/agent interaction model
- **Impact Estimate** — annual hours saved, cost savings, and ROI timeline
- **Implementation Complexity** — Low / Medium / High with description
- **Risk Flags** — dynamically generated based on compliance, data quality, and process characteristics
- **Implementation Roadmap** — phased approach with timeline estimates

## Pre-Built Scenarios

Five dealer operations scenarios are included for demonstration:

- Warranty Claims Triage
- Dealer Onboarding Documentation
- Parts Order Forecasting
- Customer Complaint Routing
- F&I Document Verification

## Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Tech Stack

- **Python 3.10+**
- **Streamlit** — Interactive dashboard
- **Plotly** — Gauge and visualizations

## Disclaimer

This is an independent portfolio project. All scenarios and estimates are illustrative. Not affiliated with or endorsed by any organization.

---

**Author:** Hammad Mirza
**Date:** June 2026
