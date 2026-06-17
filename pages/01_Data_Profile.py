import numpy as np
import pandas as pd
import streamlit as st

from src.helpers import require_dataset
from src.style import apply_style, configure_page, footer, hero

configure_page("Data profile")
apply_style()
hero(
    "Data profile",
    "Review column types, missing values, duplicate rows, and quick quality indicators before choosing a statistical test.",
    "Dataset preparation",
)

df = require_dataset()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Rows", f"{df.shape[0]:,}")
m2.metric("Columns", f"{df.shape[1]:,}")
m3.metric("Missing cells", f"{int(df.isna().sum().sum()):,}")
m4.metric("Duplicate rows", f"{int(df.duplicated().sum()):,}")

st.subheader("Column-level details")
profile = pd.DataFrame(
    {
        "Column": df.columns,
        "Data type": [str(df[col].dtype) for col in df.columns],
        "Valid values": [int(df[col].notna().sum()) for col in df.columns],
        "Missing values": [int(df[col].isna().sum()) for col in df.columns],
        "Missing %": [round(float(df[col].isna().mean() * 100), 2) for col in df.columns],
        "Unique values": [int(df[col].nunique(dropna=True)) for col in df.columns],
    }
)
st.dataframe(profile, use_container_width=True, hide_index=True)

st.subheader("Preview")
st.dataframe(df.head(50), use_container_width=True)

st.subheader("Numerical columns")
num = df.select_dtypes(include=[np.number])
if num.empty:
    st.warning("No numerical columns were found.")
else:
    st.dataframe(num.describe().T.reset_index().rename(columns={"index": "Column"}), use_container_width=True, hide_index=True)

st.subheader("Categorical columns")
cat = df.select_dtypes(include=["object", "category", "bool"])
if cat.empty:
    st.warning("No categorical columns were found.")
else:
    top_rows = []
    for col in cat.columns:
        vc = cat[col].dropna().value_counts()
        if vc.empty:
            top_rows.append({"Column": col, "Most common value": None, "Count": 0})
        else:
            top_rows.append({"Column": col, "Most common value": vc.index[0], "Count": int(vc.iloc[0])})
    st.dataframe(pd.DataFrame(top_rows), use_container_width=True, hide_index=True)

footer()
