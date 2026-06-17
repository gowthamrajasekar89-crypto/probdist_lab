from __future__ import annotations

import io
from dataclasses import dataclass
from itertools import combinations
from typing import Iterable, Sequence

import numpy as np
import pandas as pd
import scipy.stats as stats
import streamlit as st


ALPHA = 0.05


def get_dataset() -> pd.DataFrame | None:
    return st.session_state.get("dataset")


def require_dataset() -> pd.DataFrame:
    df = get_dataset()
    if df is None:
        st.warning("Upload a CSV or Excel file from the Data Home page before opening this module.")
        st.stop()
    return df


def numeric_columns(df: pd.DataFrame) -> list[str]:
    return df.select_dtypes(include=[np.number]).columns.tolist()


def categorical_columns(df: pd.DataFrame) -> list[str]:
    return df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()


def require_numeric_columns(df: pd.DataFrame) -> list[str]:
    cols = numeric_columns(df)
    if not cols:
        st.error("No numerical columns were detected in the uploaded dataset.")
        st.stop()
    return cols


def require_categorical_columns(df: pd.DataFrame, minimum: int = 1) -> list[str]:
    cols = categorical_columns(df)
    if len(cols) < minimum:
        st.error(f"At least {minimum} categorical column(s) are required for this analysis.")
        st.stop()
    return cols


def load_uploaded_file(file) -> pd.DataFrame:
    name = file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(file)
    if name.endswith((".xlsx", ".xls")):
        return pd.read_excel(file)
    raise ValueError("Unsupported file type. Use CSV or Excel.")


def decision_text(p_value: float, alpha: float = ALPHA) -> str:
    return "Reject H₀" if p_value < alpha else "Fail to reject H₀"


def evidence_sentence(p_value: float, alpha: float = ALPHA) -> str:
    if p_value < alpha:
        return f"Because p = {p_value:.4f} is below α = {alpha}, the result is statistically significant."
    return f"Because p = {p_value:.4f} is not below α = {alpha}, the result is not statistically significant."


def display_hypotheses(null: str, alternative: str) -> None:
    left, right = st.columns(2)
    with left:
        st.info(f"**H₀**  \n{null}")
    with right:
        st.info(f"**H₁**  \n{alternative}")


def result_table(rows: list[tuple[str, object]], title: str = "Result summary") -> None:
    df = pd.DataFrame(rows, columns=["Measure", "Value"])
    st.subheader(title)
    st.dataframe(df, use_container_width=True, hide_index=True)


def sample_table(groups: dict[str, Sequence[float]]) -> pd.DataFrame:
    rows = []
    for label, values in groups.items():
        s = pd.Series(values).dropna()
        rows.append(
            {
                "Group": label,
                "n": int(s.count()),
                "Mean": round(float(s.mean()), 4) if len(s) else np.nan,
                "Median": round(float(s.median()), 4) if len(s) else np.nan,
                "Std. Dev.": round(float(s.std(ddof=1)), 4) if len(s) > 1 else np.nan,
            }
        )
    return pd.DataFrame(rows)


def cohen_d_one_sample(values: Sequence[float], hypothesized_mean: float) -> float:
    x = pd.Series(values).dropna()
    sd = x.std(ddof=1)
    return float((x.mean() - hypothesized_mean) / sd) if sd else np.nan


def cohen_d_independent(first: Sequence[float], second: Sequence[float]) -> float:
    a = pd.Series(first).dropna()
    b = pd.Series(second).dropna()
    n1, n2 = len(a), len(b)
    if n1 < 2 or n2 < 2:
        return np.nan
    pooled = np.sqrt(((n1 - 1) * a.var(ddof=1) + (n2 - 1) * b.var(ddof=1)) / (n1 + n2 - 2))
    return float((a.mean() - b.mean()) / pooled) if pooled else np.nan


def cohen_d_paired(first: Sequence[float], second: Sequence[float]) -> float:
    diff = pd.Series(first).reset_index(drop=True) - pd.Series(second).reset_index(drop=True)
    diff = diff.dropna()
    sd = diff.std(ddof=1)
    return float(diff.mean() / sd) if sd else np.nan


def effect_label(value: float, kind: str = "d") -> str:
    if pd.isna(value):
        return "Not available"
    v = abs(value)
    if kind == "eta":
        if v < 0.01:
            return "Very small"
        if v < 0.06:
            return "Small"
        if v < 0.14:
            return "Medium"
        return "Large"
    if v < 0.20:
        return "Negligible"
    if v < 0.50:
        return "Small"
    if v < 0.80:
        return "Medium"
    return "Large"


def cramers_v_from_table(table: pd.DataFrame, chi_square: float) -> float:
    n = table.to_numpy().sum()
    r, c = table.shape
    denom = n * max(min(r - 1, c - 1), 1)
    return float(np.sqrt(chi_square / denom)) if denom else np.nan


def parse_ratio_string(text: str, expected_len: int) -> np.ndarray:
    parts = [p.strip() for p in text.split(",") if p.strip()]
    if len(parts) != expected_len:
        raise ValueError(f"Enter exactly {expected_len} comma-separated ratios.")
    ratios = np.array([float(p) for p in parts], dtype=float)
    if np.any(ratios < 0) or ratios.sum() <= 0:
        raise ValueError("Ratios must be non-negative and their total must be greater than zero.")
    return ratios / ratios.sum()


def long_to_wide_complete(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    return df[cols].dropna().copy()


def fmt(x, digits: int = 4):
    if isinstance(x, (float, np.floating)):
        return round(float(x), digits)
    return x
