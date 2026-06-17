import numpy as np
import pandas as pd
import scipy.stats as stats
import streamlit as st

from src.helpers import require_dataset, require_numeric_columns
from src.style import apply_style, configure_page, footer, hero

configure_page("Descriptive review")
apply_style()
hero(
    "Descriptive review",
    "Summarize one numerical variable using central tendency, spread, shape, missing data, and IQR-based outlier detection.",
    "Exploratory statistics",
)

df = require_dataset()
num_cols = require_numeric_columns(df)

selected = st.selectbox("Choose a numerical variable", num_cols)
raw = df[selected]
x = raw.dropna()

if x.empty:
    st.error("The selected column has no valid numerical observations.")
    st.stop()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total rows", f"{len(raw):,}")
m2.metric("Valid values", f"{len(x):,}")
m3.metric("Missing", f"{int(raw.isna().sum()):,}")
m4.metric("Missing %", f"{raw.isna().mean() * 100:.2f}%")

q1 = x.quantile(0.25)
q3 = x.quantile(0.75)
iqr = q3 - q1
low = q1 - 1.5 * iqr
high = q3 + 1.5 * iqr
outliers = x[(x < low) | (x > high)]

summary = pd.DataFrame(
    [
        ("Mean", x.mean()),
        ("Median", x.median()),
        ("Mode", x.mode().iloc[0] if not x.mode().empty else np.nan),
        ("Minimum", x.min()),
        ("Maximum", x.max()),
        ("Range", x.max() - x.min()),
        ("Variance", x.var(ddof=1)),
        ("Standard deviation", x.std(ddof=1)),
        ("Q1", q1),
        ("Q3", q3),
        ("Interquartile range", iqr),
        ("Skewness", stats.skew(x, nan_policy="omit")),
        ("Kurtosis", stats.kurtosis(x, nan_policy="omit")),
    ],
    columns=["Statistic", "Value"],
)
summary["Value"] = summary["Value"].apply(lambda v: round(float(v), 4) if pd.notna(v) else v)
st.subheader("Statistical summary")
st.dataframe(summary, use_container_width=True, hide_index=True)

st.subheader("IQR outlier check")
c1, c2, c3 = st.columns(3)
c1.metric("Lower fence", f"{low:.4f}")
c2.metric("Upper fence", f"{high:.4f}")
c3.metric("Outliers", f"{len(outliers):,}")

if len(outliers):
    with st.expander("Show detected outlier values"):
        st.dataframe(outliers.to_frame(name=selected), use_container_width=True)
else:
    st.success("No IQR outliers were detected for this variable.")

st.subheader("Result Interpretation")
if abs(stats.skew(x, nan_policy="omit")) < 0.5:
    shape = "fairly balanced"
elif stats.skew(x, nan_policy="omit") > 0:
    shape = "right-skewed"
else:
    shape = "left-skewed"
st.write(
    f"The variable **{selected}** has {len(x)} usable values. "
    f"Its average is **{x.mean():.4f}**, the median is **{x.median():.4f}**, "
    f"and the distribution looks **{shape}** based on skewness."
)

footer()
