import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from src.helpers import require_dataset, require_numeric_columns
from src.style import apply_style, configure_page, footer, hero

configure_page("Visual explorer")
apply_style()
hero(
    "Visual explorer",
    "Inspect a numerical variable through distribution, spread, frequency, and cumulative views.",
    "Data visualization",
)

df = require_dataset()
num_cols = require_numeric_columns(df)

selected = st.selectbox("Numerical variable", num_cols)
x = df[selected].dropna()

if x.empty:
    st.error("The selected variable has no usable values.")
    st.stop()

unique_ratio = x.nunique() / len(x)
integer_like = np.allclose(x, np.round(x))
variable_type = "Discrete" if unique_ratio < 0.10 or integer_like else "Continuous"
st.info(f"Detected variable style: **{variable_type}**")

tab1, tab2, tab3, tab4 = st.tabs(["Histogram", "Box plot", "Frequency / PMF", "Empirical CDF"])

with tab1:
    bins = st.slider("Number of bins", min_value=5, max_value=80, value=25)
    fig, ax = plt.subplots(figsize=(8, 4.6))
    ax.hist(x, bins=bins, edgecolor="black")
    ax.set_title(f"Histogram of {selected}")
    ax.set_xlabel(selected)
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

with tab2:
    fig, ax = plt.subplots(figsize=(7, 3.8))
    ax.boxplot(x, vert=False)
    ax.set_title(f"Box plot of {selected}")
    ax.set_xlabel(selected)
    st.pyplot(fig)

with tab3:
    if variable_type == "Discrete" and x.nunique() <= 60:
        freq = x.value_counts().sort_index()
        pmf = freq / freq.sum()
        freq_df = pd.DataFrame({"Value": freq.index, "Frequency": freq.values, "PMF": pmf.values})
        st.dataframe(freq_df, use_container_width=True, hide_index=True)
        fig, ax = plt.subplots(figsize=(8, 4.6))
        ax.bar(freq.index.astype(str), pmf.values)
        ax.set_title(f"Probability mass view for {selected}")
        ax.set_xlabel(selected)
        ax.set_ylabel("Probability")
        ax.tick_params(axis="x", rotation=45)
        st.pyplot(fig)
    else:
        st.write("For continuous variables, the histogram tab is the better frequency view.")

with tab4:
    ordered = np.sort(x)
    probs = np.arange(1, len(ordered) + 1) / len(ordered)
    fig, ax = plt.subplots(figsize=(8, 4.6))
    ax.step(ordered, probs, where="post")
    ax.set_title(f"Empirical CDF of {selected}")
    ax.set_xlabel(selected)
    ax.set_ylabel("Cumulative probability")
    st.pyplot(fig)

footer()
