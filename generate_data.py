import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

random.seed(42)
np.random.seed(42)

os.makedirs("data", exist_ok=True)

# ─── 1. FAN ACQUISITION DATASET ────────────────────────────────────────────
# 50K fans acquired during/after the World Cup window
n_fans = 50000

markets = {
    "New York":       {"weight": 0.18, "country_mix": ["USA","Mexico","Brazil","Colombia"]},
    "Los Angeles":    {"weight": 0.16, "country_mix": ["USA","Mexico","El Salvador","Guatemala"]},
    "Chicago":        {"weight": 0.10, "country_mix": ["USA","Mexico","Poland","Germany"]},
    "Houston":        {"weight": 0.09, "country_mix": ["USA","Mexico","El Salvador","Honduras"]},
    "Miami":          {"weight": 0.08, "country_mix": ["USA","Colombia","Argentina","Cuba"]},
    "Dallas":         {"weight": 0.07, "country_mix": ["USA","Mexico","Honduras","Guatemala"]},
    "San Francisco":  {"weight": 0.06, "country_mix": ["USA","Mexico","Japan","South Korea"]},
    "Boston":         {"weight": 0.05, "country_mix": ["USA","Portugal","Brazil","Ireland"]},
    "Seattle":        {"weight": 0.05, "country_mix": ["USA","Mexico","Canada","South Korea"]},
    "Atlanta":        {"weight": 0.04, "country_mix": ["USA","Mexico","Ghana","Nigeria"]},
    "Denver":         {"weight": 0.04, "country_mix": ["USA","Mexico","Colombia","Peru"]},
    "Other":          {"weight": 0.08, "country_mix": ["USA","various"]},
}

market_names  = list(markets.keys())
market_weights = [markets[m]["weight"] for m in market_names]

segments = ["Casual Viewer", "Converted Fan", "Lapsed Fan", "New to Soccer"]
seg_weights = [0.35, 0.25, 0.20, 0.20]

channels = ["Digital Ad", "Social Media", "Email Campaign", "Partner Referral",
            "In-Stadium", "Organic Search", "TV Promotion"]
chan_weights = [0.28, 0.25, 0.18, 0.12, 0.08, 0.06, 0.03]

wc_start = datetime(2026, 6, 11)
wc_end   = datetime(2026, 7, 19)
post_end = datetime(2026, 10, 31)
all_days = [wc_start + timedelta(days=i) for i in range((post_end - wc_start).days + 1)]
total_days = len(all_days)

def acquisition_weight(d):
    delta = (d - wc_start).days
    if delta < 0:
        return 0.5
    elif delta <= 38:           # during tournament
        return 1.0 + 2.0 * np.sin(np.pi * delta / 38) ** 2
    else:                        # post-tournament decay
        decay = np.exp(-0.025 * (delta - 38))
        return max(0.2, decay)

day_weights = np.array([acquisition_weight(d) for d in all_days])
day_weights /= day_weights.sum()
acq_days = np.random.choice(all_days, size=n_fans, p=day_weights)

chosen_markets  = np.random.choice(market_names, size=n_fans, p=market_weights)
chosen_segments = np.random.choice(segments, size=n_fans, p=seg_weights)
chosen_channels = np.random.choice(channels, size=n_fans, p=chan_weights)

seg_convert = {"Converted Fan": 0.72, "Lapsed Fan": 0.41, "Casual Viewer": 0.28, "New to Soccer": 0.19}
seg_ltv     = {"Converted Fan": 380,  "Lapsed Fan": 210,  "Casual Viewer": 140,  "New to Soccer": 95}
seg_ticket  = {"Converted Fan": 0.38, "Lapsed Fan": 0.21, "Casual Viewer": 0.12, "New to Soccer": 0.06}
seg_merch   = {"Converted Fan": 0.55, "Lapsed Fan": 0.30, "Casual Viewer": 0.22, "New to Soccer": 0.15}

convert_prob = np.array([seg_convert[s] for s in chosen_segments])
ltv_base     = np.array([seg_ltv[s]     for s in chosen_segments])
ticket_prob  = np.array([seg_ticket[s]  for s in chosen_segments])
merch_prob   = np.array([seg_merch[s]   for s in chosen_segments])

noise = np.random.normal(1.0, 0.15, n_fans)
ltv_values = np.round(np.clip(ltv_base * noise, 20, 900), 2)

df_fans = pd.DataFrame({
    "fan_id":                    [f"FAN{str(i+1).zfill(6)}" for i in range(n_fans)],
    "acquisition_date":          [d.strftime("%Y-%m-%d") for d in acq_days],
    "market":                    chosen_markets,
    "segment":                   chosen_segments,
    "acquisition_channel":       chosen_channels,
    "age_group":                 np.random.choice(["18-24","25-34","35-44","45-54","55+"],
                                                   size=n_fans, p=[0.22,0.31,0.24,0.14,0.09]),
    "gender":                    np.random.choice(["Male","Female","Non-binary/Other"],
                                                   size=n_fans, p=[0.58,0.38,0.04]),
    "country_of_origin":         np.random.choice(["USA","Mexico","Brazil","Colombia","Argentina",
                                                    "England","Germany","Other"],
                                                   size=n_fans, p=[0.42,0.20,0.08,0.06,0.05,0.04,0.03,0.12]),
    "email_opt_in":              np.random.choice([True, False], size=n_fans, p=[0.71, 0.29]),
    "app_downloaded":            np.random.choice([True, False], size=n_fans, p=[0.44, 0.56]),
    "ticket_purchase_intent":    (np.random.rand(n_fans) < ticket_prob).astype(int),
    "merch_purchase_intent":     (np.random.rand(n_fans) < merch_prob).astype(int),
    "season_ticket_conversion":  (np.random.rand(n_fans) < convert_prob).astype(int),
    "predicted_ltv_usd":         ltv_values,
    "engagement_score":          np.clip(np.round(np.random.normal(55, 20, n_fans), 1), 0, 100),
    "churn_risk":                np.random.choice(["Low","Medium","High"],
                                                   size=n_fans, p=[0.35,0.38,0.27]),
})

df_fans.to_csv("data/fan_acquisition.csv", index=False)
print(f"✓ fan_acquisition.csv  — {len(df_fans):,} rows")

# ─── 2. SPONSOR ENGAGEMENT DATASET ─────────────────────────────────────────
sponsors = [
    {"name": "Apex Auto Group",     "category": "Automotive",       "tier": "Presenting",  "contract_value_usd": 8500000},
    {"name": "GlobalBank",           "category": "Financial Svcs",   "tier": "Presenting",  "contract_value_usd": 7200000},
    {"name": "SportsFuel Energy",    "category": "FMCG/Beverage",    "tier": "Gold",        "contract_value_usd": 4100000},
    {"name": "TechVerse",            "category": "Technology",        "tier": "Gold",        "contract_value_usd": 3800000},
    {"name": "NationAir",            "category": "Travel/Airlines",   "tier": "Gold",        "contract_value_usd": 3500000},
    {"name": "HealthPlus Insurance", "category": "Insurance/Health",  "tier": "Silver",      "contract_value_usd": 1900000},
    {"name": "ProGear Apparel",      "category": "Sporting Goods",    "tier": "Silver",      "contract_value_usd": 1600000},
    {"name": "QuickBite Foods",      "category": "Food/Restaurant",   "tier": "Silver",      "contract_value_usd": 1400000},
    {"name": "MediaStream",          "category": "Media/Streaming",   "tier": "Bronze",      "contract_value_usd": 850000},
    {"name": "BuildRight Realty",    "category": "Real Estate",       "tier": "Bronze",      "contract_value_usd": 720000},
]

rows = []
for sp in sponsors:
    for phase in ["Pre-Tournament", "During Tournament", "Post-Tournament (30d)",
                  "Post-Tournament (60d)", "Post-Tournament (90d)"]:
        if phase == "Pre-Tournament":
            brand_lift = round(random.uniform(2, 8), 1)
            engagement = round(random.uniform(30, 55), 1)
            roi = round(random.uniform(0.9, 1.4), 2)
            renewal_prob = round(random.uniform(0.6, 0.8), 2)
        elif phase == "During Tournament":
            brand_lift = round(random.uniform(18, 42), 1)
            engagement = round(random.uniform(65, 92), 1)
            roi = round(random.uniform(2.1, 3.8), 2)
            renewal_prob = round(random.uniform(0.75, 0.95), 2)
        elif "30d" in phase:
            brand_lift = round(random.uniform(12, 28), 1)
            engagement = round(random.uniform(52, 74), 1)
            roi = round(random.uniform(1.5, 2.4), 2)
            renewal_prob = round(random.uniform(0.65, 0.88), 2)
        elif "60d" in phase:
            brand_lift = round(random.uniform(7, 18), 1)
            engagement = round(random.uniform(40, 62), 1)
            roi = round(random.uniform(1.1, 1.8), 2)
            renewal_prob = round(random.uniform(0.55, 0.78), 2)
        else:
            brand_lift = round(random.uniform(3, 12), 1)
            engagement = round(random.uniform(30, 52), 1)
            roi = round(random.uniform(0.9, 1.4), 2)
            renewal_prob = round(random.uniform(0.45, 0.70), 2)

        rows.append({
            "sponsor_name":         sp["name"],
            "category":             sp["category"],
            "tier":                 sp["tier"],
            "contract_value_usd":   sp["contract_value_usd"],
            "phase":                phase,
            "brand_lift_pct":       brand_lift,
            "fan_engagement_score": engagement,
            "roi_multiple":         roi,
            "social_impressions_m": round(random.uniform(1, 40), 1),
            "renewal_probability":  renewal_prob,
            "activation_quality":   random.choice(["Excellent","Good","Average","Below Average"]),
        })

df_sponsors = pd.DataFrame(rows)
df_sponsors.to_csv("data/sponsor_engagement.csv", index=False)
print(f"✓ sponsor_engagement.csv — {len(df_sponsors):,} rows")

# ─── 3. CRM ENGAGEMENT DATASET ──────────────────────────────────────────────
n_crm = 50000
campaign_types = ["Welcome Series", "Re-engagement", "Ticket Upsell",
                  "Merchandise Offer", "Loyalty Reward", "Content Newsletter"]

df_crm = pd.DataFrame({
    "fan_id":             [f"FAN{str(i+1).zfill(6)}" for i in range(n_crm)],
    "segment":            np.random.choice(segments, size=n_crm, p=seg_weights),
    "campaign_type":      np.random.choice(campaign_types, size=n_crm),
    "emails_sent":        np.random.randint(1, 12, size=n_crm),
    "email_open_rate":    np.round(np.clip(np.random.normal(0.34, 0.12, n_crm), 0.05, 0.85), 3),
    "click_through_rate": np.round(np.clip(np.random.normal(0.09, 0.05, n_crm), 0.01, 0.40), 3),
    "app_sessions_30d":   np.random.randint(0, 45, size=n_crm),
    "push_opt_in":        np.random.choice([True, False], size=n_crm, p=[0.52, 0.48]),
    "days_since_last_touch": np.random.randint(0, 90, size=n_crm),
    "journey_stage":      np.random.choice(["Awareness","Consideration","Conversion","Loyalty","Churned"],
                                            size=n_crm, p=[0.25,0.22,0.20,0.18,0.15]),
    "revenue_generated_usd": np.round(np.clip(np.random.exponential(85, n_crm), 0, 800), 2),
})
df_crm.to_csv("data/crm_engagement.csv", index=False)
print(f"✓ crm_engagement.csv   — {len(df_crm):,} rows")

# ─── 4. ACTIVATION PLAYBOOK SUMMARY ─────────────────────────────────────────
playbook = [
    {"window": "0-30 days post-tournament",  "priority": 1, "tactic": "Welcome email series for new fans",              "target_segment": "All new acquisitions",      "expected_open_rate": "38-45%", "est_conversion_rate": "12-18%", "resource_level": "Low",    "roi_estimate": "3.2x"},
    {"window": "0-30 days post-tournament",  "priority": 2, "tactic": "Sponsor co-branded content push",                "target_segment": "Casual Viewer, New to Soccer","expected_open_rate": "28-35%","est_conversion_rate": "8-12%", "resource_level": "Medium", "roi_estimate": "2.1x"},
    {"window": "0-30 days post-tournament",  "priority": 3, "tactic": "Season ticket early-bird offer",                 "target_segment": "Converted Fan",             "expected_open_rate": "42-55%", "est_conversion_rate": "22-30%","resource_level": "Low",    "roi_estimate": "4.8x"},
    {"window": "31-60 days post-tournament", "priority": 1, "tactic": "Lapsed fan re-engagement campaign",              "target_segment": "Lapsed Fan",                "expected_open_rate": "25-32%", "est_conversion_rate": "9-14%", "resource_level": "Medium", "roi_estimate": "2.7x"},
    {"window": "31-60 days post-tournament", "priority": 2, "tactic": "Merchandise limited edition drop",               "target_segment": "Converted Fan, Lapsed Fan", "expected_open_rate": "36-44%", "est_conversion_rate": "15-22%","resource_level": "Medium", "roi_estimate": "3.1x"},
    {"window": "31-60 days post-tournament", "priority": 3, "tactic": "Sponsor renewal outreach with brand lift data",  "target_segment": "Sponsor partners",          "expected_open_rate": "N/A",    "est_conversion_rate": "65-80%","resource_level": "High",   "roi_estimate": "5.5x"},
    {"window": "61-90 days post-tournament", "priority": 1, "tactic": "Club partnership upsell for MLS clubs",          "target_segment": "Converted Fan",             "expected_open_rate": "38-48%", "est_conversion_rate": "18-26%","resource_level": "High",   "roi_estimate": "4.2x"},
    {"window": "61-90 days post-tournament", "priority": 2, "tactic": "Loyalty program enrollment push",               "target_segment": "All retained fans",         "expected_open_rate": "30-40%", "est_conversion_rate": "20-28%","resource_level": "Medium", "roi_estimate": "3.8x"},
    {"window": "61-90 days post-tournament", "priority": 3, "tactic": "Youth/family segment content series",           "target_segment": "New to Soccer",             "expected_open_rate": "22-30%", "est_conversion_rate": "7-11%", "resource_level": "Low",    "roi_estimate": "1.9x"},
    {"window": "90+ days",                   "priority": 1, "tactic": "Annual renewal & loyalty tier upgrade campaign", "target_segment": "Converted Fan, Loyalty",    "expected_open_rate": "44-58%", "est_conversion_rate": "28-38%","resource_level": "Medium", "roi_estimate": "5.1x"},
    {"window": "90+ days",                   "priority": 2, "tactic": "Churn-risk intervention (high-risk cohort)",    "target_segment": "High churn risk fans",      "expected_open_rate": "18-26%", "est_conversion_rate": "6-10%", "resource_level": "High",   "roi_estimate": "2.3x"},
    {"window": "90+ days",                   "priority": 3, "tactic": "New market expansion — diaspora targeting",     "target_segment": "New to Soccer",             "expected_open_rate": "24-32%", "est_conversion_rate": "9-14%", "resource_level": "High",   "roi_estimate": "2.8x"},
]
df_playbook = pd.DataFrame(playbook)
df_playbook.to_csv("data/activation_playbook.csv", index=False)
print(f"✓ activation_playbook.csv — {len(df_playbook):,} rows")

# ─── 5. MARKET SUMMARY (pre-aggregated for quick context) ───────────────────
market_summary = []
for market in market_names:
    fans_in_market = df_fans[df_fans["market"] == market]
    n = len(fans_in_market)
    market_summary.append({
        "market":                  market,
        "total_fans_acquired":     n,
        "pct_email_opted_in":      round(fans_in_market["email_opt_in"].mean() * 100, 1),
        "pct_app_downloaded":      round(fans_in_market["app_downloaded"].mean() * 100, 1),
        "avg_engagement_score":    round(fans_in_market["engagement_score"].mean(), 1),
        "avg_predicted_ltv_usd":   round(fans_in_market["predicted_ltv_usd"].mean(), 2),
        "pct_high_churn_risk":     round((fans_in_market["churn_risk"] == "High").mean() * 100, 1),
        "top_segment":             fans_in_market["segment"].value_counts().idxmax(),
        "top_acquisition_channel": fans_in_market["acquisition_channel"].value_counts().idxmax(),
        "season_ticket_conversion_rate": round(fans_in_market["season_ticket_conversion"].mean() * 100, 1),
    })
df_market = pd.DataFrame(market_summary)
df_market.to_csv("data/market_summary.csv", index=False)
print(f"✓ market_summary.csv   — {len(df_market):,} rows")

print("\n✅ All datasets generated in /data/")
print(f"   Total fans modeled:  {n_fans:,}")
print(f"   Sponsors tracked:    {len(sponsors)}")
print(f"   Markets covered:     {len(market_names)}")
print(f"   Activation tactics:  {len(playbook)}")
