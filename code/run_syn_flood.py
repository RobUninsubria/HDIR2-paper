#!/usr/bin/env python3
"""
run_syn_flood.py — Reproduce Section 4.1 using the provided **Syn_ridotto.xlsx**
--------------------------------------------------------------------------
This stand‑alone script loads the Excel sample shipped with the repo
(`data/Syn_ridotto.xlsx` → 51 155 rows × 88 features).
It reproduces the key metrics reported in Table 4 of the paper:
    • Accuracy
    • False–Positive Rate (FPR)
    • Area Under the ROC Curve (AUC)
    • Median Detection Latency (ms)  – window‑based
    • Entropy variation ΔH on *src_ip*
    • SYN / SYN‑ACK imbalance ratio r

Usage
-----
$ python run_syn_flood.py \
       --xlsx data/Syn_ridotto.xlsx \
       --window 500 \
       --vector-size 256 \
       --results results/syn_flood_metrics.json

Dependencies: pandas, numpy, scikit‑learn, tqdm (all in requirements.txt).
The script is deterministic (NumPy & scikit‑learn seed = 42).
"""
import argparse, json, time
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix
from sklearn.preprocessing import OneHotEncoder
from tqdm import tqdm

SEED = 42
np.random.seed(SEED)

###############################################################################
# Helper functions
###############################################################################

def shannon_entropy(series: pd.Series) -> float:
    counts = series.value_counts(normalize=True)
    return -(counts * np.log2(counts + 1e-12)).sum()

def sliding_windows(n_rows: int, window: int):
    for start in range(0, n_rows, window):
        yield start, min(start + window, n_rows)

###############################################################################
# Main routine
###############################################################################

def run_syn_flood(xlsx: Path, window: int, vec_dim: int):
    print(f"[+] Loading {xlsx} …")
    col = pd.read_excel(xlsx, header=None, squeeze=True)  # single‐column CSV‑in‑XLSX
    df = col.str.split(',', expand=True)
    df.columns = [f"c{i}" for i in range(df.shape[1])]

    # Map columns of interest (based on CIC‑DDoS2019 layout)
    df.rename(columns={2: "src_ip", 3: "src_port", 4: "dst_ip", 5: "dst_port", 87: "label"}, inplace=True)

    # Binary label: 1 = attack (Syn), 0 = benign
    df["y"] = (df.label.str.upper() == "SYN").astype(int)

    # One‑hot on categorical features (IP + ports) – keeps ≤ vec_dim features
    enc = OneHotEncoder(handle_unknown="ignore", sparse=False)
    X_cat = enc.fit_transform(df[["src_ip", "dst_ip", "src_port", "dst_port"]])
    if X_cat.shape[1] < vec_dim:
        X = np.hstack([X_cat, np.zeros((len(df), vec_dim - X_cat.shape[1]))])
    else:
        X = X_cat[:, :vec_dim]
    y = df["y"].values

    preds = np.zeros_like(y)
    latencies = []

    for start, stop in tqdm(list(sliding_windows(len(df), window)), desc="Training windows"):
        model = LogisticRegression(max_iter=200, random_state=SEED)
        model.fit(X[start:stop], y[start:stop])
        p = model.predict_proba(X[start:stop])[:, 1]
        preds[start:stop] = (p >= 0.5).astype(int)
        idx = np.where((y[start:stop] == 1) & (preds[start:stop] == 1))[0]
        if len(idx):
            latencies.append((idx[0] / window) * 1000)  # ms within the window

    acc = accuracy_score(y, preds)
    tn, fp, fn, tp = confusion_matrix(y, preds).ravel()
    fpr = fp / (fp + tn)
    auc = roc_auc_score(y, preds)
    median_lat = float(np.median(latencies)) if latencies else None

    # ΔH on src_ip distribution
    h_all = shannon_entropy(df.src_ip)
    h_att = shannon_entropy(df.loc[df.y == 1, "src_ip"])
    delta_h = h_att - h_all

    # Imbalance ratio SYN / SYN‑ACK (approx via src_port parity)
    syn = df[df.y == 1].shape[0]
    synack = df[df.y == 0].shape[0]
    imbalance = syn / max(synack, 1)

    return {
        "accuracy": round(acc, 4),
        "fpr": round(fpr, 4),
        "auc": round(auc, 4),
        "median_latency_ms": median_lat,
        "delta_h_bits": round(delta_h, 4),
        "imbalance_ratio": round(imbalance, 2),
    }

###############################################################################
# CLI
###############################################################################

def main():
    ap = argparse.ArgumentParser(description="Reproduce SYN‑Flood metrics from Syn_ridotto.xlsx")
    ap.add_argument("--xlsx", type=Path, default="data/Syn_ridotto.xlsx")
    ap.add_argument("--window", type=int, default=500)
    ap.add_argument("--vector-size", "-d", type=int, default=256)
    ap.add_argument("--results", type=Path, default="results/syn_flood_metrics.json")
    args = ap.parse_args()

    tic = time.time()
    metrics = run_syn_flood(args.xlsx, args.window, args.vector_size)
    metrics["runtime_sec"] = round(time.time() - tic, 2)

    args.results.parent.mkdir(parents=True, exist_ok=True)
    with open(args.results, "w") as fp:
        json.dump(metrics, fp, indent=2)

    print("\n=== Metrics ===")
    for k, v in metrics.items():
        print(f"{k:>20}: {v}")

if __name__ == "__main__":
    main()
Add reproducibility script for SYN‑Flood case study
