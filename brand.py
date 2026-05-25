"""
brand.py — Sohil Gala · Data & AI Advisory
Master design token file. Import this into every tool you build.
All colors, typography, spacing, and component CSS in one place.
Update here → updates everywhere.
"""

# ── Brand identity ────────────────────────────────────────────────────────────

BRAND = {
    "name":     "Sohil Gala",
    "tagline":  "Data & AI Advisory",
    "url":      "sohilgala.com",
    "logo_icon": "📊",   # fallback emoji if SVG unavailable
}

# ── Color tokens ──────────────────────────────────────────────────────────────

COLORS = {
    # Primary — Emerald
    "emerald":       "#1D9E75",
    "emerald_dark":  "#0F6E56",
    "emerald_deep":  "#085041",
    "emerald_tint":  "#EAF3DE",
    "emerald_mid":   "#639922",

    # Neutrals
    "ink":           "#111827",
    "slate":         "#374151",
    "muted":         "#6B7280",
    "border":        "#E5E7EB",
    "surface":       "#F9FAFB",
    "white":         "#FFFFFF",

    # Semantic
    "success":       "#1D9E75",
    "warning":       "#BA7517",
    "warning_tint":  "#FAEEDA",
    "danger":        "#A32D2D",
    "danger_tint":   "#FCEBEB",
    "info":          "#185FA5",
    "info_tint":     "#E6F1FB",
}

# ── Typography ────────────────────────────────────────────────────────────────

TYPE = {
    "font_sans":  "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    "font_mono":  "'JetBrains Mono', 'Fira Code', monospace",

    "h1":  {"size": "22px", "weight": "500", "color": COLORS["ink"]},
    "h2":  {"size": "18px", "weight": "500", "color": COLORS["ink"]},
    "h3":  {"size": "15px", "weight": "500", "color": COLORS["ink"]},
    "body":{"size": "14px", "weight": "400", "color": COLORS["slate"]},
    "sm":  {"size": "12px", "weight": "400", "color": COLORS["muted"]},
    "xs":  {"size": "11px", "weight": "400", "color": COLORS["muted"]},
}

# ── Spacing & radius ──────────────────────────────────────────────────────────

SPACE = {
    "xs":  "4px",
    "sm":  "8px",
    "md":  "12px",
    "lg":  "16px",
    "xl":  "24px",
    "2xl": "32px",
}

RADIUS = {
    "sm":  "4px",
    "md":  "8px",
    "lg":  "12px",
    "xl":  "16px",
    "full":"9999px",
}

# ── Master CSS ────────────────────────────────────────────────────────────────
# Inject this into any Streamlit app via st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

GLOBAL_CSS = f"""
<style>
  /* ── Reset & base ─────────────────────────────────────── */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

  html, body, [class*="css"] {{
    font-family: {TYPE["font_sans"]};
  }}

  /* ── App backgrounds ──────────────────────────────────── */
  .stApp {{
    background-color: {COLORS["surface"]};
  }}

  [data-testid="stSidebar"] {{
    background-color: {COLORS["white"]};
    border-right: 0.5px solid {COLORS["border"]};
  }}

  /* ── Top nav bar (Streamlit header) ───────────────────── */
  [data-testid="stHeader"] {{
    background-color: {COLORS["white"]};
    border-bottom: 0.5px solid {COLORS["border"]};
  }}

  /* ── Sidebar brand header ─────────────────────────────── */
  .sg-brand {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0 0 16px 0;
    border-bottom: 0.5px solid {COLORS["border"]};
    margin-bottom: 20px;
  }}
  .sg-logomark {{
    width: 32px;
    height: 32px;
    background: {COLORS["emerald"]};
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    font-size: 16px;
  }}
  .sg-brand-text {{ line-height: 1.2; }}
  .sg-brand-name {{
    font-size: 14px;
    font-weight: 500;
    color: {COLORS["ink"]};
    margin: 0;
  }}
  .sg-brand-tag {{
    font-size: 11px;
    color: {COLORS["muted"]};
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }}

  /* ── Page title ───────────────────────────────────────── */
  .sg-page-title {{
    font-size: 22px;
    font-weight: 500;
    color: {COLORS["ink"]};
    margin: 0 0 4px;
    letter-spacing: -0.01em;
  }}
  .sg-page-sub {{
    font-size: 14px;
    color: {COLORS["muted"]};
    margin: 0 0 24px;
  }}

  /* ── Section labels ───────────────────────────────────── */
  .sg-label {{
    font-size: 11px;
    font-weight: 500;
    color: {COLORS["muted"]};
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin: 0 0 10px;
  }}

  /* ── Cards ────────────────────────────────────────────── */
  .sg-card {{
    background: {COLORS["white"]};
    border: 0.5px solid {COLORS["border"]};
    border-radius: {RADIUS["lg"]};
    padding: 16px 20px;
    margin-bottom: 12px;
  }}
  .sg-card-title {{
    font-size: 14px;
    font-weight: 500;
    color: {COLORS["ink"]};
    margin: 0 0 4px;
  }}
  .sg-card-sub {{
    font-size: 12px;
    color: {COLORS["muted"]};
    margin: 0 0 12px;
  }}

  /* ── Metric cards ─────────────────────────────────────── */
  [data-testid="stMetric"] {{
    background: {COLORS["white"]};
    border: 0.5px solid {COLORS["border"]};
    border-radius: {RADIUS["md"]};
    padding: 14px 16px;
  }}
  [data-testid="stMetricLabel"] {{
    font-size: 12px !important;
    color: {COLORS["muted"]} !important;
  }}
  [data-testid="stMetricValue"] {{
    font-size: 22px !important;
    font-weight: 500 !important;
    color: {COLORS["ink"]} !important;
  }}
  [data-testid="stMetricDelta"] {{
    font-size: 12px !important;
  }}

  /* ── Buttons ──────────────────────────────────────────── */
  .stButton > button {{
    background: {COLORS["white"]};
    color: {COLORS["slate"]};
    border: 0.5px solid {COLORS["border"]};
    border-radius: {RADIUS["md"]};
    font-size: 13px;
    font-weight: 400;
    padding: 6px 14px;
    transition: all 0.15s;
    width: 100%;
    text-align: left;
  }}
  .stButton > button:hover {{
    background: {COLORS["emerald_tint"]};
    color: {COLORS["emerald_dark"]};
    border-color: {COLORS["emerald"]};
  }}

  /* ── Primary button (use .sg-btn-primary class on container) */
  .sg-primary .stButton > button {{
    background: {COLORS["emerald"]};
    color: {COLORS["white"]};
    border: none;
    text-align: center;
    font-weight: 500;
  }}
  .sg-primary .stButton > button:hover {{
    background: {COLORS["emerald_dark"]};
    color: {COLORS["white"]};
  }}

  /* ── Chat interface ───────────────────────────────────── */
  [data-testid="stChatMessage"] {{
    background: {COLORS["white"]};
    border: 0.5px solid {COLORS["border"]};
    border-radius: {RADIUS["lg"]};
    padding: 4px 8px;
    margin-bottom: 8px;
  }}
  [data-testid="stChatInput"] textarea {{
    background: {COLORS["white"]} !important;
    border: 0.5px solid {COLORS["border"]} !important;
    border-radius: {RADIUS["md"]} !important;
    font-size: 14px !important;
    color: {COLORS["ink"]} !important;
  }}
  [data-testid="stChatInput"] textarea:focus {{
    border-color: {COLORS["emerald"]} !important;
    box-shadow: 0 0 0 3px {COLORS["emerald"]}20 !important;
  }}

  /* ── Sidebar nav items ────────────────────────────────── */
  .sg-nav-item {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 10px;
    border-radius: {RADIUS["md"]};
    font-size: 13px;
    color: {COLORS["slate"]};
    cursor: pointer;
    margin-bottom: 2px;
    transition: all 0.15s;
  }}
  .sg-nav-item:hover {{
    background: {COLORS["surface"]};
    color: {COLORS["ink"]};
  }}
  .sg-nav-item.active {{
    background: {COLORS["emerald_tint"]};
    color: {COLORS["emerald_dark"]};
    font-weight: 500;
  }}

  /* ── Badges ───────────────────────────────────────────── */
  .sg-badge {{
    display: inline-block;
    font-size: 11px;
    font-weight: 500;
    padding: 2px 10px;
    border-radius: {RADIUS["full"]};
    margin: 2px 3px 2px 0;
  }}
  .sg-badge-green  {{ background: {COLORS["emerald_tint"]}; color: {COLORS["emerald_deep"]}; }}
  .sg-badge-amber  {{ background: {COLORS["warning_tint"]}; color: #633806; }}
  .sg-badge-red    {{ background: {COLORS["danger_tint"]};  color: {COLORS["danger"]}; }}
  .sg-badge-blue   {{ background: {COLORS["info_tint"]};    color: {COLORS["info"]}; }}
  .sg-badge-slate  {{ background: {COLORS["surface"]}; color: {COLORS["slate"]}; border: 0.5px solid {COLORS["border"]}; }}

  /* ── Source citations ─────────────────────────────────── */
  .sg-source {{
    display: inline-block;
    background: {COLORS["emerald_tint"]};
    color: {COLORS["emerald_dark"]};
    font-size: 11px;
    padding: 2px 10px;
    border-radius: {RADIUS["full"]};
    margin: 3px 3px 3px 0;
    border: 0.5px solid {COLORS["emerald"]}33;
  }}

  /* ── Pill tabs ────────────────────────────────────────── */
  [data-testid="stRadio"] > div {{
    display: flex;
    flex-direction: column;
    gap: 2px;
  }}

  /* ── Divider ──────────────────────────────────────────── */
  hr {{
    border: none;
    border-top: 0.5px solid {COLORS["border"]};
    margin: 16px 0;
  }}

  /* ── Dataframe ────────────────────────────────────────── */
  [data-testid="stDataFrame"] {{
    border: 0.5px solid {COLORS["border"]};
    border-radius: {RADIUS["md"]};
    overflow: hidden;
  }}

  /* ── Expander ─────────────────────────────────────────── */
  [data-testid="stExpander"] {{
    border: 0.5px solid {COLORS["border"]} !important;
    border-radius: {RADIUS["md"]} !important;
    background: {COLORS["white"]};
  }}

  /* ── Footer ───────────────────────────────────────────── */
  .sg-footer {{
    display: flex;
    align-items: center;
    gap: 8px;
    padding-top: 16px;
    margin-top: 24px;
    border-top: 0.5px solid {COLORS["border"]};
  }}
  .sg-footer-dot {{
    width: 4px;
    height: 4px;
    border-radius: 50%;
    background: {COLORS["emerald"]};
    flex-shrink: 0;
  }}
  .sg-footer-text {{
    font-size: 12px;
    color: {COLORS["muted"]};
  }}

  /* ── Mobile responsive ────────────────────────────────── */
  @media (max-width: 768px) {{
    .sg-page-title {{ font-size: 18px; }}
    .sg-card {{ padding: 12px 14px; }}
    [data-testid="stMetricValue"] {{ font-size: 18px !important; }}
  }}

  /* ── Hide Streamlit defaults ──────────────────────────── */
  footer {{ visibility: hidden; }}
  #MainMenu {{ visibility: hidden; }}
  [data-testid="stToolbar"] {{ display: none; }}
</style>
"""

# ── Sidebar brand HTML ────────────────────────────────────────────────────────

SIDEBAR_BRAND_HTML = f"""
<div class="sg-brand">
  <div class="sg-logomark">📊</div>
  <div class="sg-brand-text">
    <p class="sg-brand-name">{BRAND["name"]}</p>
    <p class="sg-brand-tag">{BRAND["tagline"]}</p>
  </div>
</div>
"""

# ── Footer HTML ───────────────────────────────────────────────────────────────

FOOTER_HTML = f"""
<div class="sg-footer">
  <div class="sg-footer-dot"></div>
  <span class="sg-footer-text">{BRAND["name"]} · {BRAND["tagline"]} · {BRAND["url"]}</span>
</div>
"""

# ── Page header HTML ──────────────────────────────────────────────────────────

def page_header(title, subtitle=""):
    return f"""
<div>
  <p class="sg-page-title">{title}</p>
  <p class="sg-page-sub">{subtitle}</p>
</div>
"""

# ── Badge HTML ────────────────────────────────────────────────────────────────

def badge(text, variant="slate"):
    return f'<span class="sg-badge sg-badge-{variant}">{text}</span>'

# ── Source badge HTML ─────────────────────────────────────────────────────────

def source_badges(sources):
    return " ".join(f'<span class="sg-source">{s}</span>' for s in sources)
