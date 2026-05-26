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
    """Build a data summary string for the selected team's market."""
    n = len(df_filtered)
    if n == 0:
        return ""
    seg = segment_summary(df_filtered)
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
    lines.append(f"\nTOP ACQUISITION CHANNELS: " + ", ".join(f"{k}: {v:,}" for k,v in top_ch.items()))
    lines.append(f"\nAvg predicted LTV across all fans: ${df_filtered['predicted_ltv_usd'].mean():.0f}")
    lines.append(f"Email opt-in rate: {df_filtered['email_opt_in'].mean()*100:.1f}%")
    lines.append(f"App download rate: {df_filtered['app_downloaded'].mean()*100:.1f}%")
    return "\n".join(lines)

index    = get_index()
all_fans = load_fans()

# ── Session state init ────────────────────────────────────────────────────────

if "messages"         not in st.session_state: st.session_state.messages         = []
if "pending_question" not in st.session_state: st.session_state.pending_question = None
if "last_role"        not in st.session_state: st.session_state.last_role        = None
if "last_team"        not in st.session_state: st.session_state.last_team        = None

# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown(SIDEBAR_BRAND_HTML, unsafe_allow_html=True)

    # ── Role selector
    st.markdown('<p class="sg-label">Your organization type</p>', unsafe_allow_html=True)
    role_label = st.selectbox(
        label            = "role",
        options          = list(ROLES.keys()),
        index            = 0,
        label_visibility = "collapsed",
    )
    role_config = get_role_config(role_label)

    # ── Team selector
    st.markdown('<p class="sg-label" style="margin-top:12px">Your team</p>', unsafe_allow_html=True)
    team_name = st.selectbox(
        label            = "team",
        options          = role_config["teams"],
        index            = 0,
        label_visibility = "collapsed",
    )

    # Clear chat if role or team changes
    if st.session_state.last_role != role_label or st.session_state.last_team != team_name:
        st.session_state.messages = []
        st.session_state.last_role = role_label
        st.session_state.last_team = team_name

    # Resolve market
    market = get_market_for_team(role_config, team_name)

    # Filter fan data
    if market:
        df_team = all_fans[all_fans["market"] == market]
    else:
        df_team = all_fans  # league office sees all

    st.divider()

    # ── Advisory mode
    st.markdown('<p class="sg-label">Advisory mode</p>', unsafe_allow_html=True)
    mode = st.radio(
        label            = "mode",
        options          = list(role_config["questions"].keys()),
        index            = 0,
        label_visibility = "collapsed",
    )

    st.divider()

    # ── Live data snapshot for selected team
    st.markdown('<p class="sg-label">Your data snapshot</p>', unsafe_allow_html=True)
    n_fans  = len(df_team)
    avg_ltv = int(df_team["predicted_ltv_usd"].mean())
    high_churn_pct = int((df_team["churn_risk"] == "High").mean() * 100)
    email_opt = int(df_team["email_opt_in"].mean() * 100)

    c1, c2 = st.columns(2)
    c1.metric("Fans",        f"{n_fans:,}")
    c2.metric("Avg LTV",     f"${avg_ltv}")
    c1.metric("High churn",  f"{high_churn_pct}%")
    c2.metric("Email opt-in",f"{email_opt}%")

    if market:
        st.markdown(
            f"<p style='font-size:11px;color:{COLORS['muted']};margin:6px 0 0'>📍 {market} market</p>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<p style='font-size:11px;color:{COLORS['muted']};margin:6px 0 0'>🌎 All markets</p>",
            unsafe_allow_html=True
        )

    st.divider()
    st.markdown(FOOTER_HTML, unsafe_allow_html=True)

# ── Main area ─────────────────────────────────────────────────────────────────

scope_label = f"{team_name} · {market} market" if market else f"{team_name} · All markets"

st.markdown(
    page_header(
        "Post-World Cup Activation Advisor",
        f"Advising {scope_label} · 2026 World Cup commercial window"
    ),
    unsafe_allow_html=True
)

# ── Sample questions ──────────────────────────────────────────────────────────

st.markdown('<p class="sg-label">Suggested questions</p>', unsafe_allow_html=True)
cols = st.columns(2)
for i, q in enumerate(role_config["questions"][mode]):
    if cols[i % 2].button(q, key=f"sq_{i}_{role_label}_{team_name}"):
        st.session_state["pending_question"] = q

st.divider()

# ── Data expander ─────────────────────────────────────────────────────────────

with st.expander(f"📊  {team_name} fan data", expanded=False):
    tab1, tab2, tab3 = st.tabs(["Fan segments", "Churn risk", "Acquisition channels"])

    with tab1:
        seg = segment_summary(df_team).copy()
        seg.columns = ["Segment","Fans","Avg LTV ($)","Avg Engagement","ST Conv %"]
        seg["Avg LTV ($)"] = seg["Avg LTV ($)"].apply(lambda x: f"${x:.0f}")
        seg["ST Conv %"]   = seg["ST Conv %"].apply(lambda x: f"{x:.1f}%")
        st.dataframe(seg, hide_index=True, use_container_width=True)

    with tab2:
        churn_df = df_team["churn_risk"].value_counts().reset_index()
        churn_df.columns = ["Churn Risk","Fan Count"]
        churn_df["% of Total"] = (churn_df["Fan Count"] / len(df_team) * 100).round(1).astype(str) + "%"
        st.dataframe(churn_df, hide_index=True, use_container_width=True)

    with tab3:
        ch_df = df_team["acquisition_channel"].value_counts().reset_index()
        ch_df.columns = ["Channel","Fans"]
        ch_df["Avg LTV ($)"] = ch_df["Channel"].map(
            df_team.groupby("acquisition_channel")["predicted_ltv_usd"].mean().round(0).astype(int).apply(lambda x: f"${x}")
        )
        st.dataframe(ch_df, hide_index=True, use_container_width=True)

# ── Chat ──────────────────────────────────────────────────────────────────────

# Build role + market context for the engine
role_ctx = role_config["system_addendum"]
role_ctx += "\n\n" + build_role_context(role_config, team_name, market)

market_snippet = build_market_snippet(df_team, market or "All markets", team_name)

# Render history
for msg in st.session_state.messages:
    avatar = "⚽" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "sources" in msg:
            st.markdown(source_badges(msg["sources"]), unsafe_allow_html=True)

# Handle input
prompt     = st.session_state.pending_question
st.session_state.pending_question = None
chat_input = st.chat_input(f"Ask about {team_name} fan activation, campaigns, or strategy...")
if chat_input:
    prompt = chat_input

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
                role_context   = role_ctx,
                market_filter  = market,
                market_data_snippet = market_snippet,
            )
        st.markdown(answer)
        st.markdown(source_badges(sources), unsafe_allow_html=True)

    st.session_state.messages.append({"role":"assistant","content":answer,"sources":sources})

# ── Empty state ───────────────────────────────────────────────────────────────

if not st.session_state.messages:
    st.markdown(f"""
    <div style='text-align:center; padding:48px 20px;'>
      <div style='font-size:40px; margin-bottom:12px'>⚽</div>
      <p style='font-size:16px; font-weight:500; color:{COLORS["ink"]}; margin:0 0 6px'>
        Ready to advise {team_name}
      </p>
      <p style='font-size:14px; color:{COLORS["muted"]}; margin:0'>
        {n_fans:,} fans · {f"{market} market" if market else "All markets"} · Select a mode and ask a question above
      </p>
    </div>
    """, unsafe_allow_html=True)
