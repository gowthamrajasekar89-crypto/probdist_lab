import numpy as np
import pandas as pd
import streamlit as st
from statsmodels.stats.weightstats import ztest

from src.helpers import ALPHA, decision_text, display_hypotheses, require_categorical_columns, require_dataset, require_numeric_columns, sample_table
from src.style import apply_style, configure_page, footer, hero

configure_page("Z-test lab")
apply_style()
hero(
    "Z-test lab",
    "Use one-sample or two-sample z-tests for large-sample mean comparisons.",
    "Large-sample tests",
)

df = require_dataset()
num_cols = require_numeric_columns(df)
mode = st.radio("Z-test type", ["One-sample", "Two-sample"], horizontal=True)

if mode == "One-sample":
    col = st.selectbox("Numerical variable", num_cols)
    mu0 = st.number_input("Hypothesized mean", value=0.0)
    x = df[col].dropna()

    if len(x) < 30:
        st.warning("Z-tests are usually more appropriate for large samples. Consider a t-test for small samples.")

    display_hypotheses(f"μ = {mu0}", f"μ ≠ {mu0}")
    z_stat, p_val = ztest(x, value=mu0)
    se = x.std(ddof=1) / np.sqrt(len(x))

    table = pd.DataFrame(
        [
            ("Sample size", len(x)),
            ("Sample mean", round(float(x.mean()), 4)),
            ("Sample SD", round(float(x.std(ddof=1)), 4)),
            ("Standard error", round(float(se), 4)),
            ("Mean difference", round(float(x.mean() - mu0), 4)),
            ("z statistic", round(float(z_stat), 4)),
            ("p value", round(float(p_val), 4)),
            ("Decision", decision_text(p_val)),
        ],
        columns=["Measure", "Value"],
    )
    st.dataframe(table, use_container_width=True, hide_index=True)

else:
    cat_cols = require_categorical_columns(df)
    value_col = st.selectbox("Numerical variable", num_cols)
    group_col = st.selectbox("Group variable", cat_cols)
    levels = df[group_col].dropna().unique().tolist()

    if len(levels) < 2:
        st.error("The selected group column needs at least two groups.")
        st.stop()

    g1 = st.selectbox("First group", levels, index=0)
    g2 = st.selectbox("Second group", levels, index=1)
    a = df.loc[df[group_col] == g1, value_col].dropna()
    b = df.loc[df[group_col] == g2, value_col].dropna()

    if len(a) < 30 or len(b) < 30:
        st.warning("Two-sample z-tests are usually recommended when both samples are large.")

    display_hypotheses(f"μ({g1}) = μ({g2})", f"μ({g1}) ≠ μ({g2})")
    z_stat, p_val = ztest(a, b)
    se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))

    st.subheader("Group summary")
    st.dataframe(sample_table({str(g1): a, str(g2): b}), use_container_width=True, hide_index=True)

    table = pd.DataFrame(
        [
            ("Mean difference", round(float(a.mean() - b.mean()), 4)),
            ("Standard error", round(float(se), 4)),
            ("z statistic", round(float(z_stat), 4)),
            ("p value", round(float(p_val), 4)),
            ("Decision", decision_text(p_val)),
        ],
        columns=["Measure", "Value"],
    )
    st.dataframe(table, use_container_width=True, hide_index=True)

if p_val < ALPHA:
    st.error("Reject H₀: the mean comparison is statistically significant.")
else:
    st.success("Fail to reject H₀: the mean comparison is not statistically significant.")

footer()
