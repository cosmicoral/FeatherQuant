# 🪶 FeatherQuant

**A lightweight, cross-asset sentiment-driven market direction predictor.**

FeatherQuant combines LLM-based news sentiment analysis with classical machine learning to estimate short-term market direction across three fundamentally different asset classes — equities, cryptocurrencies, and commodity futures — without relying on deep learning. The project is designed to demonstrate that a *thin, interpretable* ML layer on top of a well-engineered sentiment pipeline can produce meaningful, explainable signals.

> Why "Feather"? The model is intentionally kept light — no LSTMs, no fine-tuned transformers, no black-box price prediction. Every prediction traces back to a specific set of interpretable features and named news drivers.

---

## 🎯 Project Motivation

Most portfolio projects in this space either (a) wrap an LLM summary and call it "AI-powered," or (b) throw a deep learning model at price data and hope it generalizes. FeatherQuant sits deliberately in between: it treats sentiment as a **feature**, not an oracle, and asks a simple, testable question —

> *Does LLM-extracted news sentiment carry predictive signal for short-term direction, and does that signal behave differently across equities, crypto, and commodities?*

This cross-asset comparison is the core analytical contribution of the project — three independently trained, equally lightweight models, benchmarked against each other.

---

## 📊 Asset Coverage (V1)

| Asset Class | Instruments | Rationale |
|---|---|---|
| **US Equities** | 10 NASDAQ-listed stocks | Dense news coverage, clear earnings-driven sentiment spikes |
| **Crypto** | BTC, ETH, 1 stablecoin | 24/7 markets, sentiment sourced from both news and social media |
| **Commodity Futures** | Gold (GC), Crude Oil (CL) | Macro-driven, distinct news structure (Fed policy, OPEC+, inventory reports) |
| **European Equities** *(V1.1)* | Rheinmetall (RHM.DE), BAE Systems (BA.L), ASML (ASML.AS), LVMH (MC.PA), SAP (SAP.DE) | Cross-sector spread (defense, semiconductors, luxury, software) with varying English-language news density — a natural test case for sentiment coverage quality |

*Planned V1.1 extension: 5 European equities (Rheinmetall, BAE Systems, ASML, LVMH, SAP), plus Silver, Natural Gas, Copper (see [Roadmap](#-roadmap)).*

---

## 🏗️ Architecture

```
                     ┌─────────────────────┐
                     │   Market Data APIs   │
                     │  (equities / crypto  │
                     │   / futures prices)  │
                     └──────────┬───────────┘
                                │
┌─────────────────────┐        │        ┌──────────────────────┐
│    News/Data APIs    │◄──────┼───────►│  Macro Data (EIA/FRED)│
│ (per-asset-class)     │      │        │  for futures context  │
└──────────┬───────────┘        │        └──────────────────────┘
           │                    │
           ▼                    ▼
   ┌───────────────────────────────────┐
   │   LLM Sentiment Classification    │
   │   (OpenAI / Gemini)                │
   │   → sentiment score + key drivers  │
   └──────────────────┬─────────────────┘
                       ▼
   ┌───────────────────────────────────┐
   │   Feature Engineering (per class)  │
   │   sentiment, volume Δ, volatility, │
   │   macro deltas, seasonal factors   │
   └──────────────────┬─────────────────┘
                       ▼
   ┌───────────────────────────────────┐
   │   PostgreSQL (sentiment + price    │
   │   + feature store)                 │
   └──────────────────┬─────────────────┘
                       ▼
   ┌───────────────────────────────────┐
   │  3× Lightweight scikit-learn       │
   │  Models (Equities / Crypto /       │
   │  Futures — trained independently)  │
   └──────────────────┬─────────────────┘
                       ▼
   ┌───────────────────────────────────┐
   │        Dashboard (Frontend)        │
   │  sentiment summary · confidence ·  │
   │  predicted direction · key drivers │
   │  · backtest accuracy               │
   └───────────────────────────────────┘
```

---

## 🧠 Modeling Approach

Three separate, independently trained models — **not** one model across all assets — because equities, crypto, and futures respond to fundamentally different drivers, and pooling them dilutes signal.

| Asset Class | Model | Target | Feature Set (examples) |
|---|---|---|---|
| Equities | Logistic Regression | up / down (next 1–3 days) | sentiment score, earnings surprise, volume Δ%, volatility |
| Crypto | Logistic Regression / Random Forest | up / down | sentiment score, social sentiment buzz, on-chain volume, stablecoin flow |
| Futures | Logistic Regression / Random Forest | bullish / neutral / bearish | sentiment score, macro indicator Δ (CPI/PMI), inventory report Δ, seasonality |

Model choice starts with **Logistic Regression as the baseline** for interpretability, with **Random Forest** as a secondary comparison where non-linear relationships (e.g. futures/macro interactions) are suspected. XGBoost/LightGBM are noted as a future extension, not a V1 requirement.

Each model reports:
- Predicted direction + confidence score
- Feature importances / coefficients (the "key drivers" shown on the dashboard)
- Backtested accuracy vs. a naive baseline (e.g. persistence / majority class)

---

## 🛠️ Tech Stack

- **Backend:** Python
- **Data Layer:** PostgreSQL (sentiment + price + feature store)
- **Market Data:** Alpha Vantage / Polygon.io / yfinance (equities), CoinGecko / Binance API (crypto), Alpha Vantage / Nasdaq Data Link (futures)
- **News & Sentiment Sources:** NewsAPI, Finnhub News (equities); CryptoPanic API + social sentiment (crypto); EIA + FRED (futures macro context)
- **LLM Sentiment Engine:** OpenAI GPT-4o / Gemini (structured sentiment classification + driver extraction)
- **ML:** scikit-learn (Logistic Regression, Random Forest)
- **Dashboard:** [React / Vite — to be finalized]
- **Deployment:** [Render / Vercel — to be finalized]

---

## 📈 Dashboard (Planned Views)

- Multi-asset overview: sentiment heatmap across equities / crypto / futures
- Per-asset detail view: sentiment trend, predicted direction, confidence, key news drivers
- Model performance panel: accuracy, precision/recall, comparison across the three asset-class models
- Backtest chart: predicted vs. actual direction over a rolling window

*(Screenshots / demo link to be added once the dashboard is live.)*

---

## 📊 Results

> _To be filled in once V1 training is complete._

| Asset Class | Model | Accuracy | Baseline (naive) |
|---|---|---|---|
| Equities | — | — | — |
| Crypto | — | — | — |
| Futures | — | — | — |

---

## 🗺️ Roadmap

**V1 (current)**
- [ ] Price + news ingestion pipeline for equities, crypto, futures (gold + crude oil)
- [ ] LLM sentiment classification with structured output (score + key drivers)
- [ ] PostgreSQL feature store
- [ ] Three independent scikit-learn baseline models
- [ ] Dashboard with sentiment summary, prediction, confidence, backtest accuracy

**V1.1**
- [ ] Extend equities to 15 tickers: add 5 European stocks (Rheinmetall, BAE Systems, ASML, LVMH, SAP)
- [ ] Extend futures coverage: Silver, Natural Gas, Copper
- [ ] Evaluate non-English news sources for European equities with sparse English coverage (e.g. Rheinmetall, SAP)
- [ ] Model comparison: Logistic Regression vs. Random Forest per asset class

## V2 (Product Evolution)

### User Accounts & Personalization
- [ ] User authentication (Better Auth / Firebase Authentication)
- [ ] Personalized watchlists for stocks, cryptocurrencies, and commodities
- [ ] Save favorite assets and custom watchlist groups
- [ ] Persistent user preferences and dashboard settings

### Portfolio Tracking
- [ ] Manual portfolio tracking (non-broker connected)
- [ ] Portfolio-level sentiment and risk overview
- [ ] Asset allocation visualization
- [ ] Portfolio heatmap and sector exposure summary

### Notifications
- [ ] Sentiment change alerts
- [ ] Confidence threshold notifications
- [ ] Watchlist price & sentiment updates
- [ ] Daily and weekly market digest emails

### Expanded Market Coverage
- [ ] Additional US, European, and Asia-Pacific equities
- [ ] Expanded commodity futures coverage
- [ ] ETF support
- [ ] Major forex pairs (EUR/USD, GBP/USD, USD/JPY)

## **V3 (exploratory, not committed)**
- [ ] XGBoost/LightGBM comparison layer
- [ ] Social media sentiment integration for crypto (Reddit/Twitter)
- [ ] Explore (cautiously) sequence models only if the lightweight baseline shows a clear ceiling
  
### Web3 Extension: On-chain Market Intelligence
- [ ] Add Ethereum / DeFi asset coverage
- [ ] Use the Graph to query on-chain activity from indexed subgraphs
- [ ] Combine on-chain metrics with news sentiment and market price data
- [ ] Build token-level risk and sentiment dashboards
- [ ] Compare off-chain news sentiment with on-chain behavioral signals
### Engineering Improvements
- [ ] Background data ingestion jobs
- [ ] Caching layer (Redis)
- [ ] Scheduled market updates
- [ ] Improved API abstraction and modular data providers
### AI Market Intelligence
- [ ] Personalized daily market briefings
- [ ] Asset-specific AI research summaries
- [ ] Multi-asset comparison reports (e.g. NVIDIA vs AMD, Gold vs Bitcoin)
- [ ] Historical sentiment timeline and trend analysis

**Explicitly out of scope for this project:**
LSTMs/transformer fine-tuning for price prediction, high-frequency trading, complex backtesting frameworks, portfolio optimization. These are high-effort, low-credibility additions for a project whose value proposition is pipeline quality and interpretable signal — not trading performance.

---

## 💡 What This Project Demonstrates

- End-to-end **data pipeline** design across heterogeneous, asynchronous data sources (markets, news, macro data)
- Practical **LLM/NLP application**: structured sentiment extraction with explainable output, not just summarization
- **Applied ML judgment**: choosing an interpretable baseline deliberately over a more "impressive" but less trustworthy deep learning approach
- **Cross-domain financial reasoning**: recognizing that equities, crypto, and futures require different features and different models rather than a one-size-fits-all pipeline
- **Product sense**: a dashboard that communicates confidence and reasoning, not just a raw prediction

---

## ⚠️ Disclaimer

FeatherQuant is a research and portfolio project. It does not constitute financial advice, and predictions should not be used for real trading or investment decisions.

---

## 👤 Author

Built by Coral — an environmental sociology PhD transitioning into software/AI engineering, with a research-driven approach to data-heavy product design.

