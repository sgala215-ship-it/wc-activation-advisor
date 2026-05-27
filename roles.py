"""
roles.py — Sohil Gala · Data & AI Advisory
Role configuration: system prompts, team/market mapping, suggested questions.
Add new roles here without touching app.py or engine.py.
"""

ROLES = {
    "⚽  Soccer Club": {
        "id":          "soccer_club",
        "description": "Single club activation — ticket sales, membership, fan loyalty",
"teams": [
    "Northeast Club",
    "Southeast Club",
    "Midwest Club",
    "South Club",
    "West Coast Club",
    "Mountain West Club",
],
"market_map": {
    "Northeast Club":     "New York",
    "Southeast Club":     "Miami",
    "Midwest Club":       "Chicago",
    "South Club":         "Houston",
    "West Coast Club":    "Los Angeles",
    "Mountain West Club": "Denver",
},        "questions": {
            "🎯  Strategy & Playbooks": [
                "We have 90 days post-tournament. What's the highest ROI activation sequence for our club?",
                "What does our 90-day activation calendar look like?",
                "How do we convert World Cup fans into season ticket holders?",
                "Which fan segments should we target first in our market?",
            ],
            "👥  Fan Intelligence": [
                "How many fans in our market are at high churn risk?",
                "What's the LTV breakdown of fans acquired in our city?",
                "Which acquisition channel brought us the highest quality fans?",
                "What's our season ticket conversion rate vs league benchmark?",
            ],
            "📣  Campaign Ideation": [
                "What campaigns should I use to activate fans signed up during the watch party we hosted?",
                "Generate a 3-email re-engagement sequence for lapsed fans in our market",
                "Write a season ticket early-bird campaign for converted fans",
                "What content strategy works for new-to-soccer fans in our city?",
            ],
        },
        "system_addendum": """
You are advising a single professional soccer club. All recommendations should be:
- Scoped to ONE club and ONE local market — not league-wide
- Focused on club-level commercial goals: season ticket sales, membership growth, match day attendance, local sponsorship
- Aware that the club competes locally for fan attention with other sports franchises in their market
- Sensitive to club budget realities — recommendations should be practical and executable
- Grounded in the specific market data provided for this club's city

When referencing data, only use figures from the club's home market. Do not aggregate across all markets.
When giving campaign ideas, make them feel local and club-specific, not generic soccer content.
""",
    },

    "🏆  Soccer League / Federation": {
        "id":          "soccer_league",
        "description": "League or federation — all markets, all clubs, national programs",
        "teams": [
            "Professional Soccer League",
            "Women's Soccer League",
            "Second Division League",
            "National Soccer Federation",
            "Regional Soccer Confederation",
        ],
        "market_map": None,  # League offices see ALL markets
        "questions": {
            "🎯  Strategy & Playbooks": [
                "We have 90 days post-tournament. What's the highest ROI activation sequence?",
                "What does our national 90-day activation calendar look like?",
                "Which sponsor categories are most at risk of not renewing?",
                "How do we coordinate club-level activation across all markets?",
            ],
            "👥  Fan Intelligence": [
                "Which markets have the highest concentration of high-value fans?",
                "What's the national fan acquisition breakdown by segment?",
                "Which markets need the most urgent churn intervention?",
                "How do we prioritize league investment across all host city markets?",
            ],
            "📣  Campaign Ideation": [
                "What campaigns should I use to activate fans signed up during the watch party we hosted?",
                "Design a national re-engagement campaign for lapsed fans post-tournament",
                "What's the content strategy for converting new-to-soccer fans at scale?",
                "Create a sponsor co-activation framework for league-wide partners",
            ],
        },
        "system_addendum": """
You are advising a soccer league or national federation operating across ALL markets simultaneously.
Your strategic context:
- You are coordinating activation across multiple markets and club partners — not a single team
- Your priorities are league-wide growth metrics: total fan acquisition, national sponsor ROI, broadcast audience growth, club revenue lift
- You have access to the full 50,000-fan dataset across all 12 markets — use aggregate and comparative market data freely
- You are also responsible for coordinating club-level activation so individual clubs benefit from the national campaign
- Sponsor relationships at this level are national/global deals — brand lift and renewal conversations happen at the C-suite level

When giving recommendations, think in terms of national programs that cascade to local markets. Include both the league-level initiative and how clubs execute it locally.
""",
    },

    "🏟️  Other Sports Team": {
        "id":          "other_sports",
        "description": "Non-soccer sports franchise — cross-sport fan conversion strategy",
        "teams": [
            "Northeast Basketball Team",
            "Southeast Football Team",
            "Midwest Baseball Team",
            "Southwest Hockey Team",
            "West Coast Basketball Team",
            "Other — I'll specify in chat",
        ],
        "market_map": {
            "Northeast Basketball Team":    None,
            "Southeast Football Team":      None,
            "Midwest Baseball Team":        None,
            "Southwest Hockey Team":        None,
            "West Coast Basketball Team":   None,
            "Other — I'll specify in chat":None,
        },
        "questions": {
            "🎯  Strategy & Playbooks": [
                "How do we build on World Cup momentum before our season starts?",
                "What's the 90-day plan to capture World Cup fans for our sport?",
                "Which World Cup fan segments are our best cross-sport opportunity?",
                "How do we position our season launch against World Cup momentum?",
            ],
            "👥  Fan Intelligence": [
                "Which World Cup demographics overlap most with our existing fan base?",
                "What's the LTV opportunity if we convert 10% of World Cup fans?",
                "Which fan segments are most open to trying a different sport?",
                "How do we identify World Cup fans who aren't our season ticket holders yet?",
            ],
            "📣  Campaign Ideation": [
                "What campaigns should I use to activate fans signed up during the watch party we hosted?",
                "Create a cross-sport trial experience campaign concept",
                "Write a campaign that bridges soccer culture and our sport's fan experience",
                "How do we use World Cup momentum in our season ticket renewal messaging?",
            ],
        },
        "system_addendum": """
You are advising a non-soccer professional sports team on capturing cross-sport fan opportunity from the 2026 World Cup.
Your strategic context:
- The World Cup created a large pool of newly engaged sports fans in your market — many of whom may not be your current ticket buyers
- Cross-sport fan acquisition is a proven strategy: sports fans tend to consume multiple sports when given the right entry point
- Your activation window depends on your sport's season calendar — identify the nearest home games as conversion opportunities
- The Latino/Hispanic demographic is especially important: they are the core World Cup audience and a growing market for all sports

Adapt tone to the specific sport when the user identifies it. Focus on the shared live-event experience and community angle that crosses sport boundaries.
""",
    },

    "🤝  Sports Sponsor / Brand": {
        "id":          "sponsor",
        "description": "Brand or sponsor partner — ROI reporting, renewal strategy, fan activation",
        "teams": [
            "Automotive Brand",
            "Financial Services Brand",
            "Technology Brand",
            "Beverage / FMCG Brand",
            "Travel / Hospitality Brand",
            "Health & Wellness Brand",
            "Apparel / Sporting Goods Brand",
            "Other Brand",
        ],
        "market_map": None,  # Sponsors typically operate nationally
        "questions": {
            "🎯  Strategy & Playbooks": [
                "How do we maximize ROI in the 60 days post-tournament?",
                "What's the renewal conversation strategy with our rights holder?",
                "Which fan segments should we target with our post-tournament activation?",
                "How do we extend our World Cup sponsorship narrative into the domestic season?",
            ],
            "👥  Fan Intelligence": [
                "Which fan segments have the highest overlap with our target consumer?",
                "What does the post-tournament fan profile look like across markets?",
                "Which markets gave us the strongest brand engagement during the tournament?",
                "What's the LTV of a fan converted through our sponsorship activation?",
            ],
            "📣  Campaign Ideation": [
                "What campaigns should I use to activate fans signed up during the watch party we hosted?",
                "Create a post-tournament brand campaign that extends our World Cup presence",
                "How do we activate our sponsorship through co-registration with the rights holder?",
                "Generate a social content strategy that rides post-tournament fan sentiment",
            ],
        },
        "system_addendum": """
You are advising a brand or corporate sponsor partner on maximizing their World Cup sponsorship investment post-tournament.
Your strategic context:
- The sponsor has invested in official World Cup or rights holder partnership and wants to extend that ROI beyond the event
- Brand recall and fan engagement are at peak immediately post-tournament — the 30-day window is critical
- The sponsor's goal is commercial: leads generated, brand lift achieved, product consideration increased, and ultimately renewal justification
- Data partnership with the rights holder (co-registration, audience insights, clean room matching) is a growing priority for data-mature sponsors

Frame all recommendations in terms of brand ROI and commercial outcomes. Sponsors think in terms of campaign metrics, not fan lifecycle economics — translate accordingly.
""",
    },
}

# ── Helper functions ──────────────────────────────────────────────────────────

def get_role_config(role_label):
    return ROLES.get(role_label, list(ROLES.values())[0])

def get_market_for_team(role_config, team_name):
    if role_config["market_map"] is None:
        return None
    return role_config["market_map"].get(team_name)

def build_role_context(role_config, team_name, market):
    lines = ["ORGANIZATION CONTEXT:"]
    lines.append(f"Role: {role_config['id']}")
    lines.append(f"Organization: {team_name}")
    if market:
        lines.append(f"Primary market: {market}")
        lines.append(f"Data scope: Filtered to {market} market only")
    else:
        lines.append(f"Data scope: All markets (national/league-wide view)")
    return "\n".join(lines)
