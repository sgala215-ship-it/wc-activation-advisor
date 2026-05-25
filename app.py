"""
app.py — World Cup Activation Advisor
Streamlit chatbot UI. Run with: python -m streamlit run app.py
"""

import streamlit as st
import pandas as pd
from engine import load_index, query
from brand import GLOBAL_CSS, SIDEBAR_BRAND_HTML, FOOTER_HTML, page_header, source_badges, badge, COLORS

# ── Page config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title = "WC Activation Advisor · Sohil Gala",
    page_icon  = "⚽",
    layout     = "wide",
)

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── Data loaders ─────────────────────────────────────────────────────────────

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
        count   = ("fan_id",                  "count"),
        avg_ltv = ("predicted_ltv_usd",        "mean"),
        avg_eng = ("engagement_score",         "mean"),
        st_conv = ("season_ticket_conversion", "mean"),
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
    st.markdown(SIDEBAR_BRAND_HTML, unsafe_allow_html=True)

    st.markdown('<p class="sg-label">Advisory mode</p>', unsafe_allow_html=True)
    mode = st.radio(
        label            = "mode",
        options          = ["🎯  Strategy & Playbooks", "👥  Fan Intelligence", "📣  Campaign Ideation"],
        index            = 0,
        label_visibility = "collapsed",
    )

    st.divider()
    st.markdown('<p class="sg-label">Live data</p>', unsafe_allow_html=True)

    seg = load_segment_data()
    mdf = load_market_data()
    total_fans = int(seg["count"].sum())
    avg_ltv    = int(seg["avg_ltv"].mean())

    c1, c2 = st.columns(2)
    c1.metric("Fans",     f"{total_fans:,}")
    c2.metric("Markets",  len(mdf))
    c1.metric("Avg LTV",  f"${avg_ltv}")
    c2.metric("Sponsors", "10")

    st.divider()
    st.markdown('<p class="sg-label">Knowledge base</p>', unsafe_allow_html=True)
    for s in ["📋 2026 WC Overview","👥 Fan Segmentation","🤝 Sponsor Strategy",
              "🎯 Activation Playbook","🏟️ MLS Landscape","🔒 Data Governance"]:
        st.markdown(f"<p style='font-size:12px;color:{COLORS['muted']};margin:2px 0'>{s}</p>",
                    unsafe_allow_html=True)

    st.divider()
    st.markdown(FOOTER_HTML, unsafe_allow_html=True)

# ── Main ─────────────────────────────────────────────────────────────────────

st.markdown(
    page_header(
        "Post-World Cup Activation Advisor",
        "Strategic AI for rights holders navigating the 2026 World Cup commercial window"
    ),
    unsafe_allow_html=True
)

# ── Sample questions ──────────────────────────────────────────────────────────

MODE_QUESTIONS = {
    "🎯  Strategy & Playbooks": [
        "We have 90 days post-tournament. What's the highest ROI activation sequence?",
        "What does our 90-day activation calendar look like?",
        "Which sponsor categories are most at risk of not renewing?",
        "How should we prioritize our 30-day plan across markets?",
    ],
    "👥  Fan Intelligence": [
        "Which fan segments should we prioritize and why?",
        "Which markets have the most high-value fans?",
        "How many fans are at high churn risk and how do we intervene?",
        "What's the season ticket conversion rate by segment?",
    ],
    "📣  Campaign Ideation": [
        "What campaigns should I use to activate fans signed up during the watch party we hosted?",
        "Generate a 3-email re-engagement sequence for lapsed fans",
        "Write a season ticket campaign for converted fans",
        "What content strategy works best for new-to-soccer fans?",
    ],
}

st.markdown('<p class="sg-label">Suggested questions</p>', unsafe_allow_html=True)
cols = st.columns(2)
for i, q in enumerate(MODE_QUESTIONS[mode]):
    if cols[i % 2].button(q, key=f"sq_{i}"):
        st.session_state["pending_question"] = q

st.divider()

# ── Data expander ─────────────────────────────────────────────────────────────

with st.expander("📊  View underlying data", expanded=False):
    tab1, tab2, tab3 = st.tabs(["Fan segments", "Markets", "Sponsors"])

    with tab1:
        d = load_segment_data().copy()
        d.columns = ["Segment","Fans","Avg LTV ($)","Avg Engagement","ST Conv %"]
        d["Avg LTV ($)"]  = d["Avg LTV ($)"].apply(lambda x: f"${x:.0f}")
        d["ST Conv %"]    = d["ST Conv %"].apply(lambda x: f"{x:.1f}%")
        st.dataframe(d, hide_index=True, use_container_width=True)

    with tab2:
        m = mdf[["market","total_fans_acquired","avg_predicted_ltv_usd",
                  "pct_email_opted_in","season_ticket_conversion_rate","pct_high_churn_risk"]].copy()
        m.columns = ["Market","Fans","Avg LTV ($)","Email Opt-in %","ST Conv %","High Churn %"]
        st.dataframe(m, hide_index=True, use_container_width=True)

    with tab3:
        s = load_sponsor_data().copy()
        s.columns = ["Sponsor","Category","Tier","Brand Lift %","ROI Multiple","Renewal Prob"]
        s["Renewal Prob"] = s["Renewal Prob"].apply(lambda x: f"{x*100:.0f}%")
        st.dataframe(s, hide_index=True, use_container_width=True)

# ── Chat ──────────────────────────────────────────────────────────────────────

if "messages"         not in st.session_state: st.session_state.messages         = []
if "pending_question" not in st.session_state: st.session_state.pending_question = None

for msg in st.session_state.messages:
    avatar = "⚽" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "sources" in msg:
            st.markdown(source_badges(msg["sources"]), unsafe_allow_html=True)

prompt     = st.session_state.pending_question
st.session_state.pending_question = None
chat_input = st.chat_input("Ask about fan activation, sponsor strategy, campaign ideas, market data...")
if chat_input:
    prompt = chat_input

if prompt:
    mode_context = {
        "🎯  Strategy & Playbooks": "Focus on strategic recommendations and commercial priorities.",
        "👥  Fan Intelligence":     "Focus on data-driven fan insights and segment analysis.",
        "📣  Campaign Ideation":    "Focus on campaign concepts, messaging, and creative direction.",
    }
    enriched = f"[{mode.split('  ', 1)[1]}] {prompt}\n\n{mode_context[mode]}"

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages[:-1]
        if m["role"] in ("user", "assistant")
    ][-10:]

    with st.chat_message("assistant", avatar="⚽"):
        with st.spinner("Analyzing..."):
            answer, sources = query(enriched, index, history)
        st.markdown(answer)
        st.markdown(source_badges(sources), unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})

# ── Empty state ───────────────────────────────────────────────────────────────

if not st.session_state.messages:
    st.markdown(f"""
    <div style='text-align:center; padding:48px 20px;'>
      <div style='font-size:40px; margin-bottom:12px'>⚽</div>
      <p style='font-size:16px; font-weight:500; color:{COLORS["ink"]}; margin:0 0 6px'>Ready to activate</p>
      <p style='font-size:14px; color:{COLORS["muted"]}; margin:0'>
        Select a mode in the sidebar, click a suggested question, or type below.
      </p>
    </div>
    """, unsafe_allow_html=True)
