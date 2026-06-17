import numpy as np
import pandas as pd
import scipy.stats as stats
import streamlit as st

from src.helpers import ALPHA, cohen_d_independent, cohen_d_one_sample, cohen_d_paired, decision_text, display_hypotheses, effect_label, require_categorical_columns, require_dataset, require_numeric_columns, sample_table
from src.style import apply_style, configure_page, footer, hero

configure_page("T-test lab")
apply_style()
hero(
    "T-test lab",
    "Run one-sample, independent two-sample, or paired-sample t-tests and interpret the result at α = 0.05.",
    "Parametric mean tests",
)

df = require_dataset()
num_cols = require_numeric_columns(df)
mode = st.radio("Test type", ["One-sample", "Independent two-sample", "Paired sample"], horizontal=True)

if mode == "One-sample":
    col = st.selectbox("Numerical variable", num_cols)
    mu0 = st.number_input("Hypothesized population mean", value=0.0)
    x = df[col].dropna()

    if len(x) < 2:
        st.error("At least 2 valid observations are needed.")
        st.stop()

    display_hypotheses(f"μ = {mu0}", f"μ ≠ {mu0}")
    t_stat, p_val = stats.ttest_1samp(x, popmean=mu0)
    d = cohen_d_one_sample(x, mu0)

    table = pd.DataFrame(
        [
            ("Sample size", len(x)),
            ("Sample mean", round(float(x.mean()), 4)),
            ("Sample SD", round(float(x.std(ddof=1)), 4)),
            ("Mean difference", round(float(x.mean() - mu0), 4)),
            ("Degrees of freedom", len(x) - 1),
            ("t statistic", round(float(t_stat), 4)),
            ("p value", round(float(p_val), 4)),
            ("Cohen's d", round(float(d), 4)),
            ("Effect size", effect_label(d)),
            ("Decision", decision_text(p_val)),
        ],
        columns=["Measure", "Value"],
    )
    st.dataframe(table, use_container_width=True, hide_index=True)

elif mode == "Independent two-sample":
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

    if len(a) < 2 or len(b) < 2:
        st.error("Each group needs at least 2 valid observations.")
        st.stop()

    display_hypotheses(f"μ({g1}) = μ({g2})", f"μ({g1}) ≠ μ({g2})")
    levene_stat, levene_p = stats.levene(a, b)
    equal_var = bool(levene_p >= ALPHA)
    t_stat, p_val = stats.ttest_ind(a, b, equal_var=equal_var)
    dfree = len(a) + len(b) - 2 if equal_var else "Welch approximation"
    d = cohen_d_independent(a, b)

    st.subheader("Group summary")
    st.dataframe(sample_table({str(g1): a, str(g2): b}), use_container_width=True, hide_index=True)
    st.info(f"Levene variance check: p = {levene_p:.4f}. Equal variance used: {equal_var}")

    table = pd.DataFrame(
        [
            ("Mean difference", round(float(a.mean() - b.mean()), 4)),
            ("Degrees of freedom", dfree),
            ("t statistic", round(float(t_stat), 4)),
            ("p value", round(float(p_val), 4)),
            ("Cohen's d", round(float(d), 4)),
            ("Effect size", effect_label(d)),
            ("Decision", decision_text(p_val)),
        ],
        columns=["Measure", "Value"],
    )
    st.dataframe(table, use_container_width=True, hide_index=True)

else:
    first = st.selectbox("First paired numerical variable", num_cols)
    second_options = [c for c in num_cols if c != first]
    if not second_options:
        st.error("A paired test needs two numerical variables.")
        st.stop()
    second = st.selectbox("Second paired numerical variable", second_options)

    pair_df = df[[first, second]].dropna()
    if len(pair_df) < 2:
        st.error("At least 2 complete pairs are needed.")
        st.stop()

    display_hypotheses(f"Mean paired difference between {first} and {second} = 0", "Mean paired difference is not 0")
    t_stat, p_val = stats.ttest_rel(pair_df[first], pair_df[second])
    d = cohen_d_paired(pair_df[first], pair_df[second])
    diff = pair_df[first] - pair_df[second]

    table = pd.DataFrame(
        [
            ("Complete pairs", len(pair_df)),
            ("Mean difference", round(float(diff.mean()), 4)),
            ("SD of differences", round(float(diff.std(ddof=1)), 4)),
            ("Degrees of freedom", len(pair_df) - 1),
            ("t statistic", round(float(t_stat), 4)),
            ("p value", round(float(p_val), 4)),
            ("Cohen's dz", round(float(d), 4)),
            ("Effect size", effect_label(d)),
            ("Decision", decision_text(p_val)),
        ],
        columns=["Measure", "Value"],
    )
    st.dataframe(table, use_container_width=True, hide_index=True)

p_show = locals().get("p_val")
if p_show is not None:
    if p_show < ALPHA:
        st.error("Reject H₀: the observed mean difference is statistically significant.")
    else:
        st.success("Fail to reject H₀: the observed mean difference is not statistically significant.")

footer()
