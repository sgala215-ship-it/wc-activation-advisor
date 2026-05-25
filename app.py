"""
app.py — World Cup Activation Advisor
Streamlit chatbot UI. Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import os
from engine import load_index, query, format_source

# ── Page config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title = "World Cup Activation Advisor",
    page_icon  = "⚽",
    layout     = "wide",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────

st.markdown("""
<style>
  /* Main background */
  .stApp { background-color: #0a0e1a; }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background-color: #0f1525;
    border-right: 1px solid #1e2d4a;
  }

  /* Chat messages */
  [data-testid="stChatMessage"] {
    background-color: #111827;
    border: 1px solid #1e2d4a;
    border-radius: 12px;
    padding: 4px 8px;
    margin-bottom: 8px;
  }

  /* Source badges */
  .source-badge {
    display: inline-block;
    background-color: #1a2744;
    color: #60a5fa;
    font-size: 11px;
    padding: 3px 10px;
    border-radius: 20px;
    margin: 3px 3px 3px 0;
    border: 1px solid #2563eb33;
  }

  /* Mode buttons */
  .stButton > button {
    background-color: #111827;
    color: #94a3b8;
    border: 1px solid #1e2d4a;
    border-radius: 8px;
    font-size: 13px;
    padding: 6px 12px;
    transition: all 0.2s;
    width: 100%;
    text-align: left;
  }
  .stButton > button:hover {
    background-color: #1a2744;
    color: #60a5fa;
    border-color: #2563eb;
  }

  /* Metric cards */
  [data-testid="stMetric"] {
    background-color: #111827;
    border: 1px solid #1e2d4a;
    border-radius: 10px;
    padding: 12px 16px;
  }

  /* Hide default streamlit footer */
  footer { visibility: hidden; }

  /* Chat input */
  [data-testid="stChatInput"] textarea {
    background-color: #111827 !important;
    border: 1px solid #1e2d4a !important;
    color: #e2e8f0 !important;
    border-radius: 10px !important;
  }

  /* Headers */
  h1, h2, h3 { color: #f1f5f9 !important; }
  p, li { color: #94a3b8; }

  /* Divider */
  hr { border-color: #1e2d4a; }
</style>
""", unsafe_allow_html=True)

# ── Load knowledge base ───────────────────────────────────────────────────────

@st.cache_resource
def get_index():
    return load_index()

@st.cache_data
def load_market_data():
    return pd.read_csv("data/market_summary.csv")

@st.cache_data
def load_segment_data():
    df = pd.read_csv("data/fan_acquisition.csv")
    return df.groupby("segment").agg(
        count=("fan_id","count"),
        avg_ltv=("predicted_ltv_usd","mean"),
        avg_eng=("engagement_score","mean"),
        churn_high=("churn_risk", lambda x: (x=="High").mean()*100),
        st_conv=("season_ticket_conversion","mean"),
    ).round(1).reset_index()

@st.cache_data
def load_sponsor_data():
    df = pd.read_csv("data/sponsor_engagement.csv")
    return df[df["phase"] == "During Tournament"][
        ["sponsor_name","category","tier","brand_lift_pct","roi_multiple","renewal_probability"]
    ].sort_values("roi_multiple", ascending=False)

index = get_index()

# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### ⚽ World Cup\n# Activation Advisor")
    st.markdown("*AI-powered commercial intelligence for rights holders*")
    st.divider()

    # Mode selector
    st.markdown("**Advisory Mode**")
    mode = st.radio(
        label      = "mode",
        options    = ["🎯 Strategy & Playbooks", "👥 Fan Intelligence", "📣 Campaign Ideation"],
        index      = 0,
        label_visibility = "collapsed",
    )
    st.divider()

    # Data snapshot
    st.markdown("**Live Data Snapshot**")

    mdf = load_market_data()
    seg = load_segment_data()

    total_fans = int(seg["count"].sum())
    top_market = mdf.sort_values("total_fans_acquired", ascending=False).iloc[0]["market"]
    avg_ltv    = round(seg["avg_ltv"].mean(), 0)

    col1, col2 = st.columns(2)
    col1.metric("Fans", f"{total_fans:,}")
    col2.metric("Markets", len(mdf))
    col1.metric("Avg LTV", f"${int(avg_ltv)}")
    col2.metric("Sponsors", "10")

    st.divider()
    st.markdown("**Knowledge Base**")
    sources = [
        "📋 2026 WC Overview",
        "👥 Fan Segmentation",
        "🤝 Sponsor Strategy",
        "🎯 Activation Playbook",
        "🏟️ MLS Landscape",
        "🔒 Data Governance",
    ]
    for s in sources:
        st.markdown(f"<small style='color:#4a6080'>{s}</small>", unsafe_allow_html=True)

    st.divider()
    st.markdown(
        "<small style='color:#374151'>Built by <b>Sohil Gala</b> · "
        "VP Strategic Solutions, Two Circles</small>",
        unsafe_allow_html=True
    )

# ── Main area ─────────────────────────────────────────────────────────────────

# Header
st.markdown(
    "<h2 style='margin-bottom:4px'>Post-World Cup Activation Advisor</h2>"
    "<p style='color:#4a6080;margin-top:0'>Strategic AI for rights holders navigating the 2026 World Cup commercial window</p>",
    unsafe_allow_html=True
)

# Mode-specific sample questions
MODE_QUESTIONS = {
    "🎯 Strategy & Playbooks": [
        "We have 90 days post-tournament. What's the highest ROI activation sequence?",
        "What does our 90-day activation calendar look like?",
        "Which sponsor categories are most at risk of not renewing?",
        "How should we prioritize our 30-day plan across markets?",
    ],
    "👥 Fan Intelligence": [
        "Which fan segments should we prioritize and why?",
        "Which markets have the most high-value fans?",
        "How many fans are at high churn risk and how do we intervene?",
        "What's the season ticket conversion rate by segment?",
    ],
    "📣 Campaign Ideation": [
        "What campaigns should I use to activate fans signed up during the watch party we hosted?",
        "Generate a 3-email re-engagement sequence for lapsed fans",
        "Write a season ticket campaign for converted fans",
        "What content strategy works best for new-to-soccer fans?",
    ],
}

# Sample questions as clickable chips
current_mode = mode
st.markdown("**Suggested questions**")
cols = st.columns(2)
for i, q in enumerate(MODE_QUESTIONS[current_mode]):
    if cols[i % 2].button(q, key=f"sq_{i}"):
        st.session_state["pending_question"] = q

st.divider()

# ── Data tabs (collapsible) ───────────────────────────────────────────────────

with st.expander("📊 View underlying data", expanded=False):
    tab1, tab2, tab3 = st.tabs(["Fan Segments", "Markets", "Sponsors"])

    with tab1:
        seg_display = load_segment_data().copy()
        seg_display.columns = ["Segment","Fans","Avg LTV ($)","Avg Engagement","High Churn %","ST Conv %"]
        seg_display["Avg LTV ($)"] = seg_display["Avg LTV ($)"].apply(lambda x: f"${x:.0f}")
        seg_display["High Churn %"] = seg_display["High Churn %"].apply(lambda x: f"{x:.1f}%")
        seg_display["ST Conv %"] = seg_display["ST Conv %"].apply(lambda x: f"{x:.1f}%")
        st.dataframe(seg_display, hide_index=True, use_container_width=True)

    with tab2:
        mdf_display = mdf[["market","total_fans_acquired","avg_predicted_ltv_usd",
                            "pct_email_opted_in","season_ticket_conversion_rate","pct_high_churn_risk"]].copy()
        mdf_display.columns = ["Market","Fans","Avg LTV ($)","Email Opt-in %","ST Conv %","High Churn %"]
        st.dataframe(mdf_display, hide_index=True, use_container_width=True)

    with tab3:
        sp = load_sponsor_data().copy()
        sp.columns = ["Sponsor","Category","Tier","Brand Lift %","ROI Multiple","Renewal Prob"]
        sp["Renewal Prob"] = sp["Renewal Prob"].apply(lambda x: f"{x*100:.0f}%")
        st.dataframe(sp, hide_index=True, use_container_width=True)

# ── Chat interface ─────────────────────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="⚽" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "sources" in msg:
            st.markdown(
                " ".join(f'<span class="source-badge">{s}</span>' for s in msg["sources"]),
                unsafe_allow_html=True
            )

# Handle pending question from button click
prompt = st.session_state.pending_question
st.session_state.pending_question = None

# Chat input
chat_input = st.chat_input(
    placeholder="Ask about fan activation, sponsor strategy, campaign ideas, market data..."
)
if chat_input:
    prompt = chat_input

# Process prompt
if prompt:
    # Add mode context to the question
    mode_context = {
        "🎯 Strategy & Playbooks": "Focus on strategic recommendations and commercial priorities.",
        "👥 Fan Intelligence":      "Focus on data-driven fan insights and segment analysis.",
        "📣 Campaign Ideation":     "Focus on campaign concepts, messaging, and creative direction.",
    }
    enriched_prompt = f"[{current_mode.split(' ', 1)[1]}] {prompt}\n\n{mode_context[current_mode]}"

    # Show user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Build history for multi-turn (exclude sources metadata)
    history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages[:-1]  # exclude the just-added user message
        if m["role"] in ("user", "assistant")
    ][-10:]  # last 5 turns

    # Call engine
    with st.chat_message("assistant", avatar="⚽"):
        with st.spinner("Analyzing..."):
            answer, sources = query(enriched_prompt, index, history)
        st.markdown(answer)
        st.markdown(
            " ".join(f'<span class="source-badge">{s}</span>' for s in sources),
            unsafe_allow_html=True
        )

    st.session_state.messages.append({
        "role":    "assistant",
        "content": answer,
        "sources": sources,
    })

# ── Empty state ───────────────────────────────────────────────────────────────

if not st.session_state.messages:
    st.markdown("""
    <div style='text-align:center; padding:40px 20px; color:#374151'>
        <div style='font-size:48px; margin-bottom:16px'>⚽</div>
        <h3 style='color:#60a5fa'>Ready to activate</h3>
        <p>Ask a question above or select one of the suggested prompts.<br>
        Switch modes in the sidebar to shift between strategy, fan intelligence, and campaign ideation.</p>
    </div>
    """, unsafe_allow_html=True)
