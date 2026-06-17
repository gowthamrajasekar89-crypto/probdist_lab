import pandas as pd
import streamlit as st

from src.helpers import categorical_columns, load_uploaded_file, numeric_columns
from src.style import APP_NAME, apply_style, configure_page, footer, hero

configure_page(APP_NAME)
apply_style()

if "dataset" not in st.session_state:
    st.session_state["dataset"] = None
if "dataset_name" not in st.session_state:
    st.session_state["dataset_name"] = None

hero(
    "ProbDist Lab",
    "A clean statistical workspace for exploring datasets, checking assumptions, running hypothesis tests, and writing simple interpretations.",
    "Dataset hub",
)

left, right = st.columns([0.95, 1.35], gap="large")

with left:
    st.subheader("Load your data")
    uploaded = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx", "xls"])
    if uploaded is not None:
        try:
            data = load_uploaded_file(uploaded)
            st.session_state["dataset"] = data
            st.session_state["dataset_name"] = uploaded.name
            st.success(f"Loaded: {uploaded.name}")
        except Exception as exc:
            st.error(f"Could not read the file: {exc}")

    if st.session_state["dataset"] is not None:
        if st.button("Clear current dataset"):
            st.session_state["dataset"] = None
            st.session_state["dataset_name"] = None
            st.rerun()

    st.markdown(
        """
        <p class="small-note">
        Tip: keep one row per observation and use separate columns for each variable.
        Categorical columns are used for grouping in ANOVA, t-tests, chi-square tests, and nonparametric tests.
        </p>
        """,
        unsafe_allow_html=True,
    )

with right:
    df = st.session_state["dataset"]
    if df is None:
        st.info("Upload a dataset to unlock the analysis pages from the sidebar.")
    else:
        st.subheader("Dataset snapshot")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Rows", f"{df.shape[0]:,}")
        m2.metric("Columns", f"{df.shape[1]:,}")
        m3.metric("Numeric", len(numeric_columns(df)))
        m4.metric("Categorical", len(categorical_columns(df)))

        missing_total = int(df.isna().sum().sum())
        duplicate_rows = int(df.duplicated().sum())

        q1, q2 = st.columns(2)
        q1.metric("Missing cells", f"{missing_total:,}")
        q2.metric("Duplicate rows", f"{duplicate_rows:,}")

        with st.expander("Preview the first rows", expanded=True):
            st.dataframe(df.head(25), use_container_width=True)

        with st.expander("Column inventory"):
            inventory = pd.DataFrame(
                {
                    "Column": df.columns,
                    "Type": [str(dtype) for dtype in df.dtypes],
                    "Missing": [int(df[col].isna().sum()) for col in df.columns],
                    "Unique values": [int(df[col].nunique(dropna=True)) for col in df.columns],
                }
            )
            st.dataframe(inventory, use_container_width=True, hide_index=True)

st.divider()
st.subheader("Modules included")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("**Explore**  \nDescriptive summary, plots, normality checks, CLT simulation.")
with c2:
    st.markdown("**Model distributions**  \nFit common probability distributions and compare KS statistics.")
with c3:
    st.markdown("**Test hypotheses**  \nANOVA, t-test, z-test, chi-square, and nonparametric procedures.")

footer()
