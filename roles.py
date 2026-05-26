"""
roles.py — Sohil Gala · Data & AI Advisory
Role configuration: system prompts, team/market mapping, suggested questions.
Add new roles here without touching app.py or engine.py.
"""

# ── Role definitions ──────────────────────────────────────────────────────────

ROLES = {
    "⚽  MLS / Soccer Club": {
        "id":          "soccer_club",
        "description": "Single club activation — ticket sales, membership, fan loyalty",
        "teams": [
            "Atlanta United FC",
            "Chicago Fire FC",
            "FC Dallas",
            "Houston Dynamo FC",
            "Inter Miami CF",
            "LA Galaxy",
            "LAFC",
            "New England Revolution",
            "New York City FC",
            "New York Red Bulls",
            "Seattle Sounders FC",
            "Colorado Rapids",
        ],
        "market_map": {
            "Atlanta United FC":       "Atlanta",
            "Chicago Fire FC":         "Chicago",
            "FC Dallas":               "Dallas",
            "Houston Dynamo FC":       "Houston",
            "Inter Miami CF":          "Miami",
            "LA Galaxy":               "Los Angeles",
            "LAFC":                    "Los Angeles",
            "New England Revolution":  "Boston",
            "New York City FC":        "New York",
            "New York Red Bulls":      "New York",
            "Seattle Sounders FC":     "Seattle",
            "Colorado Rapids":         "Denver",
        },
        "questions": {
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
You are advising a single MLS or professional soccer club. All recommendations should be:
- Scoped to ONE club and ONE local market — not league-wide
- Focused on club-level commercial goals: season ticket sales, membership growth, match day attendance, local sponsorship
- Aware that the club competes locally for fan attention with other sports (NFL, NBA, NHL, MLB depending on market)
- Sensitive to club budget realities — most MLS clubs have smaller commercial teams than major European clubs
- Grounded in the specific market data provided for this club's city

When referencing data, only use figures from the club's home market. Do not aggregate across all markets.
When giving campaign ideas, make them feel local and club-specific, not generic soccer content.
""",
    },

    "🏈  NFL Team": {
        "id":          "nfl_team",
        "description": "Cross-sport fan conversion — capturing soccer fans for NFL product",
        "teams": [
            "Atlanta Falcons",
            "Chicago Bears",
            "Dallas Cowboys",
            "Houston Texans",
            "Miami Dolphins",
            "Los Angeles Rams",
            "Los Angeles Chargers",
            "New England Patriots",
            "New York Giants",
            "New York Jets",
            "Seattle Seahawks",
            "Denver Broncos",
        ],
        "market_map": {
            "Atlanta Falcons":       "Atlanta",
            "Chicago Bears":         "Chicago",
            "Dallas Cowboys":        "Dallas",
            "Houston Texans":        "Houston",
            "Miami Dolphins":        "Miami",
            "Los Angeles Rams":      "Los Angeles",
            "Los Angeles Chargers":  "Los Angeles",
            "New England Patriots":  "Boston",
            "New York Giants":       "New York",
            "New York Jets":         "New York",
            "Seattle Seahawks":      "Seattle",
            "Denver Broncos":        "Denver",
        },
        "questions": {
            "🎯  Strategy & Playbooks": [
                "How do we capture World Cup fans before the NFL season starts in September?",
                "What's the 90-day window strategy to convert soccer fans to NFL fans?",
                "Which World Cup fan segments are most likely to buy NFL tickets?",
                "How do we position the NFL season launch against World Cup momentum?",
            ],
            "👥  Fan Intelligence": [
                "Which World Cup fan segments overlap most with NFL fan profiles?",
                "How many fans in our market attended World Cup matches and aren't NFL season ticket holders?",
                "What's the LTV of a converted cross-sport fan vs a native NFL fan?",
                "Which demographics from the World Cup audience are our biggest opportunity?",
            ],
            "📣  Campaign Ideation": [
                "What campaigns should I use to activate fans signed up during the watch party we hosted?",
                "Write a campaign targeting Latino World Cup fans for NFL season tickets",
                "Create a cross-sport fan experience concept for preseason",
                "How do we use NFL players with World Cup connections in our marketing?",
            ],
        },
        "system_addendum": """
You are advising an NFL team on capturing cross-sport fan opportunity from the 2026 World Cup.
Your strategic context:
- The NFL season starts in September — 6-8 weeks after the World Cup final. This is the critical capture window.
- World Cup fans in NFL host cities are a high-value, partially-overlapping audience
- Latino/Hispanic fans are a core World Cup demographic and a growing NFL target audience
- The goal is cross-sport conversion: turn soccer fans into NFL ticket buyers, merchandise customers, and eventually season ticket holders
- NFL teams have larger commercial budgets than soccer clubs — recommendations can include bigger activations

Key tension to address: NFL and soccer compete for the same living room, the same weekend, and increasingly the same demographics. The World Cup is a rare moment when soccer fans are warm and open — the NFL must move before that window closes.

When referencing data, focus on the team's home market. Highlight age groups and demographics most likely to be NFL-convertible.
""",
    },

    "🏟️  League Office": {
        "id":          "league_office",
        "description": "Federation-level strategy — all markets, all clubs, national programs",
        "teams": [
            "MLS (Major League Soccer)",
            "NWSL (National Women's Soccer League)",
            "USL Championship",
            "US Soccer Federation",
            "CONCACAF",
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
                "How do we prioritize league investment across 12 host city markets?",
            ],
            "📣  Campaign Ideation": [
                "What campaigns should I use to activate fans signed up during the watch party we hosted?",
                "Design a national re-engagement campaign for lapsed fans post-tournament",
                "What's the content strategy for converting new-to-soccer fans at scale?",
                "Create a sponsor co-activation framework for league-wide partners",
            ],
        },
        "system_addendum": """
You are advising a league office or national federation operating across ALL markets simultaneously.
Your strategic context:
- You are coordinating activation across multiple markets and club partners — not a single team
- Your priorities are league-wide growth metrics: total fan acquisition, national sponsor ROI, broadcast audience growth, club revenue lift
- You have access to the full 50,000-fan dataset across all 12 markets — use aggregate and comparative market data freely
- You are also responsible for coordinating club-level activation so individual clubs benefit from the national campaign
- Sponsor relationships at this level are national/global deals, not local — brand lift and renewal conversations happen at the C-suite level

When giving recommendations, think in terms of national programs that cascade to local markets. Include both the league-level initiative and how clubs execute it locally.
""",
    },

    "🏀  Other Sports Team": {
        "id":          "other_sports",
        "description": "NBA, NHL, MLB — cross-sport fan opportunity strategy",
        "teams": [
            "NBA team (my market)",
            "NHL team (my market)",
            "MLB team (my market)",
            "Other — I'll specify in chat",
        ],
        "market_map": {
            "NBA team (my market)":   None,
            "NHL team (my market)":   None,
            "MLB team (my market)":   None,
            "Other — I'll specify in chat": None,
        },
        "questions": {
            "🎯  Strategy & Playbooks": [
                "How do we build on World Cup momentum before our season starts?",
                "What's the 90-day plan to capture World Cup fans for our sport?",
                "How do we compete with soccer for fan attention post-tournament?",
                "Which World Cup fan segments are our best cross-sport opportunity?",
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
                "How do we use World Cup player connections in our marketing?",
                "Write a campaign that bridges soccer culture and our sport's fan experience",
            ],
        },
        "system_addendum": """
You are advising a non-soccer professional sports team (NBA, NHL, or MLB) on capturing cross-sport fan opportunity from the 2026 World Cup.
Your strategic context:
- The World Cup created a large pool of newly engaged sports fans in your market — many of whom may not be your current ticket buyers
- Cross-sport fan acquisition is a proven strategy: sports fans tend to consume multiple sports when given the right entry point
- Your activation window depends on your sport's season calendar — identify the nearest home games as conversion opportunities
- The Latino/Hispanic demographic is especially important: they are the core World Cup audience and a growing market for all US sports

Tone your advice to the specific sport when the user identifies it. NBA advice should emphasize entertainment and urban culture crossover. NHL should emphasize the shared live-event intensity. MLB should emphasize the family and community angle.
""",
    },
}

# ── Helper functions ──────────────────────────────────────────────────────────

def get_role_config(role_label):
    return ROLES.get(role_label, list(ROLES.values())[0])

def get_market_for_team(role_config, team_name):
    """Return the market to filter data by, or None for all markets."""
    if role_config["market_map"] is None:
        return None
    return role_config["market_map"].get(team_name)

def build_role_context(role_config, team_name, market):
    """Build a context string to prepend to the system prompt."""
    lines = [f"ORGANIZATION CONTEXT:"]
    lines.append(f"Role: {role_config['id']}")
    lines.append(f"Organization: {team_name}")
    if market:
        lines.append(f"Primary market: {market}")
        lines.append(f"Data scope: Filtered to {market} market only")
    else:
        lines.append(f"Data scope: All markets (national/league-wide view)")
    return "\n".join(lines)
