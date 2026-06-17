import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import streamlit as st

from src.helpers import require_dataset, require_numeric_columns
from src.style import apply_style, configure_page, footer, hero

configure_page("Distribution fit")
apply_style()
hero(
    "Distribution fit",
    "Fit common probability distributions to a numerical column and compare them using the Kolmogorov-Smirnov statistic.",
    "Probability modeling",
)

df = require_dataset()
num_cols = require_numeric_columns(df)

selected = st.selectbox("Numerical variable", num_cols)
x = df[selected].dropna()

if len(x) < 5:
    st.error("At least 5 valid observations are recommended for distribution fitting.")
    st.stop()

candidate_map = {
    "Normal": stats.norm,
    "Exponential": stats.expon,
    "Uniform": stats.uniform,
}
chosen = st.multiselect("Distributions to compare", list(candidate_map), default=list(candidate_map))

if not chosen:
    st.warning("Select at least one distribution.")
    st.stop()

rows = []
fit_objects = {}
for name in chosen:
    dist = candidate_map[name]
    try:
        params = dist.fit(x)
        ks_stat, p_val = stats.kstest(x, dist.name, args=params)
        fit_objects[name] = (dist, params)
        rows.append(
            {
                "Distribution": name,
                "KS statistic": round(float(ks_stat), 4),
                "P value": round(float(p_val), 4),
                "Parameters": ", ".join([f"{p:.4g}" for p in params]),
            }
        )
    except Exception as exc:
        rows.append({"Distribution": name, "KS statistic": np.nan, "P value": np.nan, "Parameters": f"Fit failed: {exc}"})

result = pd.DataFrame(rows).sort_values("KS statistic", na_position="last")
st.subheader("Fit comparison")
st.dataframe(result, use_container_width=True, hide_index=True)

best = result.iloc[0]["Distribution"]
st.success(f"Best fit by the smallest KS statistic: **{best}**")

fig, ax = plt.subplots(figsize=(8, 4.8))
ax.hist(x, bins=30, density=True, alpha=0.55, edgecolor="black", label="Data")
grid = np.linspace(x.min(), x.max(), 350)
for name, (dist, params) in fit_objects.items():
    try:
        ax.plot(grid, dist.pdf(grid, *params), label=name)
    except Exception:
        pass
ax.set_title(f"Fitted distributions for {selected}")
ax.set_xlabel(selected)
ax.set_ylabel("Density")
ax.legend()
st.pyplot(fig)

footer()
