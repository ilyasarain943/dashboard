import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# ─────────────────────────────────────────────
# PAGE CONFIG + THEME
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="PeoplePro Analytics | HR Dashboard",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS — Arctic White Corporate
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Instrument+Serif:ital@0;1&display=swap');

:root {
  --bg-primary: #f8fafc;
  --bg-surface: #f1f5f9;
  --bg-card: rgba(255,255,255,0.95);
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --text-muted: #94a3b8;
  --border: #e2e8f0;
  --border-hover: #cbd5e1;
  --mint: #10b981;
  --mint-light: #d1fae5;
  --mint-dark: #059669;
  --steel: #3b82f6;
  --steel-light: #dbeafe;
  --amber: #f59e0b;
  --amber-light: #fef3c7;
  --red: #ef4444;
  --red-light: #fee2e2;
  --emerald: #059669;
  --violet: #8b5cf6;
  --cyan: #06b6d4;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
  --shadow-md: 0 4px 16px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.04);
  --shadow-lg: 0 12px 40px rgba(0,0,0,0.10), 0 4px 8px rgba(0,0,0,0.05);
  --shadow-mint: 0 8px 24px rgba(16,185,129,0.20);
}

/* ── ROOT ── */
html, body, [class*="css"] {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  color: var(--text-primary) !important;
}

.stApp {
  background: var(--bg-primary) !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
  background: #ffffff !important;
  border-right: 1px solid var(--border) !important;
  box-shadow: 2px 0 12px rgba(0,0,0,0.04) !important;
}

[data-testid="stSidebar"] * {
  color: var(--text-primary) !important;
}

[data-testid="stSidebar"] label {
  font-size: 11px !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: 1.2px !important;
  color: var(--text-muted) !important;
}

/* All sidebar inputs — white bg with mint border */
[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-baseweb="input"],
[data-testid="stSidebar"] input {
  background: var(--bg-surface) !important;
  border: 1.5px solid var(--border) !important;
  border-radius: 10px !important;
  color: var(--text-primary) !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div:focus-within,
[data-testid="stSidebar"] [data-baseweb="input"]:focus-within {
  border-color: var(--mint) !important;
  box-shadow: 0 0 0 3px rgba(16,185,129,0.12) !important;
}

[data-testid="stSidebar"] [data-baseweb="tag"] {
  background: var(--mint-light) !important;
  border: 1px solid rgba(16,185,129,0.3) !important;
  border-radius: 6px !important;
  color: var(--mint-dark) !important;
}

[data-testid="stSidebar"] [data-baseweb="tag"] span {
  color: var(--mint-dark) !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] input {
  background: transparent !important;
  color: var(--text-primary) !important;
}

[data-testid="stSidebar"] [data-baseweb="popover"] [data-baseweb="menu"],
[data-baseweb="popover"] ul {
  background: #ffffff !important;
  border: 1px solid var(--border) !important;
  box-shadow: var(--shadow-lg) !important;
  border-radius: 12px !important;
}

[data-baseweb="popover"] li {
  background: #ffffff !important;
  color: var(--text-primary) !important;
}

[data-baseweb="popover"] li:hover {
  background: var(--mint-light) !important;
  color: var(--mint-dark) !important;
}

/* Calendar */
[data-baseweb="calendar"] {
  background: #ffffff !important;
  border: 1px solid var(--border) !important;
  border-radius: 14px !important;
  box-shadow: var(--shadow-lg) !important;
}

[data-baseweb="calendar"] * { color: var(--text-primary) !important; }
[data-baseweb="calendar"] [aria-selected="true"] div {
  background: var(--mint) !important;
  color: white !important;
}

/* ── METRICS ── */
[data-testid="stMetric"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 20px !important;
  padding: 24px 20px !important;
  box-shadow: var(--shadow-md) !important;
  transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}

[data-testid="stMetric"]:hover {
  transform: translateY(-3px) !important;
  box-shadow: var(--shadow-lg) !important;
  border-color: var(--mint) !important;
}

[data-testid="stMetricLabel"] {
  font-size: 11px !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: 1.4px !important;
  color: var(--text-muted) !important;
}

[data-testid="stMetricValue"] {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 34px !important;
  font-weight: 800 !important;
  color: var(--text-primary) !important;
  line-height: 1.1 !important;
}

/* ── TABS ── */
[data-testid="stTabs"] [role="tablist"] {
  background: var(--bg-surface) !important;
  border-radius: 14px !important;
  padding: 5px !important;
  border: 1px solid var(--border) !important;
  gap: 3px !important;
}

[data-testid="stTabs"] [role="tab"] {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-weight: 600 !important;
  font-size: 13px !important;
  color: var(--text-secondary) !important;
  border-radius: 10px !important;
  padding: 9px 20px !important;
  transition: all 0.2s !important;
}

[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
  background: var(--mint) !important;
  color: white !important;
  box-shadow: var(--shadow-mint) !important;
}

/* ── BUTTONS ── */
.stButton > button {
  background: var(--mint) !important;
  color: white !important;
  border: none !important;
  border-radius: 12px !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-weight: 700 !important;
  font-size: 13px !important;
  padding: 12px 22px !important;
  letter-spacing: 0.3px !important;
  box-shadow: var(--shadow-mint) !important;
  transition: all 0.2s !important;
  width: 100% !important;
}

.stButton > button:hover {
  background: var(--mint-dark) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 10px 30px rgba(16,185,129,0.35) !important;
}

/* ── DATAFRAME ── */
.stDataFrame {
  border: 1px solid var(--border) !important;
  border-radius: 16px !important;
  overflow: hidden !important;
  box-shadow: var(--shadow-sm) !important;
}

/* ── PLOTLY CHART ── */
.stPlotlyChart {
  border-radius: 16px !important;
  overflow: hidden !important;
}

/* ── SEARCH INPUT ── */
.stTextInput input {
  background: var(--bg-surface) !important;
  border: 1.5px solid var(--border) !important;
  border-radius: 10px !important;
  color: var(--text-primary) !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.stTextInput input:focus {
  border-color: var(--mint) !important;
  box-shadow: 0 0 0 3px rgba(16,185,129,0.12) !important;
}

/* ── SLIDER ── */
[data-testid="stSidebar"] [data-baseweb="slider"] div[role="slider"] {
  background: var(--mint) !important;
  border: 2px solid var(--mint-dark) !important;
}

/* ── CUSTOM COMPONENTS ── */
.pp-header {
  background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
  border: 1px solid var(--border);
  border-bottom: 3px solid var(--mint);
  border-radius: 20px;
  padding: 26px 32px;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: var(--shadow-md);
  position: relative;
  overflow: hidden;
}

.pp-header::after {
  content: '';
  position: absolute;
  top: 0; right: 0;
  width: 200px; height: 100%;
  background: linear-gradient(135deg, transparent 0%, rgba(16,185,129,0.05) 100%);
  border-radius: 0 20px 20px 0;
}

.pp-title {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 32px;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.5px;
  margin: 0;
}

.pp-subtitle {
  font-size: 13px;
  color: var(--text-muted);
  letter-spacing: 1.2px;
  text-transform: uppercase;
  font-weight: 600;
  margin: 4px 0 0 0;
}

.pp-badge {
  background: var(--mint-light);
  color: var(--mint-dark);
  font-size: 11px;
  font-weight: 700;
  padding: 4px 12px;
  border-radius: 20px;
  letter-spacing: 0.5px;
  border: 1px solid rgba(16,185,129,0.25);
}

.section-title {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 20px 0 12px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-wrap {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 20px;
  box-shadow: var(--shadow-sm);
  margin-bottom: 16px;
}

.risk-high  { color: #ef4444; font-weight: 700; font-size: 12px; background: #fee2e2; padding: 3px 8px; border-radius: 6px; }
.risk-med   { color: #d97706; font-weight: 700; font-size: 12px; background: #fef3c7; padding: 3px 8px; border-radius: 6px; }
.risk-low   { color: #059669; font-weight: 700; font-size: 12px; background: #d1fae5; padding: 3px 8px; border-radius: 6px; }

.stat-pill {
  display: inline-block;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 6px 14px;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  margin: 3px;
}

.footer-bar {
  background: linear-gradient(90deg, #ffffff 0%, #f0fdf4 50%, #ffffff 100%);
  border: 1px solid var(--border);
  border-top: 2px solid var(--mint);
  border-radius: 14px;
  padding: 16px 28px;
  margin-top: 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 13px;
  color: var(--text-secondary);
  box-shadow: var(--shadow-sm);
}

.footer-brand {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-weight: 800;
  color: var(--text-primary);
}

/* Hide Streamlit chrome */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
.stDeployButton { display: none; }
header[data-testid="stHeader"] { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA GENERATION
# ─────────────────────────────────────────────
@st.cache_data
def generate_hr_data(n=800):
    np.random.seed(99)
    departments = ["Engineering", "Marketing", "Sales", "HR", "Finance", "Operations", "Design", "Legal"]
    job_titles = {
        "Engineering": ["Software Engineer", "Senior Dev", "DevOps", "QA Engineer", "Tech Lead"],
        "Marketing": ["Marketing Manager", "Content Lead", "SEO Analyst", "Brand Manager", "Growth Hacker"],
        "Sales": ["Sales Rep", "Account Executive", "Sales Manager", "BDR", "Sales Director"],
        "HR": ["HR Manager", "Recruiter", "Talent Lead", "HR Analyst", "People Ops"],
        "Finance": ["Analyst", "Controller", "Accountant", "CFO Office", "Financial Planner"],
        "Operations": ["Ops Manager", "Supply Chain", "Process Analyst", "Logistics", "COO Office"],
        "Design": ["UI Designer", "UX Lead", "Product Designer", "Brand Designer", "Creative Dir"],
        "Legal": ["Legal Counsel", "Paralegal", "Compliance", "Contract Manager", "Associate"],
    }
    edu = ["High School", "Associate", "Bachelor", "Master", "PhD"]
    emp_status = ["Full-Time", "Part-Time", "Contract", "Remote"]
    gender = ["Male", "Female", "Non-binary"]

    dept_arr = np.random.choice(departments, n, p=[0.22,0.14,0.18,0.08,0.12,0.12,0.08,0.06])
    rows = []
    base_date = datetime(2019, 1, 1)
    for i in range(n):
        dept = dept_arr[i]
        title = random.choice(job_titles[dept])
        hire_dt = base_date + timedelta(days=random.randint(0, 5*365))
        tenure = (datetime(2026, 3, 1) - hire_dt).days / 365
        sal_base = {"Engineering":7000,"Marketing":5200,"Sales":5800,"HR":4500,"Finance":6000,"Operations":4800,"Design":5500,"Legal":6500}
        salary = int(sal_base[dept] * np.random.uniform(0.75, 1.40))
        perf = round(np.random.beta(5, 2) * 5, 1)
        satisfaction = round(np.random.beta(4, 2) * 10, 1)
        turnover_risk = round(max(0, min(100, 100 - perf * 10 - satisfaction * 3 + np.random.normal(0, 8))), 1)
        rows.append({
            "employee_id": f"EMP{i+1001:04d}",
            "name": f"Employee {i+1001}",
            "department": dept,
            "job_title": title,
            "education": np.random.choice(edu, p=[0.05, 0.10, 0.45, 0.32, 0.08]),
            "employment_status": np.random.choice(emp_status, p=[0.65, 0.12, 0.15, 0.08]),
            "gender": np.random.choice(gender, p=[0.52, 0.44, 0.04]),
            "age": int(np.random.normal(35, 8)),
            "hire_date": hire_dt,
            "tenure_years": round(tenure, 1),
            "monthly_salary": salary,
            "performance_score": perf,
            "satisfaction_score": satisfaction,
            "turnover_risk": turnover_risk,
            "projects_completed": np.random.randint(1, 25),
            "training_hours": np.random.randint(0, 120),
        })
    df = pd.DataFrame(rows)
    df["age"] = df["age"].clip(22, 62)
    df["hire_month"] = df["hire_date"].dt.to_period("M").astype(str)
    df["hire_year"]  = df["hire_date"].dt.year
    return df

df_full = generate_hr_data(800)

# ─────────────────────────────────────────────
# CHART THEME (Light)
# ─────────────────────────────────────────────
BG      = "rgba(248,250,252,0)"
PAPER   = "rgba(248,250,252,0)"
GRID    = "rgba(226,232,240,0.8)"
FONT_C  = "#64748b"
MINT    = "#10b981"
STEEL   = "#3b82f6"
AMBER   = "#f59e0b"
RED     = "#ef4444"
VIOLET  = "#8b5cf6"
CYAN    = "#06b6d4"
EMERALD = "#059669"
CAT6    = [MINT, STEEL, AMBER, RED, VIOLET, CYAN]

LIGHT_LAYOUT = dict(
    paper_bgcolor=PAPER,
    plot_bgcolor=BG,
    font=dict(family="Plus Jakarta Sans", color=FONT_C, size=12),
    margin=dict(t=36, b=40, l=50, r=20),
    legend=dict(
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="rgba(226,232,240,0.8)",
        borderwidth=1,
        font=dict(color="#64748b", size=11),
    ),
    xaxis=dict(gridcolor=GRID, linecolor=GRID, tickfont=dict(color=FONT_C), zeroline=False),
    yaxis=dict(gridcolor=GRID, linecolor=GRID, tickfont=dict(color=FONT_C), zeroline=False),
)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:12px 0 24px;'>
      <div style='font-family:Plus Jakarta Sans,sans-serif; font-size:22px; font-weight:800; color:#10b981;'>👥 PeoplePro</div>
      <div style='font-size:10px; color:#94a3b8; letter-spacing:1.5px; text-transform:uppercase; margin-top:3px;'>HR Analytics Platform</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**HR FILTERS**")

    dept_opts = ["All"] + sorted(df_full["department"].unique().tolist())
    dept_sel = st.selectbox("👥 Department", dept_opts)

    edu_opts = df_full["education"].unique().tolist()
    edu_sel = st.multiselect("🎓 Education Level", edu_opts, default=edu_opts)

    status_opts = ["All"] + df_full["employment_status"].unique().tolist()
    status_sel = st.selectbox("📊 Employment Status", status_opts)

    age_range = st.slider("👤 Age Range", 22, 62, (22, 62))

    search_title = st.text_input("🔍 Search Job Title", placeholder="e.g. Engineer, Manager...")

    min_date = df_full["hire_date"].min().date()
    max_date = df_full["hire_date"].max().date()
    hire_range = st.date_input("📅 Hire Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

    st.markdown("<br>", unsafe_allow_html=True)
    apply_btn = st.button("✦ APPLY FILTERS", use_container_width=True)
    reset_btn = st.button("↺ Reset All", use_container_width=True)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:11px; color:#94a3b8; text-align:center; line-height:1.9;'>
    👥 800 employees loaded<br>
    📅 Data: 2019–2026<br>
    🏢 8 Departments
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FILTER LOGIC
# ─────────────────────────────────────────────
df = df_full.copy()
if dept_sel != "All":
    df = df[df["department"] == dept_sel]
if edu_sel:
    df = df[df["education"].isin(edu_sel)]
if status_sel != "All":
    df = df[df["employment_status"] == status_sel]
df = df[(df["age"] >= age_range[0]) & (df["age"] <= age_range[1])]
if search_title:
    df = df[df["job_title"].str.lower().str.contains(search_title.lower())]
if len(hire_range) == 2:
    df = df[(df["hire_date"].dt.date >= hire_range[0]) & (df["hire_date"].dt.date <= hire_range[1])]

# ─────────────────────────────────────────────
# KPI CALCULATIONS
# ─────────────────────────────────────────────
total_emp    = len(df)
avg_tenure   = df["tenure_years"].mean()
avg_perf     = df["performance_score"].mean()
avg_sat      = df["satisfaction_score"].mean()
avg_salary   = df["monthly_salary"].mean()
high_risk_pct = (df["turnover_risk"] > 60).sum() / max(len(df), 1) * 100
prev_emp     = total_emp * 0.95

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class='pp-header'>
  <div>
    <div class='pp-title'>👥 PeoplePro Analytics</div>
    <div class='pp-subtitle'>Human Resources Intelligence Dashboard</div>
  </div>
  <div style='text-align:center;'>
    <div style='font-family:Plus Jakarta Sans,sans-serif; font-size:13px; color:#64748b; font-weight:600;'>WORKFORCE HEALTH</div>
    <div style='font-size:38px; font-weight:800; color:#10b981; line-height:1;'>{100 - high_risk_pct:.0f}<span style='font-size:18px'>/100</span></div>
    <div style='font-size:11px; color:#94a3b8; margin-top:2px;'>Health Score</div>
  </div>
  <div style='text-align:right;'>
    <div class='pp-badge'>✦ LIVE DATA</div>
    <div style='font-size:13px; color:#64748b; margin-top:8px; font-weight:600;'>{total_emp:,} Employees</div>
    <div style='font-size:11px; color:#94a3b8;'>Filtered Results</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI ROW
# ─────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    delta_emp = f"+{total_emp - int(prev_emp)} from last period"
    st.metric("👥 Total Employees", f"{total_emp:,}", delta_emp)
with k2:
    risk_str = "⚠️ High Risk" if high_risk_pct > 20 else "✓ Stable"
    st.metric("🔄 Turnover Risk", f"{high_risk_pct:.1f}%", risk_str, delta_color="inverse")
with k3:
    st.metric("📈 Avg Tenure", f"{avg_tenure:.1f} yrs", "+0.3 vs last yr")
with k4:
    sat_str = "😀 Excellent" if avg_sat >= 7 else ("😐 Moderate" if avg_sat >= 5 else "😟 Needs Work")
    st.metric("😊 Satisfaction", f"{avg_sat:.1f}/10", sat_str)
with k5:
    st.metric("💰 Avg Salary", f"${avg_salary:,.0f}", f"Perf: {avg_perf:.1f}/5")

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🎯 Performance", "🔄 Retention", "🏢 Hiring"])

# ══════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════
with tab1:
    c1, c2 = st.columns(2, gap="medium")

    # CHART 1 — Dept Headcount Bar
    with c1:
        st.markdown("<div class='section-title'>🏢 Headcount by Department</div>", unsafe_allow_html=True)
        dept_count = df.groupby("department").size().reset_index(name="count").sort_values("count", ascending=True)
        fig1 = go.Figure(go.Bar(
            y=dept_count["department"], x=dept_count["count"],
            orientation="h",
            marker=dict(
                color=dept_count["count"],
                colorscale=[[0, "#d1fae5"], [0.5, MINT], [1, EMERALD]],
                showscale=False,
                line=dict(color="white", width=1),
            ),
            text=dept_count["count"],
            textposition="outside",
            textfont=dict(color=FONT_C, size=11, family="Plus Jakarta Sans"),
            hovertemplate="<b>%{y}</b><br>Employees: %{x}<extra></extra>",
        ))
        fig1.update_layout(**LIGHT_LAYOUT, height=300,
            xaxis_title="Headcount", yaxis_title="")
        st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

    # CHART 2 — Education Donut
    with c2:
        st.markdown("<div class='section-title'>🎓 Education Distribution</div>", unsafe_allow_html=True)
        edu_count = df.groupby("education").size().reset_index(name="count")
        fig2 = go.Figure(go.Pie(
            labels=edu_count["education"], values=edu_count["count"],
            hole=0.55,
            marker=dict(colors=[MINT, STEEL, AMBER, EMERALD, VIOLET],
                        line=dict(color="white", width=3)),
            textfont=dict(family="Plus Jakarta Sans", size=11),
            hovertemplate="<b>%{label}</b><br>%{value} employees (%{percent})<extra></extra>",
        ))
        fig2.update_layout(
            **{k: v for k, v in LIGHT_LAYOUT.items() if k not in ["xaxis","yaxis"]},
            height=300,
            annotations=[dict(text=f"<b>{total_emp}</b><br>Total",
                              x=0.5, y=0.5, font=dict(size=15, color="#1e293b",
                              family="Plus Jakarta Sans"), showarrow=False)],
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    c3, c4 = st.columns(2, gap="medium")

    # CHART 3 — Salary by Gender & Dept
    with c3:
        st.markdown("<div class='section-title'>💰 Avg Salary by Department</div>", unsafe_allow_html=True)
        sal_dept = df.groupby(["department","gender"])["monthly_salary"].mean().reset_index()
        sal_dept = sal_dept[sal_dept["gender"].isin(["Male","Female"])]
        fig3 = px.bar(
            sal_dept, x="department", y="monthly_salary", color="gender",
            barmode="group",
            color_discrete_map={"Male": STEEL, "Female": MINT},
        )
        fig3.update_layout(**{k:v for k,v in LIGHT_LAYOUT.items() if k not in ['xaxis']}, height=300,
            yaxis_title="Avg Salary ($)",
            xaxis=dict(gridcolor='rgba(226,232,240,0.8)', linecolor='rgba(226,232,240,0.8)', tickfont=dict(color='#64748b'), zeroline=False, tickangle=-25))
        fig3.update_traces(marker_line_width=0)
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    # CHART 4 — Employment Status
    with c4:
        st.markdown("<div class='section-title'>📋 Employment Status Breakdown</div>", unsafe_allow_html=True)
        status_count = df.groupby("employment_status").size().reset_index(name="count")
        fig4 = px.bar(
            status_count, x="employment_status", y="count",
            color="count",
            color_continuous_scale=[[0,"#dbeafe"],[0.5,STEEL],[1,MINT]],
            text="count",
        )
        fig4.update_traces(textposition="outside", marker_line_width=0)
        fig4.update_layout(**{k: v for k, v in LIGHT_LAYOUT.items() if k != "legend"},
            height=300, xaxis_title="", yaxis_title="Count",
            showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════════
# TAB 2 — PERFORMANCE
# ══════════════════════════════════════════════
with tab2:
    c5, c6 = st.columns(2, gap="medium")

    # CHART 5 — Performance vs Salary Scatter
    with c5:
        st.markdown("<div class='section-title'>🎯 Performance vs Salary</div>", unsafe_allow_html=True)
        fig5 = px.scatter(
            df.sample(min(400, len(df))),
            x="performance_score", y="monthly_salary",
            color="department",
            size="training_hours",
            size_max=18,
            color_discrete_sequence=CAT6,
            opacity=0.75,
            trendline="ols",
            hover_data={"job_title": True, "tenure_years": ":.1f"},
            labels={"performance_score": "Performance Score (0-5)", "monthly_salary": "Monthly Salary ($)"},
        )
        fig5.update_layout(**{k: v for k, v in LIGHT_LAYOUT.items()}, height=340)
        fig5.update_traces(selector=dict(mode="lines"), line=dict(color=RED, width=2, dash="dash"))
        st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})

    # CHART 6 — Performance Distribution
    with c6:
        st.markdown("<div class='section-title'>📊 Performance Score Distribution</div>", unsafe_allow_html=True)
        fig6 = px.histogram(
            df, x="performance_score", nbins=25,
            color="employment_status",
            color_discrete_sequence=[MINT, STEEL, AMBER, VIOLET],
            barmode="overlay", opacity=0.72,
            labels={"performance_score": "Performance Score"},
        )
        fig6.update_layout(**LIGHT_LAYOUT, height=340,
            yaxis_title="Count", bargap=0.05)
        fig6.add_vline(x=df["performance_score"].mean(), line_dash="dash",
                       line_color=RED, annotation_text=f"Avg {avg_perf:.1f}",
                       annotation_font_color=RED, annotation_font_size=11)
        st.plotly_chart(fig6, use_container_width=True, config={"displayModeBar": False})

    # Perf by dept box plot
    st.markdown("<div class='section-title'>📦 Performance Score by Department</div>", unsafe_allow_html=True)
    fig_box = px.box(
        df, x="department", y="performance_score", color="department",
        color_discrete_sequence=CAT6,
        points="outliers",
        labels={"performance_score": "Performance Score", "department": ""},
    )
    fig_box.update_layout(**{k: v for k, v in LIGHT_LAYOUT.items() if k != "legend"},
        height=300, showlegend=False)
    st.plotly_chart(fig_box, use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════════
# TAB 3 — RETENTION
# ══════════════════════════════════════════════
with tab3:
    c7, c8 = st.columns(2, gap="medium")

    # CHART 7 — Turnover Risk Heatmap
    with c7:
        st.markdown("<div class='section-title'>🔥 Turnover Risk Heatmap</div>", unsafe_allow_html=True)
        heat_data = df.groupby(["department","employment_status"])["turnover_risk"].mean().reset_index()
        heat_pivot = heat_data.pivot(index="department", columns="employment_status", values="turnover_risk").fillna(0)
        fig7 = go.Figure(go.Heatmap(
            z=heat_pivot.values,
            x=heat_pivot.columns.tolist(),
            y=heat_pivot.index.tolist(),
            colorscale=[[0,"#d1fae5"],[0.4,AMBER],[1,RED]],
            text=heat_pivot.values.round(1),
            texttemplate="%{text}%",
            textfont=dict(color="#1e293b", size=11, family="Plus Jakarta Sans"),
            hovertemplate="Dept: %{y}<br>Status: %{x}<br>Risk: %{z:.1f}%<extra></extra>",
            colorbar=dict(title="Risk %", tickfont=dict(color=FONT_C), thickness=14),
        ))
        fig7.update_layout(
            paper_bgcolor=PAPER, plot_bgcolor=BG,
            font=dict(family='Plus Jakarta Sans', color=FONT_C, size=12),
            margin=dict(t=36,b=40,l=50,r=20),
            legend=dict(bgcolor='rgba(255,255,255,0.9)', bordercolor='rgba(226,232,240,0.8)', borderwidth=1, font=dict(color='#64748b',size=11)),
            xaxis=dict(title='', tickfont=dict(color=FONT_C), gridcolor=GRID, zeroline=False),
            yaxis=dict(title='', tickfont=dict(color=FONT_C), gridcolor=GRID, zeroline=False),
            height=340,
        )
        st.plotly_chart(fig7, use_container_width=True, config={"displayModeBar": False})

    # CHART 8 — Tenure Histogram
    with c8:
        st.markdown("<div class='section-title'>📅 Tenure Distribution</div>", unsafe_allow_html=True)
        fig8 = px.histogram(df, x="tenure_years", nbins=28,
            color_discrete_sequence=[STEEL], opacity=0.8,
            labels={"tenure_years": "Tenure (Years)"})
        fig8.update_traces(marker_line_color="white", marker_line_width=1)
        fig8.update_layout(**LIGHT_LAYOUT, height=340, yaxis_title="Employees", bargap=0.05)
        fig8.add_vline(x=avg_tenure, line_dash="dash", line_color=MINT,
                       annotation_text=f"Avg {avg_tenure:.1f}y",
                       annotation_font_color=MINT, annotation_font_size=11)
        fig8.add_vline(x=4.1, line_dash="dot", line_color=AMBER,
                       annotation_text="Industry 4.1y",
                       annotation_font_color=AMBER, annotation_font_size=10,
                       annotation_position="top left")
        st.plotly_chart(fig8, use_container_width=True, config={"displayModeBar": False})

    # Satisfaction vs Risk scatter
    st.markdown("<div class='section-title'>💬 Satisfaction vs Turnover Risk</div>", unsafe_allow_html=True)
    fig_sat = px.scatter(
        df.sample(min(400, len(df))),
        x="satisfaction_score", y="turnover_risk",
        color="department",
        size="monthly_salary",
        size_max=15,
        color_discrete_sequence=CAT6,
        opacity=0.7,
        trendline="ols",
        labels={"satisfaction_score": "Satisfaction (0-10)", "turnover_risk": "Turnover Risk (%)"},
    )
    fig_sat.update_layout(**LIGHT_LAYOUT, height=300)
    fig_sat.update_traces(selector=dict(mode="lines"), line=dict(color=RED, width=2, dash="dash"))
    st.plotly_chart(fig_sat, use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════════
# TAB 4 — HIRING
# ══════════════════════════════════════════════
with tab4:
    c9, c10 = st.columns(2, gap="medium")

    # CHART 9 — Monthly Hires Area
    with c9:
        st.markdown("<div class='section-title'>📈 Monthly Hiring Trend</div>", unsafe_allow_html=True)
        monthly_hires = df.groupby("hire_month").size().reset_index(name="hires")
        monthly_hires = monthly_hires.tail(24)
        fig9 = go.Figure()
        fig9.add_trace(go.Scatter(
            x=monthly_hires["hire_month"], y=monthly_hires["hires"],
            mode="lines+markers",
            fill="tozeroy",
            fillcolor=f"rgba(16,185,129,0.12)",
            line=dict(color=MINT, width=2.5),
            marker=dict(color=MINT, size=5, line=dict(color="white", width=1)),
            hovertemplate="Month: %{x}<br>Hires: %{y}<extra></extra>",
        ))
        fig9.update_layout(**{k:v for k,v in LIGHT_LAYOUT.items() if k not in ['xaxis']}, height=320,
            yaxis_title="New Hires",
            xaxis=dict(title='Month', gridcolor=GRID, linecolor=GRID, tickfont=dict(color=FONT_C, size=10), zeroline=False, tickangle=-45))
        st.plotly_chart(fig9, use_container_width=True, config={"displayModeBar": False})

    # CHART 10 — Hires by Year & Dept
    with c10:
        st.markdown("<div class='section-title'>🏢 Hires by Year & Department</div>", unsafe_allow_html=True)
        yr_dept = df.groupby(["hire_year","department"]).size().reset_index(name="hires")
        fig10 = px.bar(
            yr_dept, x="hire_year", y="hires", color="department",
            color_discrete_sequence=CAT6,
            barmode="stack",
            labels={"hire_year": "Year", "hires": "New Hires"},
        )
        fig10.update_layout(**LIGHT_LAYOUT, height=320)
        fig10.update_traces(marker_line_width=0)
        st.plotly_chart(fig10, use_container_width=True, config={"displayModeBar": False})

    # Salary vs Tenure by dept
    st.markdown("<div class='section-title'>💼 Salary Growth with Tenure</div>", unsafe_allow_html=True)
    fig_sal_ten = px.scatter(
        df.sample(min(400, len(df))),
        x="tenure_years", y="monthly_salary",
        color="department",
        trendline="ols",
        color_discrete_sequence=CAT6,
        opacity=0.65,
        size_max=12,
        labels={"tenure_years": "Tenure (Years)", "monthly_salary": "Salary ($)"},
    )
    fig_sal_ten.update_layout(**LIGHT_LAYOUT, height=300)
    st.plotly_chart(fig_sal_ten, use_container_width=True, config={"displayModeBar": False})

# ─────────────────────────────────────────────
# TEAM TABLE
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<div class='section-title'>👥 Live Team Directory</div>", unsafe_allow_html=True)

def risk_badge(r):
    if r >= 60: return "🔴 HIGH"
    elif r >= 35: return "🟡 MEDIUM"
    else: return "🟢 LOW"

table_df = df.nlargest(25, "turnover_risk")[
    ["employee_id","name","department","job_title","tenure_years","performance_score","monthly_salary","turnover_risk"]
].copy()
table_df["Risk Level"] = table_df["turnover_risk"].apply(risk_badge)
table_df.columns = ["ID","Employee","Department","Job Title","Tenure (yrs)","Perf Score","Salary ($)","Risk %","Risk Level"]
table_df["Salary ($)"] = table_df["Salary ($)"].apply(lambda x: f"${x:,}")
table_df["Perf Score"] = table_df["Perf Score"].apply(lambda x: f"{x:.1f}/5")
table_df["Risk %"] = table_df["Risk %"].apply(lambda x: f"{x:.1f}%")

st.dataframe(table_df.reset_index(drop=True), use_container_width=True, height=380)

# ─────────────────────────────────────────────
# RISK SUMMARY METRICS
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("🔴 High Risk Employees", f"{(df['turnover_risk']>=60).sum():,}",
              f"{(df['turnover_risk']>=60).sum()/max(len(df),1)*100:.1f}% of workforce", delta_color="inverse")
with m2:
    st.metric("🟡 Medium Risk Employees", f"{((df['turnover_risk']>=35)&(df['turnover_risk']<60)).sum():,}",
              "Watch closely", delta_color="off")
with m3:
    st.metric("🟢 Engaged Employees", f"{(df['turnover_risk']<35).sum():,}",
              f"{(df['turnover_risk']<35).sum()/max(len(df),1)*100:.1f}% stable")

# ─────────────────────────────────────────────
# ACTION BUTTONS
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<div class='section-title'>⚡ Quick Actions</div>", unsafe_allow_html=True)

a1, a2, a3 = st.columns(3, gap="medium")
with a1:
    if st.button("📊 Export Team Report (CSV)", use_container_width=True):
        csv = df.to_csv(index=False)
        st.download_button("⬇️ Download CSV", csv, "hr_team_report.csv", "text/csv", use_container_width=True)
with a2:
    if st.button("💎 Order Custom Dashboard — $25", use_container_width=True):
        st.info("🌐 Visit our website to place your order for a custom dashboard. https://ilyasarain943.github.io/ilyas-dashboard-portfolio/")

with a3:
    if st.button("👥 Upload Your Employee Data (CSV)", use_container_width=True):
        st.info("📂 Upload feature: integrate with your own employee CSV for live analysis.")

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class='footer-bar'>
  <div>
    <span class='footer-brand'>👥 PeoplePro Analytics</span>
    &nbsp;·&nbsp; Arctic White Edition &nbsp;·&nbsp; © 2026
  </div>
  <div style='color:#94a3b8; font-size:12px;'>
    Human Resources Intelligence Dashboard
  </div>
  <div style='font-size:12px; color:#94a3b8;'>
    Custom HR dashboards available — visit our website to order
  </div>
</div>
""", unsafe_allow_html=True)