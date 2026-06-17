import numpy as np
import pandas as pd
import scipy.stats as stats
import streamlit as st

from src.helpers import ALPHA, cramers_v_from_table, decision_text, display_hypotheses, parse_ratio_string, require_categorical_columns, require_dataset
from src.style import apply_style, configure_page, footer, hero

configure_page("Chi-square studio")
apply_style()
hero(
    "Chi-square studio",
    "Analyze categorical data using a test of independence or a goodness-of-fit test.",
    "Categorical testing",
)

df = require_dataset()
cat_cols = require_categorical_columns(df)

mode = st.radio("Chi-square procedure", ["Independence test", "Goodness-of-fit"], horizontal=True)

if mode == "Independence test":
    if len(cat_cols) < 2:
        st.error("The independence test needs two categorical variables.")
        st.stop()

    first = st.selectbox("First categorical variable", cat_cols)
    second = st.selectbox("Second categorical variable", [c for c in cat_cols if c != first])
    table = pd.crosstab(df[first], df[second])

    display_hypotheses(f"{first} and {second} are independent.", f"{first} and {second} are associated.")
    st.subheader("Observed frequency table")
    st.dataframe(table, use_container_width=True)

    chi2, p_val, dof, expected = stats.chi2_contingency(table)
    expected_df = pd.DataFrame(expected, index=table.index, columns=table.columns)
    low_cells = int((expected < 5).sum())
    v = cramers_v_from_table(table, chi2)

    st.subheader("Expected frequency table")
    st.dataframe(expected_df, use_container_width=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("χ²", f"{chi2:.4f}")
    c2.metric("df", dof)
    c3.metric("p value", f"{p_val:.4f}")
    c4.metric("Cramer's V", f"{v:.4f}")

    if low_cells == 0:
        st.success("Expected-frequency assumption satisfied: no expected cell is below 5.")
    else:
        st.warning(f"{low_cells} expected cell(s) are below 5. Interpret with care.")

else:
    variable = st.selectbox("Categorical variable", cat_cols)
    observed = df[variable].dropna().value_counts().sort_index()

    display_hypotheses(f"{variable} follows the expected category proportions.", f"{variable} does not follow the expected category proportions.")
    st.subheader("Observed counts")
    st.dataframe(observed.to_frame("Observed"), use_container_width=True)

    expected_type = st.radio("Expected proportions", ["Uniform", "Custom ratios"], horizontal=True)
    if expected_type == "Uniform":
        proportions = np.ones(len(observed)) / len(observed)
    else:
        default = ", ".join(["1"] * len(observed))
        ratio_text = st.text_input("Enter ratios in category order, separated by commas", default)
        try:
            proportions = parse_ratio_string(ratio_text, len(observed))
        except Exception as exc:
            st.error(str(exc))
            st.stop()

    expected = proportions * observed.sum()
    expected_df = pd.DataFrame({"Observed": observed.values, "Expected": expected}, index=observed.index)
    st.subheader("Observed vs expected")
    st.dataframe(expected_df, use_container_width=True)

    chi2, p_val = stats.chisquare(f_obs=observed.values, f_exp=expected)
    dof = len(observed) - 1

    c1, c2, c3 = st.columns(3)
    c1.metric("χ²", f"{chi2:.4f}")
    c2.metric("df", dof)
    c3.metric("p value", f"{p_val:.4f}")

if p_val < ALPHA:
    st.error(f"{decision_text(p_val)}: the categorical pattern is statistically significant.")
else:
    st.success(f"{decision_text(p_val)}: the evidence is not statistically significant.")

footer()
