import numpy as np
import pandas as pd
import scipy.stats as stats
import streamlit as st

from src.helpers import ALPHA, decision_text, display_hypotheses, require_categorical_columns, require_dataset, require_numeric_columns, sample_table
from src.style import apply_style, configure_page, footer, hero

configure_page("Nonparametric suite")
apply_style()
hero(
    "Nonparametric suite",
    "Use rank-based tests when normality or parametric assumptions are not suitable.",
    "Distribution-free tests",
)

df = require_dataset()
num_cols = require_numeric_columns(df)

test = st.selectbox(
    "Select procedure",
    ["Mann-Whitney U", "Wilcoxon signed-rank", "Kruskal-Wallis", "Friedman"],
)

if test == "Mann-Whitney U":
    cat_cols = require_categorical_columns(df)
    value_col = st.selectbox("Numerical variable", num_cols)
    group_col = st.selectbox("Grouping variable", cat_cols)
    levels = df[group_col].dropna().unique().tolist()

    if len(levels) < 2:
        st.error("Mann-Whitney U needs two groups.")
        st.stop()

    g1 = st.selectbox("First group", levels, index=0)
    g2 = st.selectbox("Second group", levels, index=1)
    a = df.loc[df[group_col] == g1, value_col].dropna()
    b = df.loc[df[group_col] == g2, value_col].dropna()

    display_hypotheses(f"The distributions of {g1} and {g2} are the same.", "The two distributions are different.")
    stat, p_val = stats.mannwhitneyu(a, b, alternative="two-sided")
    rank_biserial = 1 - (2 * stat) / (len(a) * len(b))

    st.subheader("Group summary")
    st.dataframe(sample_table({str(g1): a, str(g2): b}), use_container_width=True, hide_index=True)

    rows = [
        ("U statistic", round(float(stat), 4)),
        ("p value", round(float(p_val), 4)),
        ("Rank-biserial correlation", round(float(rank_biserial), 4)),
        ("Decision", decision_text(p_val)),
    ]

elif test == "Wilcoxon signed-rank":
    first = st.selectbox("First paired variable", num_cols)
    second_candidates = [c for c in num_cols if c != first]
    if not second_candidates:
        st.error("Wilcoxon signed-rank needs two numerical variables.")
        st.stop()
    second = st.selectbox("Second paired variable", second_candidates)
    pairs = df[[first, second]].dropna()

    display_hypotheses(f"The median paired difference between {first} and {second} is zero.", "The median paired difference is not zero.")
    stat, p_val = stats.wilcoxon(pairs[first], pairs[second])
    diff = pairs[first] - pairs[second]

    rows = [
        ("Complete pairs", len(pairs)),
        ("Median difference", round(float(diff.median()), 4)),
        ("W statistic", round(float(stat), 4)),
        ("p value", round(float(p_val), 4)),
        ("Decision", decision_text(p_val)),
    ]

elif test == "Kruskal-Wallis":
    cat_cols = require_categorical_columns(df)
    value_col = st.selectbox("Numerical variable", num_cols)
    group_col = st.selectbox("Grouping variable", cat_cols)
    clean = df[[value_col, group_col]].dropna()
    levels = clean[group_col].unique().tolist()

    if len(levels) < 2:
        st.error("Kruskal-Wallis needs at least two groups.")
        st.stop()

    groups = {str(level): clean.loc[clean[group_col] == level, value_col] for level in levels}
    display_hypotheses("All groups come from the same distribution.", "At least one group distribution differs.")
    stat, p_val = stats.kruskal(*groups.values())

    st.subheader("Group summary")
    st.dataframe(sample_table(groups), use_container_width=True, hide_index=True)

    rows = [
        ("H statistic", round(float(stat), 4)),
        ("Degrees of freedom", len(groups) - 1),
        ("p value", round(float(p_val), 4)),
        ("Decision", decision_text(p_val)),
    ]

else:
    chosen = st.multiselect("Repeated-measure numerical variables", num_cols, default=num_cols[: min(3, len(num_cols))])
    if len(chosen) < 3:
        st.error("Friedman test needs at least three related numerical variables.")
        st.stop()

    wide = df[chosen].dropna()
    if len(wide) < 2:
        st.error("At least two complete rows are needed.")
        st.stop()

    display_hypotheses("The repeated measures have the same distribution.", "At least one repeated measure differs.")
    stat, p_val = stats.friedmanchisquare(*[wide[col] for col in chosen])

    summary = pd.DataFrame(
        {"Variable": chosen, "Median": [round(float(wide[col].median()), 4) for col in chosen], "Valid rows": len(wide)}
    )
    st.subheader("Repeated-measure summary")
    st.dataframe(summary, use_container_width=True, hide_index=True)

    rows = [
        ("Friedman statistic", round(float(stat), 4)),
        ("Degrees of freedom", len(chosen) - 1),
        ("p value", round(float(p_val), 4)),
        ("Decision", decision_text(p_val)),
    ]

st.subheader("Test result")
st.dataframe(pd.DataFrame(rows, columns=["Measure", "Value"]), use_container_width=True, hide_index=True)

if p_val < ALPHA:
    st.error("Reject H₀: the nonparametric result is statistically significant.")
else:
    st.success("Fail to reject H₀: the nonparametric result is not statistically significant.")

footer()
