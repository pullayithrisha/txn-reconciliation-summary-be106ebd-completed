from __future__ import annotations

import numpy as np
import pandas as pd

REQUIRED_COLUMNS = ["account_id", "txn_date", "amount", "status"]


def load_transactions(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError("missing required columns")

    df["status"] = df["status"]
    return df


def add_settled_flag(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    flags = []
    for value in df["status"]:
        flags.append(value == "settled")
    df["is_settled"] = flags
    return df


def build_daily_summary(df: pd.DataFrame) -> pd.DataFrame:
    flagged = add_settled_flag(df)
    successful = flagged[flagged["is_settled"]]

    summary = (
        successful.groupby(["account_id"], as_index=False)
        .agg(total_amount=("amount", "sum"), txn_count=("amount", "count"))
    )
    return summary
