# JalRakshak AI — System Architecture
**Tagline:** "From Water Risk to Early Action."

## Overview
JalRakshak AI is a decision-support and early-warning platform for public health officials. It integrates community health data, rainfall/environmental indicators, ground water quality measurements, and historical patterns to calculate a community-level water-borne disease risk indicator.

## System Topology

```
                  ┌──────────────────────────────────────────────┐
                  │            REACT DASHBOARD UI                │
                  │   Vite + React.js + Tailwind + Recharts      │
                  └──────────────────────┬───────────────────────┘
                                         │ REST API (JSON)
                                         ▼
                  ┌──────────────────────────────────────────────┐
                  │             FLASK REST API                   │
                  │         backend/app.py (Port 5000)           │
                  └──────┬───────────────────────┬───────────────┘
                         │                       │
                         ▼                       ▼
      ┌───────────────────────────┐    ┌───────────────────────────┐
      │     SQLITE DATABASE       │    │     ML MODEL ENGINE       │
      │   database/jalrakshak.db  │    │ Random Forest + IsoForest │
      └───────────────────────────┘    └───────────────────────────┘
                         ▲                       ▲
                         │                       │
      ┌──────────────────┴───────────────────────┴───────────────┐
      │             DATA ENGINEERING PIPELINE                     │
      │  scripts/01_profile -> 02_clean -> 03_geo -> 04_integrate  │
      └──────────────────────────────────────────────────────────┘
```

## Security & Scoping
- Environment configurations managed via `.env` / `.env.example`.
- All outputs explicitly state decision-support disclaimer.
- Strict non-fabrication guarantee separating Real Public Source datasets from Synthetic Demo datasets.
