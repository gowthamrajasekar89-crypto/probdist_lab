import numpy as np
import pandas as pd
import scipy.stats as stats
import streamlit as st
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd

from src.helpers import ALPHA, decision_text, display_hypotheses, effect_label, require_categorical_columns, require_dataset, require_numeric_columns, sample_table
from src.style import apply_style, configure_page, footer, hero

configure_page("ANOVA workbench")
apply_style()
hero(
    "ANOVA workbench",
    "Compare group means using one-way or two-way ANOVA, with assumption checks and effect-size interpretation.",
    "Hypothesis testing",
)

df = require_dataset()
num_cols = require_numeric_columns(df)
cat_cols = require_categorical_columns(df)

analysis_type = st.radio("ANOVA design", ["One-way ANOVA", "Two-way ANOVA"], horizontal=True)
response = st.selectbox("Response / numerical variable", num_cols)

if analysis_type == "One-way ANOVA":
    factor = st.selectbox("Grouping factor", cat_cols)
    clean = df[[response, factor]].dropna()
    levels = clean[factor].unique().tolist()

    if len(levels) < 2:
        st.error("One-way ANOVA needs at least two groups.")
        st.stop()

    display_hypotheses(
        f"All group means of {response} are equal across {factor}.",
        f"At least one group mean of {response} differs across {factor}.",
    )

    groups = {str(level): clean.loc[clean[factor] == level, response] for level in levels}
    st.subheader("Group summary")
    st.dataframe(sample_table(groups), use_container_width=True, hide_index=True)

    st.subheader("Assumption checks")
    normal_rows = []
    for label, values in groups.items():
        if len(values) >= 3 and len(values) <= 5000:
            stat, p = stats.shapiro(values)
            normal_rows.append({"Group": label, "Shapiro p": round(float(p), 4), "Decision": decision_text(p)})
        else:
            normal_rows.append({"Group": label, "Shapiro p": "Skipped", "Decision": "Need 3–5000 rows"})
    st.dataframe(pd.DataFrame(normal_rows), use_container_width=True, hide_index=True)

    levene_stat, levene_p = stats.levene(*groups.values())
    st.info(f"Levene variance check: statistic = {levene_stat:.4f}, p = {levene_p:.4f}")

    f_stat, p_val = stats.f_oneway(*groups.values())
    grand_mean = clean[response].mean()
    ss_between = sum(len(vals) * (vals.mean() - grand_mean) ** 2 for vals in groups.values())
    ss_total = sum((clean[response] - grand_mean) ** 2)
    eta_squared = float(ss_between / ss_total) if ss_total else np.nan

    st.subheader("ANOVA result")
    result = pd.DataFrame(
        [
            ("F statistic", round(float(f_stat), 4)),
            ("p value", round(float(p_val), 4)),
            ("alpha", ALPHA),
            ("eta squared", round(eta_squared, 4)),
            ("effect size reading", effect_label(eta_squared, "eta")),
            ("decision", decision_text(p_val)),
        ],
        columns=["Measure", "Value"],
    )
    st.dataframe(result, use_container_width=True, hide_index=True)

    if p_val < ALPHA and len(levels) >= 2:
        st.subheader("Post-hoc Tukey comparison")
        tukey = pairwise_tukeyhsd(endog=clean[response], groups=clean[factor], alpha=ALPHA)
        tukey_df = pd.DataFrame(data=tukey._results_table.data[1:], columns=tukey._results_table.data[0])
        st.dataframe(tukey_df, use_container_width=True, hide_index=True)

    if p_val < ALPHA:
        st.error("Reject H₀: at least one group mean appears different.")
    else:
        st.success("Fail to reject H₀: the evidence does not show a significant group-mean difference.")

else:
    if len(cat_cols) < 2:
        st.error("Two-way ANOVA needs two categorical factors.")
        st.stop()

    factor_a = st.selectbox("First factor", cat_cols, index=0)
    factor_b_options = [c for c in cat_cols if c != factor_a]
    factor_b = st.selectbox("Second factor", factor_b_options, index=0)

    clean = df[[response, factor_a, factor_b]].dropna()
    if clean[factor_a].nunique() < 2 or clean[factor_b].nunique() < 2:
        st.error("Each factor must contain at least two levels.")
        st.stop()

    display_hypotheses(
        "Factor A, Factor B, and their interaction do not change the response mean.",
        "At least one main effect or the interaction changes the response mean.",
    )

    formula = f'Q("{response}") ~ C(Q("{factor_a}")) + C(Q("{factor_b}")) + C(Q("{factor_a}")):C(Q("{factor_b}"))'
    model = ols(formula, data=clean).fit()
    table = sm.stats.anova_lm(model, typ=2).reset_index().rename(columns={"index": "Source"})
    if "PR(>F)" in table.columns:
        table["Decision"] = table["PR(>F)"].apply(lambda p: decision_text(float(p)) if pd.notna(p) else "")
    st.subheader("Two-way ANOVA table")
    st.dataframe(table, use_container_width=True, hide_index=True)

    st.subheader("Cell means")
    means = clean.groupby([factor_a, factor_b])[response].agg(["count", "mean", "std"]).reset_index()
    st.dataframe(means, use_container_width=True, hide_index=True)

footer()
