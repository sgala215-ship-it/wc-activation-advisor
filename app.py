"""
app.py — World Cup Activation Advisor
Streamlit chatbot UI. Run with: python -m streamlit run app.py
"""

import streamlit as st
import pandas as pd
from engine import load_index, query
from brand import GLOBAL_CSS, SIDEBAR_BRAND_HTML, FOOTER_HTML, page_header, source_badges, COLORS
from roles import ROLES, get_role_config, get_market_for_team, build_role_context

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title = "WC Activation Advisor · Sohil Gala",
    page_icon  = "⚽",
    layout     = "wide",
)
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── Extra mobile CSS ──────────────────────────────────────────────────────────

st.markdown("""
<style>
  /* Role/team selector cards */
  .selector-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 16px;
  }
  @media (max-width: 640px) {
    .selector-grid { grid-template-columns: 1fr; }
  }

  /* Stat strip */
  .stat-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin-bottom: 16px;
  }
  @media (max-width: 640px) {
    .stat-strip { grid-template-columns: repeat(2, 1fr); }
  }
  .stat-pill {
    background: #fff;
    border: 0.5px solid #E5E7EB;
    border-radius: 10px;
    padding: 10px 14px;
  }
  .stat-pill-label { font-size: 11px; color: #6B7280; margin: 0 0 2px; }
  .stat-pill-value { font-size: 18px; font-weight: 500; color: #111827; margin: 0; }

  /* Mode tabs on mobile */
  .mode-tabs {
    display: flex;
    gap: 6px;
    margin-bottom: 16px;
    overflow-x: auto;
    padding-bottom: 2px;
  }
  .mode-tab {
    flex-shrink: 0;
    font-size: 13px;
    padding: 6px 14px;
    border-radius: 20px;
    border: 0.5px solid #E5E7EB;
    background: #fff;
    color: #374151;
    cursor: pointer;
    white-space: nowrap;
  }
  .mode-tab.active {
    background: #EAF3DE;
    color: #0F6E56;
    border-color: #1D9E75;
    font-weight: 500;
  }

  /* Start over button — subtle, not primary */
  [data-testid="stButton"] button[kind="secondary"] {
    background: transparent;
    color: #6B7280;
    border: 0.5px solid #E5E7EB;
    font-size: 12px;
    padding: 4px 12px;
    min-height: 32px;
    width: auto !important;
  }
  [data-testid="stButton"] button[kind="secondary"]:hover {
    background: #FEE2E2;
    color: #991B1B;
    border-color: #FCA5A5;
  }

  /* Question chips */
  .stButton > button {
    white-space: normal !important;
    text-align: left !important;
    height: auto !important;
    min-height: 44px;
    line-height: 1.4;
  }
</style>
""", unsafe_allow_html=True)

# ── Data loaders ──────────────────────────────────────────────────────────────

@st.cache_resource
def get_index():
    return load_index()

@st.cache_data
def load_fans():
    return pd.read_csv("data/fan_acquisition.csv")

@st.cache_data
def load_market_data():
    return pd.read_csv("data/market_summary.csv")

@st.cache_data
def load_sponsor_data():
    df = pd.read_csv("data/sponsor_engagement.csv")
    return df[df["phase"] == "During Tournament"][
        ["sponsor_name","category","tier","brand_lift_pct","roi_multiple","renewal_probability"]
    ].sort_values("roi_multiple", ascending=False)

def segment_summary(df):
    return df.groupby("segment").agg(
        count   = ("fan_id",                  "count"),
        avg_ltv = ("predicted_ltv_usd",        "mean"),
        avg_eng = ("engagement_score",         "mean"),
        st_conv = ("season_ticket_conversion", "mean"),
    ).round(1).reset_index()

def build_market_snippet(df_filtered, market, team):
    n = len(df_filtered)
    if n == 0:
        return ""
    seg   = segment_summary(df_filtered)
    churn = df_filtered["churn_risk"].value_counts(normalize=True).mul(100).round(1)
    top_ch = df_filtered["acquisition_channel"].value_counts().head(3)
    lines = [f"Data for {team} ({market} market) — {n:,} fans acquired during 2026 World Cup:\n"]
    lines.append("SEGMENT BREAKDOWN:")
    for _, row in seg.iterrows():
        lines.append(
            f"  {row['segment']}: {int(row['count']):,} fans "
            f"(avg LTV ${row['avg_ltv']:.0f}, "
            f"season ticket conversion {row['st_conv']*100:.1f}%, "
            f"avg engagement {row['avg_eng']:.1f}/100)"
        )
    lines.append(f"\nCHURN RISK: " + ", ".join(f"{k}: {v}%" for k,v in churn.items()))
    lines.append(f"\nTOP CHANNELS: " + ", ".join(f"{k}: {v:,}" for k,v in top_ch.items()))
    lines.append(f"\nAvg LTV: ${df_filtered['predicted_ltv_usd'].mean():.0f}")
    lines.append(f"Email opt-in: {df_filtered['email_opt_in'].mean()*100:.1f}%")
    lines.append(f"App download: {df_filtered['app_downloaded'].mean()*100:.1f}%")
    return "\n".join(lines)

index    = get_index()
all_fans = load_fans()

# ── Session state ─────────────────────────────────────────────────────────────

if "messages"         not in st.session_state: st.session_state.messages         = []
if "pending_question" not in st.session_state: st.session_state.pending_question = None
if "btn_counter"       not in st.session_state: st.session_state.btn_counter       = 0
if "last_role"        not in st.session_state: st.session_state.last_role        = None
if "last_team"        not in st.session_state: st.session_state.last_team        = None

# ── Sidebar (desktop) ─────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown(SIDEBAR_BRAND_HTML, unsafe_allow_html=True)
    st.markdown('<p class="sg-label">Knowledge base</p>', unsafe_allow_html=True)
    for s in ["📋 2026 WC Overview","👥 Fan Segmentation","🤝 Sponsor Strategy",
              "🎯 Activation Playbook","🏟️ MLS Landscape","🔒 Data Governance"]:
        st.markdown(
            f"<p style='font-size:12px;color:{COLORS['muted']};margin:2px 0'>{s}</p>",
            unsafe_allow_html=True
        )
    st.divider()
    st.markdown(FOOTER_HTML, unsafe_allow_html=True)

# ── Main page ─────────────────────────────────────────────────────────────────

# Header
st.markdown(
    page_header(
        "Post-World Cup Activation Advisor",
        "Strategic AI for rights holders navigating the 2026 World Cup commercial window"
    ),
    unsafe_allow_html=True
)

# ── Onboarding instructions ───────────────────────────────────────────────────

st.markdown("""
<style>
  .onboard-wrap { max-width: 900px; margin: 8px auto 4px; }
  .onboard-steps {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 10px;
  }
  @media (max-width: 640px) { .onboard-steps { grid-template-columns: 1fr; } }
  .onboard-step {
    background: #fff;
    border: 0.5px solid #E5E7EB;
    border-radius: 12px;
    padding: 14px 16px;
  }
  .onboard-step-num {
    width: 22px; height: 22px;
    background: #EAF3DE; color: #0F6E56;
    border-radius: 50%; font-size: 11px; font-weight: 600;
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 8px;
  }
  .onboard-step-title { font-size: 13px; font-weight: 500; color: #111827; margin: 0 0 3px; }
  .onboard-step-desc  { font-size: 12px; color: #6B7280; margin: 0; line-height: 1.5; }
  .onboard-modes {
    background: #fff; border: 0.5px solid #E5E7EB;
    border-radius: 12px; padding: 14px 18px; margin-bottom: 10px;
  }
  .onboard-modes-title {
    font-size: 11px; font-weight: 500; color: #6B7280;
    text-transform: uppercase; letter-spacing: 0.06em; margin: 0 0 10px;
  }
  .mode-row {
    display: flex; align-items: flex-start; gap: 12px;
    padding: 7px 0; border-bottom: 0.5px solid #F3F4F6;
  }
  .mode-row:last-child { border-bottom: none; padding-bottom: 0; }
  .mode-icon { font-size: 16px; flex-shrink: 0; width: 24px; text-align: center; margin-top: 1px; }
  .mode-info-title { font-size: 13px; font-weight: 500; color: #111827; margin: 0 0 1px; }
  .mode-info-desc  { font-size: 12px; color: #6B7280; margin: 0; line-height: 1.4; }
  .onboard-tip {
    background: #EAF3DE; border: 0.5px solid #1D9E7533;
    border-radius: 10px; padding: 10px 14px;
    display: flex; align-items: flex-start; gap: 10px; margin-bottom: 4px;
  }
  .onboard-tip-icon { font-size: 14px; flex-shrink: 0; margin-top: 2px; }
  .onboard-tip-text { font-size: 12px; color: #0F6E56; margin: 0; line-height: 1.5; }
</style>
<div class="onboard-wrap">
  <div class="onboard-steps">
    <div class="onboard-step">
      <div class="onboard-step-num">1</div>
      <p class="onboard-step-title">Select your organization</p>
      <p class="onboard-step-desc">Choose your org type and team below. Data and advice are filtered to your specific market and role.</p>
    </div>
    <div class="onboard-step">
      <div class="onboard-step-num">2</div>
      <p class="onboard-step-title">Pick an advisory mode</p>
      <p class="onboard-step-desc">Strategy, Fan Intelligence, or Campaign Ideation — each surfaces different insights for your context.</p>
    </div>
    <div class="onboard-step">
      <div class="onboard-step-num">3</div>
      <p class="onboard-step-title">Ask a question</p>
      <p class="onboard-step-desc">Click a suggested question or type your own. The advisor uses your fan data and activation research to respond.</p>
    </div>
  </div>
  <div class="onboard-modes">
    <p class="onboard-modes-title">What each mode does</p>
    <div class="mode-row">
      <div class="mode-icon">🎯</div>
      <div>
        <p class="mode-info-title">Strategy &amp; Playbooks</p>
        <p class="mode-info-desc">30/60/90-day activation sequencing, sponsor renewal timing, and market prioritization.</p>
      </div>
    </div>
    <div class="mode-row">
      <div class="mode-icon">👥</div>
      <div>
        <p class="mode-info-title">Fan Intelligence</p>
        <p class="mode-info-desc">Segment breakdowns, churn risk, LTV scoring — filtered to your team's market.</p>
      </div>
    </div>
    <div class="mode-row">
      <div class="mode-icon">📣</div>
      <div>
        <p class="mode-info-title">Campaign Ideation</p>
        <p class="mode-info-desc">Email sequences, content strategies, and campaign concepts for specific fan segments.</p>
      </div>
    </div>
  </div>
  <div class="onboard-tip">
    <div class="onboard-tip-icon">💡</div>
    <p class="onboard-tip-text">
      <strong>Recommended workflow:</strong> Start with Strategy to get your 90-day plan → switch to Fan Intelligence to prioritize segments → use Campaign Ideation to generate the actual content.
    </p>
  </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Role + Team selectors ─────────────────────────────────────────────────────

st.markdown('<p class="sg-label">Your organization</p>', unsafe_allow_html=True)


col_role, col_team = st.columns(2)

with col_role:
    role_label = st.selectbox(
        label = "Organization type",
        options = list(ROLES.keys()),
        index = 0,
    )

role_config = get_role_config(role_label)

with col_team:
    team_name = st.selectbox(
        label = "Your team",
        options = role_config["teams"],
        index = 0,
        help = "Select a region to filter fan data and tailor advice to that market. League and sponsor roles see all markets combined.",
    )

# Clear chat on role/team change
if st.session_state.last_role != role_label or st.session_state.last_team != team_name:
    st.session_state.messages = []
    st.session_state.last_role = role_label
    st.session_state.last_team = team_name

# Resolve market + filter data
market  = get_market_for_team(role_config, team_name)
df_team = all_fans[all_fans["market"] == market] if market else all_fans

# ── Data snapshot strip ───────────────────────────────────────────────────────

n_fans         = len(df_team)
avg_ltv        = int(df_team["predicted_ltv_usd"].mean())
high_churn_pct = int((df_team["churn_risk"] == "High").mean() * 100)
email_opt      = int(df_team["email_opt_in"].mean() * 100)
scope_label    = f"{market} market" if market else "All markets"

st.markdown(f"""
<div class="stat-strip">
  <div class="stat-pill">
    <p class="stat-pill-label">Fans acquired</p>
    <p class="stat-pill-value">{n_fans:,}</p>
  </div>
  <div class="stat-pill">
    <p class="stat-pill-label">Avg LTV</p>
    <p class="stat-pill-value">${avg_ltv}</p>
  </div>
  <div class="stat-pill">
    <p class="stat-pill-label">High churn</p>
    <p class="stat-pill-value">{high_churn_pct}%</p>
  </div>
  <div class="stat-pill">
    <p class="stat-pill-label">Email opt-in</p>
    <p class="stat-pill-value">{email_opt}%</p>
  </div>
</div>
<p style='font-size:12px;color:{COLORS["muted"]};margin:-8px 0 16px'>
  📍 {team_name} · {scope_label}
</p>
""", unsafe_allow_html=True)

st.divider()

# ── Advisory mode ─────────────────────────────────────────────────────────────

st.markdown('<p class="sg-label">Advisory mode</p>', unsafe_allow_html=True)
mode = st.radio(
    label            = "mode",
    options          = list(role_config["questions"].keys()),
    index            = 0,
    horizontal       = True,
    label_visibility = "collapsed",
)

# ── Sample questions ──────────────────────────────────────────────────────────

st.markdown('<p class="sg-label" style="margin-top:12px">Suggested questions</p>',
            unsafe_allow_html=True)
cols = st.columns(2)
for i, q in enumerate(role_config["questions"][mode]):
    if cols[i % 2].button(q, key=f"sq_{i}_{role_label}_{team_name}_{mode}_{st.session_state.btn_counter}"):
        st.session_state["pending_question"] = q
        st.session_state.btn_counter += 1

# ── Start over button ────────────────────────────────────────────────────────

if st.session_state.messages:
    if st.button("↩  Start over", key="reset_chat"):
        st.session_state.messages = []
        st.session_state.pending_question = None
        st.rerun()

st.divider()

# ── Data expander ─────────────────────────────────────────────────────────────

with st.expander(f"📊  {team_name} fan data", expanded=False):
    tab1, tab2, tab3 = st.tabs(["Fan segments", "Churn risk", "Acquisition channels"])

    with tab1:
        seg = segment_summary(df_team).copy()
        seg.columns = ["Segment","Fans","Avg LTV ($)","Avg Engagement","ST Conv %"]
        seg["Avg LTV ($)"] = seg["Avg LTV ($)"].apply(lambda x: f"${x:.0f}")
        seg["ST Conv %"]   = seg["ST Conv %"].apply(lambda x: f"{x:.1f}%")
        st.dataframe(seg, hide_index=True, width='stretch')

    with tab2:
        churn_df = df_team["churn_risk"].value_counts().reset_index()
        churn_df.columns = ["Churn Risk","Fan Count"]
        churn_df["% of Total"] = (churn_df["Fan Count"] / len(df_team) * 100).round(1).astype(str) + "%"
        st.dataframe(churn_df, hide_index=True, width='stretch')

    with tab3:
        ch_df = df_team["acquisition_channel"].value_counts().reset_index()
        ch_df.columns = ["Channel","Fans"]
        ch_df["Avg LTV ($)"] = ch_df["Channel"].map(
            df_team.groupby("acquisition_channel")["predicted_ltv_usd"]
            .mean().round(0).astype(int).apply(lambda x: f"${x}")
        )
        st.dataframe(ch_df, hide_index=True, width='stretch')

# ── Chat ──────────────────────────────────────────────────────────────────────

role_ctx       = role_config["system_addendum"]
role_ctx      += "\n\n" + build_role_context(role_config, team_name, market)
market_snippet = build_market_snippet(df_team, market or "All markets", team_name)

# Chat input at top of chat section — prevents page from scrolling to bottom on load
prompt     = st.session_state.pending_question
st.session_state.pending_question = None
chat_input = st.chat_input(f"Ask about {team_name} fan activation, campaigns, or strategy...")
if chat_input:
    prompt = chat_input

# Render chat history below the input
for msg in st.session_state.messages:
    avatar = "⚽" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "sources" in msg:
            st.markdown(source_badges(msg["sources"]), unsafe_allow_html=True)

if prompt:
    mode_context = {
        k: f"Focus: {k.split('  ', 1)[1]}"
        for k in role_config["questions"].keys()
    }
    enriched = f"[{mode.split('  ', 1)[1]}] {prompt}\n\n{mode_context.get(mode,'')}"

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages[:-1]
        if m["role"] in ("user","assistant")
    ][-10:]

    with st.chat_message("assistant", avatar="⚽"):
        with st.spinner(f"Analyzing {team_name} data..."):
            answer, sources = query(
                enriched, index, history,
                role_context        = role_ctx,
                market_filter       = market,
                market_data_snippet = market_snippet,
            )
        st.markdown(answer)
        st.markdown(source_badges(sources), unsafe_allow_html=True)

    st.session_state.messages.append({
        "role": "assistant", "content": answer, "sources": sources
    })

# ── Empty state / onboarding ──────────────────────────────────────────────────

