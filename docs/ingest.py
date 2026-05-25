"""
ingest.py — World Cup Activation Advisor
Builds a BM25 keyword index over all knowledge base documents.
No external embedding model needed — fully self-contained.
"""

import os, re, pickle
import pandas as pd
from rank_bm25 import BM25Okapi

DOCS_DIR   = "docs"
DATA_DIR   = "data"
INDEX_FILE = "vectordb/bm25_index.pkl"
CHUNK_SIZE = 400
OVERLAP    = 60

os.makedirs("vectordb", exist_ok=True)

def tokenize(text):
    return re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())

def chunk_text(text, source, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    words, chunks, start, idx = text.split(), [], 0, 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append({"text": " ".join(words[start:end]), "source": source, "chunk": idx})
        idx += 1
        start = end - overlap
        if end == len(words):
            break
    return chunks

def load_documents():
    all_chunks = []
    for fname in sorted(os.listdir(DOCS_DIR)):
        if not fname.endswith(".txt"):
            continue
        with open(os.path.join(DOCS_DIR, fname), "r", encoding="utf-8") as f:
            text = f.read()
        chunks = chunk_text(text, source=fname.replace(".txt",""))
        all_chunks.extend(chunks)
        print(f"  {fname}: {len(chunks)} chunks")
    return all_chunks

def csv_to_narrative_chunks():
    chunks = []

    # Fan acquisition
    df = pd.read_csv(os.path.join(DATA_DIR, "fan_acquisition.csv"))
    seg_stats = df.groupby("segment").agg(
        count=("fan_id","count"), avg_ltv=("predicted_ltv_usd","mean"),
        avg_eng=("engagement_score","mean"), ticket=("ticket_purchase_intent","mean"),
        stc=("season_ticket_conversion","mean"),
    ).round(2)
    text = f"FAN ACQUISITION DATA SUMMARY\nTotal fans: {len(df):,}\n\n"
    for seg, row in seg_stats.iterrows():
        text += (f"{seg}: {int(row['count']):,} fans ({int(row['count'])/len(df)*100:.1f}%). "
                 f"Avg LTV ${row['avg_ltv']:.0f}. Avg engagement {row['avg_eng']:.1f}/100. "
                 f"Ticket intent {row['ticket']*100:.1f}%. Season ticket conversion {row['stc']*100:.1f}%.\n\n")
    churn = df["churn_risk"].value_counts(normalize=True).mul(100).round(1)
    text += "CHURN RISK: " + ", ".join(f"{k}: {v}%" for k,v in churn.items()) + "\n\n"
    top_ch = df["acquisition_channel"].value_counts().head(5)
    text += "TOP CHANNELS: " + ", ".join(f"{k}: {v:,}" for k,v in top_ch.items()) + "\n"
    chunks.extend(chunk_text(text, source="data_fan_acquisition_summary"))

    # Market summary
    mdf = pd.read_csv(os.path.join(DATA_DIR, "market_summary.csv"))
    mtext = "MARKET SUMMARY DATA\n\n"
    for _, row in mdf.iterrows():
        mtext += (f"{row['market']}: {int(row['total_fans_acquired']):,} fans. "
                  f"Email opt-in {row['pct_email_opted_in']}%. App downloads {row['pct_app_downloaded']}%. "
                  f"Avg LTV ${row['avg_predicted_ltv_usd']:.0f}. High churn {row['pct_high_churn_risk']}%. "
                  f"Top segment: {row['top_segment']}. Season ticket conversion {row['season_ticket_conversion_rate']}%.\n\n")
    chunks.extend(chunk_text(mtext, source="data_market_summary"))

    # Sponsor data
    sdf = pd.read_csv(os.path.join(DATA_DIR, "sponsor_engagement.csv"))
    stext = "SPONSOR ENGAGEMENT DATA\n\n"
    phase_stats = sdf.groupby("phase").agg(
        avg_bl=("brand_lift_pct","mean"), avg_roi=("roi_multiple","mean"),
        avg_ren=("renewal_probability","mean"),
    ).round(2)
    for phase, row in phase_stats.iterrows():
        stext += (f"{phase}: Brand lift {row['avg_bl']}%, ROI {row['avg_roi']}x, "
                  f"renewal probability {row['avg_ren']*100:.0f}%.\n")
    during = sdf[sdf["phase"] == "During Tournament"]
    stext += "\nINDIVIDUAL SPONSORS:\n"
    for _, row in during.iterrows():
        stext += (f"{row['sponsor_name']} ({row['category']}, {row['tier']}): "
                  f"Brand lift {row['brand_lift_pct']}%, ROI {row['roi_multiple']}x.\n")
    chunks.extend(chunk_text(stext, source="data_sponsor_summary"))

    # Activation playbook
    pdf = pd.read_csv(os.path.join(DATA_DIR, "activation_playbook.csv"))
    ptext = "ACTIVATION PLAYBOOK DATA\n\n"
    for _, row in pdf.iterrows():
        ptext += (f"Window: {row['window']} | Priority {row['priority']}: {row['tactic']}. "
                  f"Target: {row['target_segment']}. Open rate: {row['expected_open_rate']}. "
                  f"Conversion: {row['est_conversion_rate']}. ROI: {row['roi_estimate']}.\n\n")
    chunks.extend(chunk_text(ptext, source="data_activation_playbook"))

    print(f"  CSV narratives: {len(chunks)} chunks")
    return chunks

def build_index():
    print("\n🔧 Building BM25 knowledge base...\n")
    all_chunks = load_documents() + csv_to_narrative_chunks()
    print(f"\nTotal chunks: {len(all_chunks)}")
    bm25 = BM25Okapi([tokenize(c["text"]) for c in all_chunks])
    with open(INDEX_FILE, "wb") as f:
        pickle.dump({"bm25": bm25, "chunks": all_chunks}, f)
    print(f"✅ BM25 index saved — {len(all_chunks)} chunks indexed")
    return {"bm25": bm25, "chunks": all_chunks}

if __name__ == "__main__":
    build_index()
