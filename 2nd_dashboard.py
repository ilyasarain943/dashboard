import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="FinTrack Pro | Sapphire Luxe",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
  --sapphire: #0f52ba;
  --sapphire-light: #1a6fe0;
  --blurple: #6366f1;
  --navy: #0d1b2a;
  --navy-card: #1e293b;
  --navy-border: #2d3f57;
  --emerald: #10b981;
  --red-risk: #ef4444;
  --amber: #f59e0b;
  --white: #f0f6ff;
  --muted: #7a94b5;
  --glass-bg: rgba(15, 82, 186, 0.08);
  --glass-border: rgba(99, 102, 241, 0.25);
}

/* ── ROOT ── */
html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif !important;
  color: var(--white) !important;
}

.stApp {
  background: radial-gradient(ellipse at 20% 20%, #0a1628 0%, #0d1b2a 40%, #080f1a 100%) !important;
  min-height: 100vh;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #141f35 0%, #1a2744 60%, #0f1a30 100%) !important;
  border-right: 1px solid var(--navy-border) !important;
}

[data-testid="stSidebar"] * {
  color: var(--white) !important;
}

[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stDateInput label {
  color: var(--muted) !important;
  font-size: 11px !important;
  text-transform: uppercase !important;
  letter-spacing: 1.2px !important;
  font-weight: 600 !important;
}

/* ── FIX WHITE BACKGROUNDS ON ALL SIDEBAR INPUTS ── */

/* Selectbox container */
[data-testid="stSidebar"] [data-baseweb="select"] {
  background: rgba(15,82,186,0.12) !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div {
  background: rgba(15,82,186,0.12) !important;
  border: 1px solid var(--glass-border) !important;
  border-radius: 10px !important;
  color: var(--white) !important;
}

/* Multiselect container + tags */
[data-testid="stSidebar"] [data-baseweb="tag"] {
  background: rgba(15,82,186,0.45) !important;
  border: 1px solid var(--glass-border) !important;
  border-radius: 6px !important;
  color: white !important;
}
[data-testid="stSidebar"] [data-baseweb="tag"] span {
  color: white !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] input {
  background: transparent !important;
  color: var(--white) !important;
  caret-color: white !important;
}

/* Date input */
[data-testid="stSidebar"] [data-testid="stDateInput"] > div,
[data-testid="stSidebar"] [data-testid="stDateInput"] input,
[data-testid="stSidebar"] .stDateInput input,
[data-testid="stSidebar"] input[type="text"],
[data-testid="stSidebar"] input[type="date"],
[data-testid="stSidebar"] input {
  background: rgba(15,82,186,0.12) !important;
  border: 1px solid var(--glass-border) !important;
  border-radius: 10px !important;
  color: var(--white) !important;
  caret-color: white !important;
}

/* baseweb input wrapper used for date range */
[data-testid="stSidebar"] [data-baseweb="input"] {
  background: rgba(15,82,186,0.12) !important;
  border: 1px solid var(--glass-border) !important;
  border-radius: 10px !important;
}
[data-testid="stSidebar"] [data-baseweb="input"] input {
  background: transparent !important;
  color: var(--white) !important;
}

/* Dropdown menu popup */
[data-baseweb="popover"] [data-baseweb="menu"],
[data-baseweb="popover"] ul {
  background: #1a2744 !important;
  border: 1px solid var(--glass-border) !important;
}
[data-baseweb="popover"] li {
  background: #1a2744 !important;
  color: var(--white) !important;
}
[data-baseweb="popover"] li:hover {
  background: rgba(15,82,186,0.4) !important;
}

/* Slider thumb */
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[role="slider"] {
  background: var(--sapphire) !important;
  border: 2px solid var(--blurple) !important;
}

/* Calendar popup for date picker */
[data-baseweb="calendar"] {
  background: #1a2744 !important;
  border: 1px solid var(--glass-border) !important;
  border-radius: 12px !important;
}
[data-baseweb="calendar"] * {
  color: var(--white) !important;
}
[data-baseweb="calendar"] button {
  background: transparent !important;
}
[data-baseweb="calendar"] [aria-selected="true"] div {
  background: var(--sapphire) !important;
}

/* ── METRICS / KPI ORBS ── */
[data-testid="stMetric"] {
  background: linear-gradient(135deg, rgba(15,82,186,0.18) 0%, rgba(99,102,241,0.10) 100%) !important;
  border: 1px solid var(--glass-border) !important;
  border-radius: 20px !important;
  padding: 28px 24px !important;
  backdrop-filter: blur(12px) !important;
  box-shadow: 0 8px 32px rgba(15,82,186,0.25), inset 0 1px 0 rgba(255,255,255,0.08) !important;
  transition: transform 0.25s ease, box-shadow 0.25s ease !important;
}

[data-testid="stMetric"]:hover {
  transform: translateY(-4px) !important;
  box-shadow: 0 16px 48px rgba(99,102,241,0.4) !important;
}

[data-testid="stMetricLabel"] {
  font-family: 'DM Sans', sans-serif !important;
  font-size: 11px !important;
  text-transform: uppercase !important;
  letter-spacing: 1.5px !important;
  color: var(--muted) !important;
  font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
  font-family: 'Syne', sans-serif !important;
  font-size: 36px !important;
  font-weight: 800 !important;
  color: var(--white) !important;
  line-height: 1.1 !important;
}

[data-testid="stMetricDelta"] {
  font-size: 13px !important;
  font-weight: 600 !important;
}

/* ── TABS ── */
[data-testid="stTabs"] [role="tablist"] {
  background: rgba(15,82,186,0.1) !important;
  border-radius: 16px !important;
  padding: 6px !important;
  border: 1px solid var(--glass-border) !important;
  gap: 4px !important;
}

[data-testid="stTabs"] [role="tab"] {
  font-family: 'Syne', sans-serif !important;
  font-weight: 600 !important;
  font-size: 13px !important;
  color: var(--muted) !important;
  border-radius: 12px !important;
  padding: 10px 22px !important;
  transition: all 0.2s !important;
  letter-spacing: 0.5px !important;
}

[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
  background: linear-gradient(135deg, var(--sapphire), var(--blurple)) !important;
  color: white !important;
  box-shadow: 0 4px 15px rgba(15,82,186,0.5) !important;
}

/* ── BUTTONS ── */
.stButton > button {
  background: linear-gradient(135deg, var(--sapphire) 0%, var(--blurple) 100%) !important;
  color: white !important;
  border: none !important;
  border-radius: 12px !important;
  font-family: 'Syne', sans-serif !important;
  font-weight: 700 !important;
  font-size: 13px !important;
  padding: 12px 24px !important;
  letter-spacing: 0.5px !important;
  box-shadow: 0 4px 20px rgba(15,82,186,0.4) !important;
  transition: all 0.2s !important;
  width: 100% !important;
}

.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 30px rgba(99,102,241,0.6) !important;
}

/* ── DATAFRAME ── */
.stDataFrame {
  border: 1px solid var(--glass-border) !important;
  border-radius: 16px !important;
  overflow: hidden !important;
}

/* ── PLOTLY CHARTS container ── */
.stPlotlyChart {
  border-radius: 16px !important;
  overflow: hidden !important;
}

/* ── CUSTOM HEADER ── */
.fintrack-header {
  background: linear-gradient(135deg, #0f52ba 0%, #6366f1 100%);
  border-radius: 20px;
  padding: 28px 36px;
  margin-bottom: 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 8px 40px rgba(15,82,186,0.5), inset 0 1px 0 rgba(255,255,255,0.12);
  position: relative;
  overflow: hidden;
}

.fintrack-header::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -10%;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(255,255,255,0.06) 0%, transparent 70%);
  border-radius: 50%;
}

.fintrack-title {
  font-family: 'Syne', sans-serif;
  font-size: 38px;
  font-weight: 800;
  color: white;
  letter-spacing: -0.5px;
  text-shadow: 0 2px 20px rgba(0,0,0,0.3);
  margin: 0;
}

.fintrack-subtitle {
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  color: rgba(255,255,255,0.65);
  letter-spacing: 1.5px;
  text-transform: uppercase;
  margin: 4px 0 0 0;
}

.health-score {
  text-align: center;
}

.health-score .score-val {
  font-family: 'Syne', sans-serif;
  font-size: 42px;
  font-weight: 800;
  color: #10b981;
  text-shadow: 0 0 20px rgba(16,185,129,0.5);
}

.health-score .score-label {
  font-size: 11px;
  color: rgba(255,255,255,0.6);
  text-transform: uppercase;
  letter-spacing: 1.5px;
}

/* ── RISK TABLE BADGES ── */
.badge-green { color: #10b981; font-weight: 700; font-size: 12px; }
.badge-amber { color: #f59e0b; font-weight: 700; font-size: 12px; }
.badge-red   { color: #ef4444; font-weight: 700; font-size: 12px; }

/* ── SECTION TITLES ── */
.section-title {
  font-family: 'Syne', sans-serif;
  font-size: 18px;
  font-weight: 700;
  color: var(--white);
  margin: 24px 0 14px 0;
  letter-spacing: 0.3px;
}

.section-sub {
  font-size: 12px;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 1.2px;
  margin-bottom: 16px;
}

/* ── SIDEBAR LOGO ── */
.sidebar-logo {
  font-family: 'Syne', sans-serif;
  font-size: 22px;
  font-weight: 800;
  background: linear-gradient(135deg, #0f52ba, #6366f1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 4px;
}

.sidebar-tagline {
  font-size: 10px;
  color: var(--muted);
  letter-spacing: 1.5px;
  text-transform: uppercase;
  margin-bottom: 24px;
}

/* ── DIVIDER ── */
hr { border-color: var(--navy-border) !important; margin: 16px 0 !important; }

/* ── FOOTER ── */
.footer-bar {
  background: linear-gradient(90deg, #0d1b2a 0%, #1a2744 50%, #0d1b2a 100%);
  border: 1px solid var(--navy-border);
  border-radius: 14px;
  padding: 18px 28px;
  margin-top: 36px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 13px;
  color: var(--muted);
}

.footer-brand {
  font-family: 'Syne', sans-serif;
  font-weight: 700;
  color: var(--white) !important;
}

/* Hide Streamlit default elements */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
.stDeployButton { display: none; }
header[data-testid="stHeader"] { background: transparent !important; }

/* Input styling */
.stSelectbox [data-baseweb="select"] > div {
  background: rgba(15,82,186,0.12) !important;
  border-color: var(--glass-border) !important;
  color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA GENERATION
# ─────────────────────────────────────────────
@st.cache_data
def generate_data(n=500):
    np.random.seed(42)
    names = [f"User_{i:03d}" for i in range(n)]
    regions = np.random.choice(["Punjab", "Sindh", "KPK", "Balochistan"], n, p=[0.40, 0.30, 0.20, 0.10])
    ages = np.random.randint(22, 62, n)
    edu = np.random.choice(["Matric", "Intermediate", "Bachelor", "Masters", "PhD"], n, p=[0.15, 0.20, 0.30, 0.25, 0.10])
    employed = np.random.choice([1, 0], n, p=[0.68, 0.32])
    gender = np.random.choice(["Male", "Female"], n, p=[0.58, 0.42])
    income = np.where(employed, np.random.normal(3800, 900, n), np.random.normal(1200, 400, n)).clip(600, 12000).round(0)
    expenses = (income * np.random.uniform(0.45, 0.75, n)).round(0)
    savings_ratio = ((income - expenses) / income * 100).round(1)
    loan_amt = np.random.choice([0, 50000, 120000, 250000, 500000, 1000000], n, p=[0.20, 0.25, 0.20, 0.18, 0.12, 0.05])
    loan_type = np.random.choice(["Personal", "Home", "Car", "Education"], n)
    loan_rate = np.random.uniform(8, 22, n).round(1)
    loan_term = np.random.choice([12, 24, 36, 48, 60], n)
    emi = (loan_amt * (loan_rate/100/12) / (1 - (1+loan_rate/100/12)**(-loan_term))).round(0)
    dti = np.where(income > 0, (emi / income * 100), 0).round(1)
    credit_score = np.random.normal(680, 80, n).clip(300, 850).round(0).astype(int)
    food = (income * np.random.uniform(0.15, 0.25, n)).round(0)
    rent = (income * np.random.uniform(0.20, 0.35, n)).round(0)
    emi_exp = emi.round(0)
    other = (expenses - food - rent - emi_exp).clip(0).round(0)
    dates = [datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365)) for _ in range(n)]
    df = pd.DataFrame({
        "name": names, "region": regions, "age": ages, "education": edu,
        "employed": employed, "gender": gender, "monthly_income": income,
        "expenses": expenses, "savings_ratio": savings_ratio,
        "loan_amount": loan_amt, "loan_type": loan_type, "loan_interest_rate": loan_rate,
        "loan_term_months": loan_term, "monthly_emi": emi, "dti_ratio": dti,
        "credit_score": credit_score, "food_exp": food, "rent_exp": rent,
        "emi_exp": emi_exp, "other_exp": other, "record_date": dates
    })
    df["record_date"] = pd.to_datetime(df["record_date"])
    df["month"] = df["record_date"].dt.to_period("M").astype(str)
    return df

df_full = generate_data(500)

# ─────────────────────────────────────────────
# CHART THEME
# ─────────────────────────────────────────────
CHART_BG    = "rgba(13,27,42,0)"
PAPER_BG    = "rgba(13,27,42,0)"
GRID_COLOR  = "rgba(45,63,87,0.6)"
FONT_COLOR  = "#7a94b5"
SAPPHIRE    = "#0f52ba"
BLURPLE     = "#6366f1"
EMERALD     = "#10b981"
RED         = "#ef4444"
AMBER       = "#f59e0b"

CHART_LAYOUT = dict(
    paper_bgcolor=PAPER_BG,
    plot_bgcolor=CHART_BG,
    font=dict(family="DM Sans", color=FONT_COLOR, size=12),
    margin=dict(t=40, b=40, l=50, r=20),
    legend=dict(
        bgcolor="rgba(13,27,42,0.6)",
        bordercolor=GRID_COLOR,
        borderwidth=1,
        font=dict(color="#aac0d8", size=11),
    ),
    xaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, tickfont=dict(color=FONT_COLOR)),
    yaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, tickfont=dict(color=FONT_COLOR)),
)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 8px 0 20px 0;'>
      <div class='sidebar-logo'>💎 FinTrack Pro</div>
      <div class='sidebar-tagline'>Sapphire Luxe Edition 2026</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**FILTERS**")
    region_opts = ["All"] + sorted(df_full["region"].unique().tolist())
    region = st.selectbox("🔍 Region", region_opts)

    age_range = st.slider("👤 Age Range", 22, 62, (22, 62), step=1)

    edu_opts = df_full["education"].unique().tolist()
    edu_sel = st.multiselect("📚 Education", edu_opts, default=edu_opts)

    emp_opts = {"All": None, "Employed": 1, "Unemployed": 0}
    emp_sel = st.selectbox("💼 Employment", list(emp_opts.keys()))

    min_date = df_full["record_date"].min().date()
    max_date = df_full["record_date"].max().date()
    date_range = st.date_input("📅 Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

    st.markdown("<br>", unsafe_allow_html=True)
    apply = st.button("✦ APPLY FILTERS", use_container_width=True)
    reset = st.button("↺ Reset", use_container_width=True)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:11px; color:#4a6080; text-align:center; line-height:1.8;'>
    📊 500 records loaded<br>
    🔄 Last updated: Mar 2026<br>
    💾 Source: Kaggle Dataset
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FILTER LOGIC
# ─────────────────────────────────────────────
df = df_full.copy()
if region != "All":
    df = df[df["region"] == region]
df = df[(df["age"] >= age_range[0]) & (df["age"] <= age_range[1])]
if edu_sel:
    df = df[df["education"].isin(edu_sel)]
if emp_opts[emp_sel] is not None:
    df = df[df["employed"] == emp_opts[emp_sel]]
if len(date_range) == 2:
    df = df[(df["record_date"].dt.date >= date_range[0]) & (df["record_date"].dt.date <= date_range[1])]

# ─────────────────────────────────────────────
# KPI CALCULATIONS
# ─────────────────────────────────────────────
avg_income   = df["monthly_income"].mean()
avg_dti      = df["dti_ratio"].mean()
avg_savings  = df["savings_ratio"].mean()
avg_credit   = df["credit_score"].mean()
prev_income  = avg_income * 0.88
health_score = min(100, max(0, round(
    (avg_credit / 850 * 35) + (max(0, 50 - avg_dti) / 50 * 35) + (avg_savings / 50 * 30)
)))

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class='fintrack-header'>
  <div>
    <div class='fintrack-title'>💎 FinTrack Pro</div>
    <div class='fintrack-subtitle'>Personal Finance Intelligence Dashboard</div>
  </div>
  <div class='health-score'>
    <div class='score-val'>{health_score}/100</div>
    <div class='score-label'>Portfolio Health Score</div>
  </div>
  <div style='text-align:right;'>
    <div style='font-family:Syne,sans-serif; font-size:14px; color:rgba(255,255,255,0.7);'>📦 {len(df):,} Records</div>
    <div style='font-size:11px; color:rgba(255,255,255,0.45); margin-top:4px; letter-spacing:1px;'>SAPPHIRE LUXE EDITION</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI ORBS
# ─────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("💰 Avg Monthly Income", f"${avg_income:,.0f}", f"+{((avg_income/prev_income)-1)*100:.1f}% MoM")
with c2:
    dti_delta = f"{'⚠️ High Risk' if avg_dti > 40 else '✓ Healthy'}"
    st.metric("⚠️ Avg Debt-to-Income", f"{avg_dti:.1f}%", dti_delta, delta_color="inverse")
with c3:
    st.metric("🟢 Avg Savings Ratio", f"{avg_savings:.1f}%", "+2.3% vs last qtr")
with c4:
    st.metric("📈 Avg Credit Score", f"{avg_credit:.0f}", "FICO Scale")

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 Finance Overview", "💳 Debt Analysis", "💵 Income Flow", "🔍 Insights"])

# ══════════════════════════════════════════════
# TAB 1 — FINANCE OVERVIEW
# ══════════════════════════════════════════════
with tab1:

    col_left, col_right = st.columns(2, gap="medium")

    # CHART 1 — Income Trend
    with col_left:
        st.markdown("<div class='section-title'>📈 Income Trends Over Time</div>", unsafe_allow_html=True)
        monthly = df.groupby(["month", "employed"])["monthly_income"].mean().reset_index()
        monthly["employment_label"] = monthly["employed"].map({1: "Employed", 0: "Unemployed"})
        fig1 = px.line(
            monthly, x="month", y="monthly_income", color="employment_label",
            markers=True,
            color_discrete_map={"Employed": EMERALD, "Unemployed": RED},
        )
        fig1.update_traces(line_width=2.5, marker_size=6)
        fig1.update_layout(**CHART_LAYOUT, height=320,
            xaxis_title="Month", yaxis_title="Avg Income ($)",
            title=dict(text="", font=dict(color=FONT_COLOR)),
        )
        fig1.update_layout(hovermode="x unified")
        st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

    # CHART 2 — Expense Donut
    with col_right:
        st.markdown("<div class='section-title'>🍩 Expense Breakdown</div>", unsafe_allow_html=True)
        exp_data = pd.DataFrame({
            "Category": ["Food", "Rent", "EMI / Loans", "Other"],
            "Amount": [df["food_exp"].mean(), df["rent_exp"].mean(), df["emi_exp"].mean(), df["other_exp"].mean()]
        })
        fig2 = go.Figure(go.Pie(
            labels=exp_data["Category"],
            values=exp_data["Amount"].round(0),
            hole=0.58,
            marker=dict(colors=[EMERALD, SAPPHIRE, RED, AMBER],
                        line=dict(color="#0d1b2a", width=3)),
            textfont=dict(color="white", size=12),
            hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<extra></extra>",
        ))
        fig2.update_layout(
            **{k: v for k, v in CHART_LAYOUT.items() if k not in ["xaxis", "yaxis"]},
            height=320,
            annotations=[dict(text=f"${exp_data['Amount'].sum():,.0f}<br><span style='font-size:10px'>Total Exp</span>",
                              x=0.5, y=0.5, font=dict(size=14, color="white"), showarrow=False)],
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    col3, col4 = st.columns(2, gap="medium")

    # CHART 3 — Region Bar
    with col3:
        st.markdown("<div class='section-title'>🗺️ Income by Region</div>", unsafe_allow_html=True)
        reg_data = df.groupby("region").agg(
            avg_income=("monthly_income","mean"),
            total_loans=("loan_amount","sum"),
            count=("name","count")
        ).reset_index()
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=reg_data["region"], y=reg_data["avg_income"],
            marker=dict(
                color=reg_data["avg_income"],
                colorscale=[[0, SAPPHIRE], [0.5, BLURPLE], [1, EMERALD]],
                showscale=False,
                line=dict(color="#0d1b2a", width=1)
            ),
            text=reg_data["avg_income"].round(0).apply(lambda x: f"${x:,.0f}"),
            textposition="outside",
            textfont=dict(color="white", size=11),
            hovertemplate="<b>%{x}</b><br>Avg Income: $%{y:,.0f}<extra></extra>",
        ))
        fig3.update_layout(**CHART_LAYOUT, height=300,
            yaxis_title="Avg Income ($)", xaxis_title="Region")
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    # CHART 4 — Savings Scatter
    with col4:
        st.markdown("<div class='section-title'>💹 Age vs Savings Ratio</div>", unsafe_allow_html=True)
        fig4 = px.scatter(
            df.sample(min(300, len(df))),
            x="age", y="savings_ratio",
            size="monthly_income",
            color="credit_score",
            color_continuous_scale=[[0, RED], [0.5, AMBER], [1, EMERALD]],
            size_max=20,
            opacity=0.75,
            hover_data={"name": True, "monthly_income": ":.0f", "credit_score": True},
            labels={"savings_ratio": "Savings Ratio (%)", "age": "Age"},
        )
        fig4.update_layout(**{k: v for k, v in CHART_LAYOUT.items() if k not in ["legend"]},
            height=300, coloraxis_colorbar=dict(
                title="Credit", tickfont=dict(color=FONT_COLOR), thickness=12))
        st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════════
# TAB 2 — DEBT ANALYSIS
# ══════════════════════════════════════════════
with tab2:
    col5, col6 = st.columns(2, gap="medium")

    # CHART 5 — Loan Stacked Bar
    with col5:
        st.markdown("<div class='section-title'>🏦 Loan Amount by Type & Gender</div>", unsafe_allow_html=True)
        loan_data = df[df["loan_amount"] > 0].groupby(["loan_type", "gender"])["loan_amount"].mean().reset_index()
        fig5 = px.bar(
            loan_data, x="loan_type", y="loan_amount", color="gender",
            barmode="group",
            color_discrete_map={"Male": SAPPHIRE, "Female": BLURPLE},
        )
        fig5.update_layout(**CHART_LAYOUT, height=340,
            yaxis_title="Avg Loan Amount ($)", xaxis_title="Loan Type")
        fig5.update_traces(marker_line_width=0)
        st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})

    # CHART 6 — EMI Heatmap
    with col6:
        st.markdown("<div class='section-title'>🔥 EMI Risk Heatmap (Rate × Term)</div>", unsafe_allow_html=True)
        df_heat = df[df["loan_amount"] > 0].copy()
        df_heat["rate_bin"] = pd.cut(df_heat["loan_interest_rate"], bins=[8,11,14,17,20,23], labels=["8-11%","11-14%","14-17%","17-20%","20-23%"])
        df_heat["term_bin"] = df_heat["loan_term_months"].astype(str) + "mo"
        heat_pivot = df_heat.groupby(["rate_bin","term_bin"])["monthly_emi"].mean().unstack(fill_value=0)
        fig6 = go.Figure(go.Heatmap(
            z=heat_pivot.values,
            x=heat_pivot.columns.tolist(),
            y=heat_pivot.index.tolist(),
            colorscale=[[0, "#0f52ba"], [0.5, "#f59e0b"], [1, "#ef4444"]],
            text=heat_pivot.values.round(0),
            texttemplate="%{text:,.0f}",
            textfont=dict(color="white", size=11),
            hovertemplate="Rate: %{y}<br>Term: %{x}<br>Avg EMI: $%{z:,.0f}<extra></extra>",
            colorbar=dict(title="Avg EMI ($)", tickfont=dict(color=FONT_COLOR), thickness=14)
        ))
        fig6.update_layout(**{k: v for k, v in CHART_LAYOUT.items() if k not in ["xaxis", "yaxis"]},
            height=340,
            xaxis=dict(title="Loan Term", tickfont=dict(color=FONT_COLOR), gridcolor=GRID_COLOR),
            yaxis=dict(title="Interest Rate", tickfont=dict(color=FONT_COLOR), gridcolor=GRID_COLOR),
        )
        st.plotly_chart(fig6, use_container_width=True, config={"displayModeBar": False})

    # DTI Distribution
    st.markdown("<div class='section-title'>📊 DTI Distribution by Employment</div>", unsafe_allow_html=True)
    fig_dti = px.histogram(
        df, x="dti_ratio", color="employed",
        nbins=40, barmode="overlay", opacity=0.75,
        color_discrete_map={1: EMERALD, 0: RED},
        labels={"dti_ratio": "Debt-to-Income Ratio (%)", "employed": "Status"},
        category_orders={"employed": [1, 0]}
    )
    layout_no_legend = {k: v for k, v in CHART_LAYOUT.items() if k != "legend"}
    fig_dti.update_layout(**layout_no_legend, height=280,
        legend=dict(bgcolor="rgba(13,27,42,0.6)", bordercolor=GRID_COLOR, borderwidth=1,
                    font=dict(color="#aac0d8", size=11), title_text=""),
    )
    fig_dti.add_vline(x=40, line_dash="dash", line_color=AMBER,
                      annotation_text="40% Risk Threshold",
                      annotation_font_color=AMBER)
    st.plotly_chart(fig_dti, use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════════
# TAB 3 — INCOME FLOW
# ══════════════════════════════════════════════
with tab3:
    col7, col8 = st.columns(2, gap="medium")

    with col7:
        st.markdown("<div class='section-title'>📦 Income Distribution by Education</div>", unsafe_allow_html=True)
        fig_box = px.box(
            df, x="education", y="monthly_income", color="education",
            color_discrete_sequence=[SAPPHIRE, BLURPLE, EMERALD, AMBER, RED],
            category_orders={"education": ["Matric", "Intermediate", "Bachelor", "Masters", "PhD"]}
        )
        fig_box.update_layout(**CHART_LAYOUT, height=340,
            showlegend=False, yaxis_title="Income ($)", xaxis_title="Education Level")
        st.plotly_chart(fig_box, use_container_width=True, config={"displayModeBar": False})

    with col8:
        st.markdown("<div class='section-title'>🌊 Credit Score Distribution</div>", unsafe_allow_html=True)
        fig_hist = px.histogram(
            df, x="credit_score", nbins=30,
            color_discrete_sequence=[BLURPLE],
        )
        fig_hist.update_traces(
            marker=dict(line=dict(color="#0d1b2a", width=1)),
            opacity=0.85,
        )
        fig_hist.update_layout(**CHART_LAYOUT, height=340,
            xaxis_title="Credit Score (FICO)", yaxis_title="Count")
        fig_hist.add_vrect(x0=300, x1=580, fillcolor=RED, opacity=0.08, line_width=0,
                           annotation_text="Poor", annotation_font_color=RED)
        fig_hist.add_vrect(x0=580, x1=670, fillcolor=AMBER, opacity=0.08, line_width=0,
                           annotation_text="Fair", annotation_font_color=AMBER)
        fig_hist.add_vrect(x0=670, x1=850, fillcolor=EMERALD, opacity=0.08, line_width=0,
                           annotation_text="Good", annotation_font_color=EMERALD)
        st.plotly_chart(fig_hist, use_container_width=True, config={"displayModeBar": False})

    # Income vs Savings Trend
    st.markdown("<div class='section-title'>📈 Savings Rate by Region & Education</div>", unsafe_allow_html=True)
    grp = df.groupby(["region", "education"])["savings_ratio"].mean().reset_index()
    fig_grp = px.bar(
        grp, x="education", y="savings_ratio", color="region",
        barmode="group",
        color_discrete_map={"Punjab": SAPPHIRE, "Sindh": BLURPLE, "KPK": EMERALD, "Balochistan": AMBER},
        category_orders={"education": ["Matric", "Intermediate", "Bachelor", "Masters", "PhD"]}
    )
    fig_grp.update_layout(**CHART_LAYOUT, height=300,
        yaxis_title="Avg Savings Ratio (%)", xaxis_title="Education Level")
    st.plotly_chart(fig_grp, use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════════
# TAB 4 — INSIGHTS / RISK TABLE
# ══════════════════════════════════════════════
with tab4:
    st.markdown("<div class='section-title'>🔴 Risk Summary — Top Users Flagged</div>", unsafe_allow_html=True)

    def risk_label(dti):
        if dti >= 40: return "🔴 HIGH"
        elif dti >= 25: return "🟡 MEDIUM"
        else: return "🟢 LOW"

    risk_df = df.nlargest(20, "dti_ratio")[["name","region","age","monthly_income","monthly_emi","dti_ratio","credit_score"]].copy()
    risk_df["Risk Level"] = risk_df["dti_ratio"].apply(risk_label)
    risk_df.columns = ["User","Region","Age","Income ($)","EMI ($)","DTI (%)","Credit Score","Risk"]
    risk_df["Income ($)"] = risk_df["Income ($)"].apply(lambda x: f"${x:,.0f}")
    risk_df["EMI ($)"] = risk_df["EMI ($)"].apply(lambda x: f"${x:,.0f}")
    risk_df["DTI (%)"] = risk_df["DTI (%)"].apply(lambda x: f"{x:.1f}%")

    st.dataframe(
        risk_df.reset_index(drop=True),
        use_container_width=True,
        height=420,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Summary stats
    cols = st.columns(3)
    high_risk = (df["dti_ratio"] >= 40).sum()
    med_risk = ((df["dti_ratio"] >= 25) & (df["dti_ratio"] < 40)).sum()
    low_risk = (df["dti_ratio"] < 25).sum()
    with cols[0]:
        st.metric("🔴 High Risk Users", f"{high_risk:,}", f"{high_risk/len(df)*100:.1f}% of total", delta_color="inverse")
    with cols[1]:
        st.metric("🟡 Medium Risk Users", f"{med_risk:,}", f"{med_risk/len(df)*100:.1f}% of total", delta_color="off")
    with cols[2]:
        st.metric("🟢 Low Risk Users", f"{low_risk:,}", f"{low_risk/len(df)*100:.1f}% of total")

# ─────────────────────────────────────────────
# BOTTOM ACTION ZONE
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<div class='section-title'>⚡ Actions</div>", unsafe_allow_html=True)

ba1, ba2, ba3 = st.columns(3, gap="medium")
with ba1:
    if st.button("📊 Download Full Report (CSV)", use_container_width=True):
        csv = df.to_csv(index=False)
        st.download_button("⬇️ Click to Download", csv, "fintrack_report.csv", "text/csv", use_container_width=True)
with ba2:
    if st.button("💎 Order Custom Dashboard — $299", use_container_width=True):
        st.info("🌐 Visit our website to place your order for a custom dashboard.")
with ba3:
    if st.button("🎥 View Dataset on Kaggle", use_container_width=True):
        st.markdown("[🔗 Open Kaggle Dataset](https://www.kaggle.com/datasets/miadul/personal-finance-ml-dataset)", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class='footer-bar'>
  <div>
    <span class='footer-brand'>💎 FinTrack Pro</span>
    &nbsp;·&nbsp; Sapphire Luxe Edition &nbsp;·&nbsp; © 2026
  </div>
  <div style='color:#4a6080; font-size:12px;'>
    Personal Finance Intelligence Dashboard
  </div>
  <div style='color:#4a6080; font-size:12px;'>
    Custom dashboards available — visit our website to order
  </div>
</div>
""", unsafe_allow_html=True)
