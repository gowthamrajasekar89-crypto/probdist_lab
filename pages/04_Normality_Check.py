import numpy as np
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
import matplotlib.pyplot as plt
import streamlit as st

from src.helpers import ALPHA, decision_text, display_hypotheses, evidence_sentence, require_dataset, require_numeric_columns
from src.style import apply_style, configure_page, footer, hero

configure_page("Normality check")
apply_style()
hero(
    "Normality check",
    "Evaluate whether a numerical variable follows a normal distribution using tests and graphical diagnostics.",
    "Assumption testing",
)

df = require_dataset()
num_cols = require_numeric_columns(df)

selected = st.selectbox("Numerical variable", num_cols)
x = df[selected].dropna()

if len(x) < 3:
    st.error("At least 3 observations are required for normality testing.")
    st.stop()

display_hypotheses(
    "The variable follows a normal distribution.",
    "The variable does not follow a normal distribution.",
)

results = []

if len(x) <= 5000:
    stat, p = stats.shapiro(x)
    results.append(("Shapiro-Wilk", stat, p, decision_text(p)))
else:
    st.warning("Shapiro-Wilk is skipped for samples above 5000 observations.")

ks_stat, ks_p = stats.kstest((x - x.mean()) / x.std(ddof=1), "norm")
results.append(("Kolmogorov-Smirnov", ks_stat, ks_p, decision_text(ks_p)))

ad = stats.anderson(x, dist="norm")
crit_5 = ad.critical_values[list(ad.significance_level).index(5.0)] if 5.0 in ad.significance_level else ad.critical_values[2]
ad_decision = "Reject H₀" if ad.statistic > crit_5 else "Fail to reject H₀"
results.append(("Anderson-Darling", ad.statistic, "5% critical value: " + str(round(float(crit_5), 4)), ad_decision))

st.subheader("Test results")
result_df = pd.DataFrame(results, columns=["Test", "Statistic", "P value / reference", "Decision"])
st.dataframe(result_df, use_container_width=True, hide_index=True)

st.subheader("Visual diagnostics")
left, right = st.columns(2)
with left:
    fig, ax = plt.subplots(figsize=(6, 4.2))
    ax.hist(x, bins=25, density=True, edgecolor="black")
    grid = np.linspace(x.min(), x.max(), 250)
    ax.plot(grid, stats.norm.pdf(grid, x.mean(), x.std(ddof=1)))
    ax.set_title("Histogram with fitted normal curve")
    st.pyplot(fig)

with right:
    fig = sm.qqplot(x, line="s", fit=True)
    plt.title("Q-Q plot")
    st.pyplot(fig)

st.subheader("Interpretation")
p_values = [row[2] for row in results if isinstance(row[2], (float, np.floating))]
if p_values:
    min_p = min(p_values)
    st.write(evidence_sentence(min_p, ALPHA))
st.write("Use this page before choosing between parametric and nonparametric tests.")

footer()
