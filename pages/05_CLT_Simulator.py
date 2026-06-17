import numpy as np
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
import matplotlib.pyplot as plt
import streamlit as st

from src.style import apply_style, configure_page, footer, hero

configure_page("CLT simulator")
apply_style()
hero(
    "Central Limit Theorem simulator",
    "Watch the sampling distribution of the mean become more normal as sample size and repeated sampling increase.",
    "Simulation lab",
)

with st.sidebar:
    st.header("Simulation controls")
    population_type = st.selectbox(
        "Population shape",
        ["Exponential / skewed", "Uniform", "Bimodal mixture", "Poisson count"],
    )
    sample_size = st.slider("Sample size per draw", 2, 250, 30)
    repetitions = st.slider("Number of repeated samples", 100, 5000, 1000, step=100)
    seed = st.number_input("Random seed", value=42, step=1)

rng = np.random.default_rng(int(seed))
population_size = 50_000

if population_type == "Exponential / skewed":
    population = rng.exponential(scale=2.0, size=population_size)
elif population_type == "Uniform":
    population = rng.uniform(low=0, high=10, size=population_size)
elif population_type == "Poisson count":
    population = rng.poisson(lam=4, size=population_size)
else:
    a = rng.normal(loc=-2.0, scale=0.8, size=population_size // 2)
    b = rng.normal(loc=3.0, scale=1.1, size=population_size // 2)
    population = np.concatenate([a, b])

sample_means = np.array([rng.choice(population, size=sample_size, replace=True).mean() for _ in range(repetitions)])

m1, m2, m3, m4 = st.columns(4)
m1.metric("Population mean", f"{population.mean():.4f}")
m2.metric("Mean of sample means", f"{sample_means.mean():.4f}")
m3.metric("Population SD", f"{population.std(ddof=1):.4f}")
m4.metric("SE of means", f"{sample_means.std(ddof=1):.4f}")

left, right = st.columns(2)
with left:
    fig, ax = plt.subplots(figsize=(6.5, 4.3))
    ax.hist(population, bins=45, edgecolor="black")
    ax.set_title("Original population")
    ax.set_xlabel("Value")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

with right:
    fig, ax = plt.subplots(figsize=(6.5, 4.3))
    ax.hist(sample_means, bins=45, density=True, edgecolor="black")
    grid = np.linspace(sample_means.min(), sample_means.max(), 250)
    ax.plot(grid, stats.norm.pdf(grid, sample_means.mean(), sample_means.std(ddof=1)))
    ax.set_title("Sampling distribution of the mean")
    ax.set_xlabel("Sample mean")
    ax.set_ylabel("Density")
    st.pyplot(fig)

st.subheader("Q-Q plot of sample means")
fig = sm.qqplot(sample_means, line="s", fit=True)
plt.title("Normal Q-Q plot")
st.pyplot(fig)

if len(sample_means) <= 5000:
    stat, p = stats.shapiro(sample_means)
    st.info(f"Shapiro-Wilk on sample means: statistic = {stat:.4f}, p = {p:.4f}")

st.write(
    "As the sample size grows, the distribution of repeated sample means usually becomes closer to normal, "
    "even when the original population is skewed or non-normal."
)

footer()
