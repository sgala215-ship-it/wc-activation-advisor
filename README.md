# ⚽ World Cup Activation Advisor

> AI-powered commercial intelligence for sports rights holders navigating the post-2026 FIFA World Cup window.

Built by **Sohil Gala** — VP Strategic Solutions, Two Circles | Enterprise Data & AI Executive

---

## What it does

A RAG-powered chatbot that advises rights holders and league offices across three commercial domains:

| Mode | What it answers |
|------|----------------|
| 🎯 Strategy & Playbooks | 30/60/90-day activation sequencing, sponsor renewal timing, market prioritization |
| 👥 Fan Intelligence | Segment analysis, churn prediction, LTV scoring, market breakdowns |
| 📣 Campaign Ideation | Email sequences, content strategies, channel recommendations by segment |

---

## Architecture

```
Knowledge Base (6 docs + 4 CSV summaries)
        ↓
   BM25 Retrieval (rank-bm25)
        ↓
   Context injection
        ↓
   Claude Sonnet (Anthropic API)
        ↓
   Streamlit UI
```

**Why BM25?** For a well-structured domain knowledge base, BM25 keyword retrieval is fast, transparent, and requires zero external dependencies. Production version would use vector embeddings for semantic search.

---

## Data

- **50,000 fan records** — acquired during/after the 2026 World Cup, segmented and scored
- **10 sponsor profiles** — brand lift, ROI, and renewal probability across 5 tournament phases
- **12 US market summaries** — engagement, LTV, and churn benchmarks by host city
- **12-tactic activation playbook** — prioritized across 4 time windows with ROI estimates

All data is synthetic/dummy, generated to mirror real sports industry benchmarks.

---

## Setup

### 1. Clone and install
```bash
git clone https://github.com/yourusername/wc-activation-advisor
cd wc-activation-advisor
pip install -r requirements.txt
```

### 2. Set your Anthropic API key
```bash
export ANTHROPIC_API_KEY=your_key_here
```
Get a key at [console.anthropic.com](https://console.anthropic.com)

### 3. Generate data and build index
```bash
python generate_data.py
python ingest.py
```

### 4. Run the app
```bash
streamlit run app.py
```

---

## Deploying to Streamlit Community Cloud (free)

1. Push this repo to GitHub (public)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Add `ANTHROPIC_API_KEY` as a secret in the Streamlit dashboard
5. Deploy — you get a public shareable URL

---

## Project structure

```
wc-activation-advisor/
├── app.py                  # Streamlit UI
├── engine.py               # RAG query engine + system prompt
├── ingest.py               # Document chunking + BM25 indexing
├── generate_data.py        # Synthetic data generator
├── requirements.txt
├── docs/                   # Knowledge base documents
│   ├── 01_world_cup_2026_overview.txt
│   ├── 02_fan_segmentation_research.txt
│   ├── 03_sponsor_activation_strategy.txt
│   ├── 04_activation_playbook.txt
│   ├── 05_mls_commercial_landscape.txt
│   └── 06_data_governance_compliance.txt
├── data/                   # Synthetic datasets
│   ├── fan_acquisition.csv
│   ├── sponsor_engagement.csv
│   ├── crm_engagement.csv
│   ├── activation_playbook.csv
│   └── market_summary.csv
└── vectordb/
    └── bm25_index.pkl      # Pre-built search index
```

---

## Sample questions

**Strategy**
- *"We have 90 days post-tournament. What's the highest ROI activation sequence?"*
- *"Which sponsor categories are most at risk of not renewing?"*

**Fan Intelligence**
- *"Which fan segments should we prioritize and why?"*
- *"Which markets have the most high-value fans?"*

**Campaign Ideation**
- *"Generate a 3-email re-engagement sequence for lapsed fans"*
- *"Write a season ticket campaign for converted fans in New York"*

---

## What this would look like with real client data

This demo uses synthetic data to illustrate the capability. In a real deployment for a rights holder:

- Fan acquisition data comes from their CRM / CDP (Salesforce, HubSpot, etc.)
- Sponsor data comes from brand tracking tools (Nielsen, Kantar)
- The knowledge base is augmented with proprietary strategy frameworks and client-specific context
- The system prompt is tuned to the specific rights holder's commercial priorities
- Vector embeddings replace BM25 for semantic search across larger document sets

---

*This project was built to demonstrate AI integration capability for sports rights holders. It reflects real activation frameworks developed through 8+ years of work with UEFA, NFL, Premier League clubs, and global entertainment brands.*
