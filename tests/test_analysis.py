import os

import numpy as np
import pandas as pd
import pytest

from business_analysis.analysis import (
    load_transactions,
    add_settled_flag,
    build_daily_summary,
)

DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "business_metrics.csv"
)


@pytest.fixture
def raw_df():
    return load_transactions(DATA_PATH)


def test_load_dtypes(raw_df):
    assert pd.api.types.is_numeric_dtype(raw_df["amount"])
    assert pd.api.types.is_datetime64_any_dtype(raw_df["txn_date"])


def test_missing_amount_preserved_as_nan(raw_df):
    assert raw_df["amount"].isna().sum() == 2


def test_missing_required_columns():
    bad = pd.DataFrame({"account_id": ["A"], "amount": [1.0]})
    bad_path = os.path.join(os.path.dirname(__file__), "_bad.csv")
    bad.to_csv(bad_path, index=False)
    try:
        with pytest.raises(ValueError):
            load_transactions(bad_path)
    finally:
        os.remove(bad_path)


def test_settled_flag_handles_casing_and_spaces(raw_df):
    flagged = add_settled_flag(raw_df)
    assert flagged["is_settled"].sum() == 11


def test_summary_grouped_by_date_and_account(raw_df):
    summary = build_daily_summary(raw_df)
    assert {"account_id", "txn_date", "total_amount", "txn_count"}.issubset(
        summary.columns
    )


def test_summary_totals_and_counts(raw_df):
    summary = build_daily_summary(raw_df)
    summary = summary.copy()
    summary["txn_date"] = pd.to_datetime(summary["txn_date"]).dt.strftime("%Y-%m-%d")

    def row(acc, date):
        sub = summary[
            (summary["account_id"] == acc) & (summary["txn_date"] == date)
        ]
        assert len(sub) == 1
        return sub.iloc[0]

    r = row("ACC001", "2024-03-01")
    assert r["total_amount"] == pytest.approx(200.50)
    assert r["txn_count"] == 2

    r = row("ACC002", "2024-03-01")
    assert r["total_amount"] == pytest.approx(350.00)
    assert r["txn_count"] == 3

    r = row("ACC001", "2024-03-02")
    assert r["total_amount"] == pytest.approx(75.75)
    assert r["txn_count"] == 2

    r = row("ACC002", "2024-03-02")
    assert r["total_amount"] == pytest.approx(500.00)
    assert r["txn_count"] == 1

    r = row("ACC003", "2024-03-01")
    assert r["total_amount"] == pytest.approx(99.99)
    assert r["txn_count"] == 1


def test_settled_count_excludes_other_statuses(raw_df):
    summary = build_daily_summary(raw_df)
    assert summary["txn_count"].sum() == 11
