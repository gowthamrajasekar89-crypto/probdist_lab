import streamlit as st

APP_NAME = "probDist Lab"
CREATOR = "Gowtham Kumar"

def configure_page(page_title: str = APP_NAME) -> None:
    st.set_page_config(
        page_title=page_title,
        page_icon="◇",
        layout="wide",
        initial_sidebar_state="expanded",
    )

def apply_style() -> None:
    st.markdown(
        """
        <style>
        :root {
            --dw-bg: #FAFAF7;
            --dw-panel: #FFFFFF;
            --dw-muted: #64748B;
            --dw-line: rgba(15, 23, 42, 0.10);
            --dw-ink: #0F172A;
        }

        .block-container {
            padding-top: 1.25rem;
            padding-bottom: 3rem;
            max-width: 1280px;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%);
            border-right: 1px solid var(--dw-line);
        }

        h1, h2, h3 {
            letter-spacing: -0.02em;
        }

        h1 {
            font-size: 2.15rem !important;
            margin-bottom: 0.35rem !important;
        }

        div[data-testid="stMetric"] {
            background: var(--dw-panel);
            border: 1px solid var(--dw-line);
            border-radius: 16px;
            padding: 16px 18px;
            box-shadow: 0 2px 10px rgba(15, 23, 42, 0.035);
        }

        div[data-testid="stMetricLabel"] {
            color: var(--dw-muted);
            font-weight: 700;
            font-size: 0.78rem !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        div[data-testid="stMetricValue"] {
            color: var(--dw-ink);
            font-size: 1.55rem !important;
            font-weight: 750 !important;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid var(--dw-line);
            border-radius: 14px;
            overflow: hidden;
        }

        .stButton > button {
            border-radius: 999px;
            border: 1px solid #CBD5E1;
            font-weight: 700;
            padding-left: 1.1rem;
            padding-right: 1.1rem;
        }

        .dw-hero {
            border: 1px solid var(--dw-line);
            border-radius: 24px;
            padding: 28px 30px;
            background:
                radial-gradient(circle at top right, rgba(148, 163, 184, 0.20), transparent 35%),
                linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
            margin-bottom: 20px;
        }

        .dw-kicker {
            color: #475569;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 0.78rem;
            margin-bottom: 0.25rem;
        }

        .dw-subtitle {
            color: #64748B;
            font-size: 1.02rem;
            margin-top: 0;
            max-width: 760px;
        }

        .dw-card {
            border: 1px solid var(--dw-line);
            border-radius: 18px;
            padding: 18px;
            background: #FFFFFF;
            box-shadow: 0 2px 10px rgba(15, 23, 42, 0.035);
            margin-bottom: 14px;
        }

        .dw-footer {
            color: #64748B;
            font-size: 0.84rem;
            text-align: center;
            padding: 28px 0 6px 0;
        }

        .small-note {
            color: #64748B;
            font-size: 0.92rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def hero(title: str, subtitle: str, kicker: str = "Analysis workspace") -> None:
    st.markdown(
        f"""
        <div class="dw-hero">
          <div class="dw-kicker">{kicker}</div>
          <h1>{title}</h1>
          <p class="dw-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def card(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="dw-card">
          <h3 style="margin-top:0;">{title}</h3>
          <p style="color:#475569;margin-bottom:0;">{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def footer() -> None:
    st.markdown(
        f"""
        <div class="dw-footer">
            {APP_NAME} · {CREATOR} · Built with Streamlit
        </div>
        """,
        unsafe_allow_html=True,
    )
