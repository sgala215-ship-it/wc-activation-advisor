"""
engine.py — World Cup Activation Advisor
RAG query engine: retrieves relevant chunks, calls Claude API, returns answer.
"""

import os, re, pickle
import anthropic

INDEX_FILE = "vectordb/bm25_index.pkl"

def load_index():
    with open(INDEX_FILE, "rb") as f:
        return pickle.load(f)

def tokenize(text):
    return re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())

def retrieve(query, index, top_k=5):
    scores = index["bm25"].get_scores(tokenize(query))
    top    = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    return [index["chunks"][i] for i in top]

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

BASE_SYSTEM_PROMPT = """You are the World Cup Activation Advisor — an AI-powered strategic intelligence tool built for sports organizations navigating the post-2026 FIFA World Cup commercial window.

You operate as a senior commercial strategist with deep expertise across three domains:

1. STRATEGY & PLAYBOOKS
   Activation sequencing, sponsor renewal timing, domestic season launch strategy, market prioritization, and 30/60/90-day commercial planning. You think in terms of ROI windows, fan lifecycle economics, and organizational execution capacity.

2. FAN INTELLIGENCE
   Fan segment analysis, conversion likelihood, churn risk identification, and targeting priorities. You have access to fan data acquired during the 2026 World Cup window across 12 US markets. Reference specific numbers and segment breakdowns when relevant.

3. CAMPAIGN IDEATION
   Campaign concepts, email sequences, content strategies, and channel recommendations tailored to specific fan segments. Grounded in sports marketing best practices, not generic theory.

BEHAVIORAL GUIDELINES:
- Lead with the most commercially valuable insight first
- Be specific — reference actual numbers, segments, markets, and timeframes
- Rank recommendations by ROI and urgency
- Acknowledge tradeoffs honestly (high ROI often means higher resource investment)
- Cite your data source when referencing specific figures
- Adapt to the organization's role — club advice differs from league office advice
- Never fabricate statistics; if data isn't in context, say it's based on industry benchmarks
- Always end strategic responses with a clear "Next Step" — one specific action to take immediately

CONTEXT:
The 2026 FIFA World Cup was hosted across the USA, Canada, and Mexico. 48 teams competed. The final was held at MetLife Stadium, New Jersey. This is the highest-value post-tournament commercial window in North American soccer history.

You have access to:
- 50,000 fan records acquired during/after the tournament (segmented, scored, market-tagged)
- 10 sponsor partner profiles with phase-by-phase brand lift, ROI, and renewal probability
- 12 US market summaries with engagement and conversion benchmarks
- A prioritized 12-tactic activation playbook across 4 time windows
- Research on fan psychology, sponsor dynamics, MLS commercial landscape, and data compliance"""


def query(user_question, index, conversation_history=None, role_context="", market_filter=None, market_data_snippet=""):
    """
    Retrieve relevant chunks, build prompt, call Claude, return (answer, sources).
    role_context: string describing the org type and team
    market_filter: specific market name to focus on, or None for all
    market_data_snippet: pre-filtered data summary for this market/team
    """
    chunks  = retrieve(user_question, index, top_k=5)
    context_parts = []
    seen_sources  = set()
    for c in chunks:
        label = format_source(c["source"])
        context_parts.append(f"[{label}]\n{c['text']}")
        seen_sources.add(label)
    context = "\n\n---\n\n".join(context_parts)

    # Build full system prompt — base + role addendum
    system = BASE_SYSTEM_PROMPT
    if role_context:
        system += f"\n\n{role_context}"

    messages = []
    if conversation_history:
        messages.extend(conversation_history)

    # Build user message with context
    market_section = ""
    if market_data_snippet:
        market_section = f"\nORGANIZATION-SPECIFIC DATA:\n{market_data_snippet}\n\n---\n\n"

    messages.append({
        "role": "user",
        "content": (
            f"RELEVANT KNOWLEDGE BASE CONTEXT:\n\n{context}\n\n"
            f"---\n\n{market_section}"
            f"QUESTION: {user_question}"
        )
    })

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
        system     = system,
        messages   = messages,
    )

    answer  = response.content[0].text
    sources = list(seen_sources)
    return answer, sources


if __name__ == "__main__":
    print("Loading knowledge base...")
    index = load_index()
    print("Ready.\n")
    history = []
    while True:
        q = input("You: ").strip()
        if q.lower() in ("quit","exit","q"):
            break
        if not q:
            continue
        answer, sources = query(q, index, history)
        print(f"\nAdvisor: {answer}\nSources: {', '.join(sources)}\n" + "-"*60 + "\n")
        history.append({"role":"user","content":q})
        history.append({"role":"assistant","content":answer})
        if len(history) > 12:
            history = history[-12:]
