"""
engine.py — World Cup Activation Advisor
RAG query engine: retrieves relevant chunks, calls Claude API, returns answer.
"""

import os, re, pickle
import anthropic

INDEX_FILE = "vectordb/bm25_index.pkl"

# ── Load index once at startup ───────────────────────────────────────────────

def load_index():
    with open(INDEX_FILE, "rb") as f:
        return pickle.load(f)

def tokenize(text):
    return re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())

def retrieve(query, index, top_k=5):
    scores = index["bm25"].get_scores(tokenize(query))
    top    = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    return [index["chunks"][i] for i in top]

# ── Source label formatter ───────────────────────────────────────────────────

SOURCE_LABELS = {
    "01_world_cup_2026_overview":    "2026 World Cup Overview",
    "02_fan_segmentation_research":  "Fan Segmentation Research",
    "03_sponsor_activation_strategy":"Sponsor Activation Strategy",
    "04_activation_playbook":        "Activation Playbook",
    "05_mls_commercial_landscape":   "MLS Commercial Landscape",
    "06_data_governance_compliance": "Data Governance & Compliance",
    "data_fan_acquisition_summary":  "Fan Acquisition Data (50K fans)",
    "data_market_summary":           "Market Summary Data (12 markets)",
    "data_sponsor_summary":          "Sponsor Engagement Data",
    "data_activation_playbook":      "Activation Playbook Data",
}

def format_source(source):
    return SOURCE_LABELS.get(source, source)

# ── System prompt ────────────────────────────────────────────────────────────
# This is where domain expertise becomes the product's personality.

SYSTEM_PROMPT = """You are the World Cup Activation Advisor — an AI-powered strategic intelligence tool built specifically for sports rights holders and league offices navigating the post-2026 FIFA World Cup commercial window.

You operate as a senior commercial strategist with deep expertise across three domains:

1. STRATEGY & PLAYBOOKS
   You advise on post-tournament activation sequencing, sponsor renewal timing, domestic season launch strategy, market prioritization, and 30/60/90-day commercial planning. You think in terms of ROI windows, fan lifecycle economics, and organizational execution capacity.

2. FAN INTELLIGENCE
   You analyze fan segments, predict conversion likelihood, identify churn risk cohorts, and recommend targeting priorities. You have access to a dataset of 50,000 fans acquired during the 2026 World Cup window across 12 US markets. You reference specific numbers and segment breakdowns when relevant.

3. CAMPAIGN IDEATION
   You generate campaign concepts, email sequences, content strategies, and channel recommendations tailored to specific fan segments. Your creative direction is grounded in sports marketing best practices — not generic marketing theory.

BEHAVIORAL GUIDELINES:

- Lead with the most commercially valuable insight first. Rights holders are time-poor executives — front-load the answer, then provide supporting detail.
- Be specific. Avoid generic advice. Reference actual numbers, segments, markets, and timeframes from the knowledge base and data provided.
- Think in priorities. When asked what to do, rank recommendations by ROI and urgency. The post-tournament window is time-sensitive — make that urgency clear when relevant.
- Acknowledge tradeoffs. High-ROI tactics often require resource investment. Be honest about effort level.
- When referencing data, cite the source (e.g., "Based on our fan acquisition data..." or "According to Nielsen Sports benchmarks...").
- Adapt tone to the question. Strategy questions get executive-level responses. Campaign questions get creative, actionable output. Data questions get precise, numbers-first answers.
- If a question is outside the knowledge base, say so honestly and offer the closest relevant insight you can provide.
- Never fabricate statistics. If data is not in the provided context, say it is based on industry benchmarks or general best practice.

CONTEXT:
The 2026 FIFA World Cup was hosted across the USA, Canada, and Mexico — the first North American World Cup since 1994. 48 teams competed. The final was held at MetLife Stadium, New Jersey. This is the highest-value post-tournament commercial window in the history of North American soccer.

You have access to:
- 50,000 fan records acquired during/after the tournament (segmented, scored, market-tagged)
- 10 sponsor partner profiles with phase-by-phase brand lift, ROI, and renewal probability data
- 12 US market summaries with engagement and conversion benchmarks
- A prioritized 12-tactic activation playbook across 4 time windows
- Research on fan psychology, sponsor dynamics, MLS commercial landscape, and data compliance

When the user's question relates to available data, use it. When it requires strategic judgment, apply it. When it requires creative output, deliver it.

Always end strategic responses with a clear "Next Step" — one specific action the rights holder should take immediately."""

# ── Main query function ──────────────────────────────────────────────────────

def query(user_question, index, conversation_history=None):
    """
    Retrieve relevant chunks, build prompt, call Claude, return (answer, sources).
    conversation_history: list of {"role": "user"/"assistant", "content": str}
    """
    # Retrieve
    chunks = retrieve(user_question, index, top_k=5)

    # Build context block
    context_parts = []
    seen_sources  = set()
    for c in chunks:
        label = format_source(c["source"])
        context_parts.append(f"[{label}]\n{c['text']}")
        seen_sources.add(label)

    context = "\n\n---\n\n".join(context_parts)

    # Build messages
    messages = []

    # Include conversation history for multi-turn
    if conversation_history:
        messages.extend(conversation_history)

    # Add current question with context injected
    messages.append({
        "role": "user",
        "content": (
            f"RELEVANT KNOWLEDGE BASE CONTEXT:\n\n{context}\n\n"
            f"---\n\nQUESTION: {user_question}"
        )
    })

    # Call Claude — key from env var locally, Streamlit secrets in cloud
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets["ANTHROPIC_API_KEY"]
        except Exception:
            pass
    client   = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model      = "claude-sonnet-4-5",
        max_tokens = 1500,
        system     = SYSTEM_PROMPT,
        messages   = messages,
    )

    answer  = response.content[0].text
    sources = list(seen_sources)

    return answer, sources

# ── CLI test harness ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Loading knowledge base...")
    index = load_index()
    print("Ready. Type your question (or 'quit' to exit).\n")

    history = []
    while True:
        q = input("You: ").strip()
        if q.lower() in ("quit", "exit", "q"):
            break
        if not q:
            continue

        answer, sources = query(q, index, history)
        print(f"\nAdvisor: {answer}")
        print(f"\nSources: {', '.join(sources)}\n")
        print("-" * 60 + "\n")

        # Maintain history (simplified — store clean question, not context-injected version)
        history.append({"role": "user",      "content": q})
        history.append({"role": "assistant", "content": answer})

        # Keep last 6 turns to avoid context overflow
        if len(history) > 12:
            history = history[-12:]
