import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="PeopleFlow Analytics | IBM HR",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CSS — Mint Arctic White
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&family=Fraunces:ital,wght@0,400;0,700;1,400&display=swap');

:root {
  --bg-main:     #f0fdf4;
  --bg-surface:  #f8fefc;
  --bg-card:     rgba(255,255,255,0.97);
  --mint:        #10b981;
  --mint-mid:    #34d399;
  --mint-light:  #d1fae5;
  --mint-dark:   #059669;
  --mint-xlight: #ecfdf5;
  --steel:       #3b82f6;
  --steel-light: #dbeafe;
  --amber:       #f59e0b;
  --amber-light: #fef3c7;
  --rose:        #ef4444;
  --rose-light:  #fee2e2;
  --violet:      #8b5cf6;
  --cyan:        #06b6d4;
  --text-dark:   #1e293b;
  --text-mid:    #475569;
  --text-muted:  #94a3b8;
  --border:      #e2e8f0;
  --border-mint: rgba(16,185,129,0.30);
  --shadow-sm:   0 1px 3px rgba(0,0,0,0.05);
  --shadow-md:   0 4px 16px rgba(0,0,0,0.07);
  --shadow-lg:   0 12px 36px rgba(0,0,0,0.09);
  --shadow-mint: 0 6px 20px rgba(16,185,129,0.22);
}

html, body, [class*="css"] {
  font-family: 'Manrope', sans-serif !important;
  color: var(--text-dark) !important;
}

.stApp {
  background: var(--bg-main) !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
  background: #ffffff !important;
  border-right: 1.5px solid var(--border) !important;
  box-shadow: 3px 0 16px rgba(16,185,129,0.06) !important;
}

[data-testid="stSidebar"] * { color: var(--text-dark) !important; }

[data-testid="stSidebar"] label {
  font-size: 10.5px !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: 1.3px !important;
  color: var(--text-muted) !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-baseweb="input"] {
  background: var(--bg-main) !important;
  border: 1.5px solid var(--border) !important;
  border-radius: 10px !important;
  color: var(--text-dark) !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div:focus-within,
[data-testid="stSidebar"] [data-baseweb="input"]:focus-within {
  border-color: var(--mint) !important;
  box-shadow: 0 0 0 3px rgba(16,185,129,0.10) !important;
}

[data-testid="stSidebar"] [data-baseweb="tag"] {
  background: var(--mint-light) !important;
  border: 1px solid var(--border-mint) !important;
  border-radius: 6px !important;
  color: var(--mint-dark) !important;
}

[data-testid="stSidebar"] [data-baseweb="tag"] span { color: var(--mint-dark) !important; }
[data-testid="stSidebar"] [data-baseweb="select"] input { background: transparent !important; color: var(--text-dark) !important; }

[data-baseweb="popover"] ul, [data-baseweb="popover"] [data-baseweb="menu"] {
  background: #ffffff !important; border: 1px solid var(--border) !important;
  box-shadow: var(--shadow-lg) !important; border-radius: 12px !important;
}
[data-baseweb="popover"] li { background: #ffffff !important; color: var(--text-dark) !important; }
[data-baseweb="popover"] li:hover { background: var(--mint-xlight) !important; color: var(--mint-dark) !important; }

[data-baseweb="calendar"] {
  background: #ffffff !important; border: 1px solid var(--border) !important;
  border-radius: 14px !important; box-shadow: var(--shadow-lg) !important;
}
[data-baseweb="calendar"] * { color: var(--text-dark) !important; }
[data-baseweb="calendar"] [aria-selected="true"] div { background: var(--mint) !important; color: white !important; }

[data-testid="stSidebar"] [data-baseweb="slider"] div[role="slider"] {
  background: var(--mint) !important; border: 2px solid var(--mint-dark) !important;
}

/* ── METRICS ── */
[data-testid="stMetric"] {
  background: var(--bg-card) !important;
  border: 1.5px solid var(--border) !important;
  border-radius: 20px !important;
  padding: 22px 20px !important;
  box-shadow: var(--shadow-md) !important;
  transition: all 0.22s ease !important;
  position: relative !important;
  overflow: hidden !important;
}
[data-testid="stMetric"]::before {
  content: '' !important;
  position: absolute !important;
  top: 0; left: 0 !important;
  width: 4px; height: 100% !important;
  background: var(--mint) !important;
  border-radius: 4px 0 0 4px !important;
}
[data-testid="stMetric"]:hover {
  transform: translateY(-3px) !important;
  box-shadow: var(--shadow-mint) !important;
  border-color: var(--border-mint) !important;
}
[data-testid="stMetricLabel"] {
  font-size: 10.5px !important; font-weight: 700 !important;
  text-transform: uppercase !important; letter-spacing: 1.4px !important;
  color: var(--text-muted) !important;
}
[data-testid="stMetricValue"] {
  font-family: 'Manrope', sans-serif !important;
  font-size: 32px !important; font-weight: 800 !important;
  color: var(--text-dark) !important; line-height: 1.1 !important;
}

/* ── TABS ── */
[data-testid="stTabs"] [role="tablist"] {
  background: #ffffff !important; border-radius: 14px !important;
  padding: 5px !important; border: 1.5px solid var(--border) !important;
  box-shadow: var(--shadow-sm) !important;
}
[data-testid="stTabs"] [role="tab"] {
  font-family: 'Manrope', sans-serif !important; font-weight: 600 !important;
  font-size: 13px !important; color: var(--text-mid) !important;
  border-radius: 10px !important; padding: 9px 22px !important;
  transition: all 0.2s !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
  background: var(--mint) !important; color: white !important;
  box-shadow: var(--shadow-mint) !important;
}

/* ── BUTTONS ── */
.stButton > button {
  background: var(--mint) !important; color: white !important;
  border: none !important; border-radius: 12px !important;
  font-family: 'Manrope', sans-serif !important; font-weight: 700 !important;
  font-size: 13px !important; padding: 12px 22px !important;
  box-shadow: var(--shadow-mint) !important;
  transition: all 0.2s !important; width: 100% !important;
}
.stButton > button:hover {
  background: var(--mint-dark) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 10px 28px rgba(16,185,129,0.35) !important;
}

/* ── DATAFRAME ── */
.stDataFrame { border: 1.5px solid var(--border) !important; border-radius: 16px !important; overflow: hidden !important; box-shadow: var(--shadow-sm) !important; }
.stPlotlyChart { border-radius: 16px !important; overflow: hidden !important; }
.stTextInput input {
  background: var(--bg-main) !important; border: 1.5px solid var(--border) !important;
  border-radius: 10px !important; color: var(--text-dark) !important;
  font-family: 'Manrope', sans-serif !important;
}
.stTextInput input:focus { border-color: var(--mint) !important; box-shadow: 0 0 0 3px rgba(16,185,129,0.10) !important; }

/* ── CUSTOM HTML COMPONENTS ── */
.pf-header {
  background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 60%, #ecfdf5 100%);
  border: 1.5px solid var(--border);
  border-left: 5px solid var(--mint);
  border-radius: 20px;
  padding: 24px 32px;
  margin-bottom: 22px;
  display: flex; align-items: center; justify-content: space-between;
  box-shadow: var(--shadow-md);
  position: relative; overflow: hidden;
}
.pf-header::after {
  content: ''; position: absolute; right: -30px; top: -30px;
  width: 140px; height: 140px;
  background: radial-gradient(circle, rgba(16,185,129,0.08) 0%, transparent 70%);
  border-radius: 50%;
}
.pf-title {
  font-family: 'Fraunces', serif; font-size: 30px; font-weight: 700;
  color: var(--text-dark); letter-spacing: -0.3px; margin: 0;
}
.pf-subtitle {
  font-size: 11.5px; color: var(--text-muted);
  letter-spacing: 1.4px; text-transform: uppercase; font-weight: 600; margin-top: 4px;
}
.kpi-tag {
  background: var(--mint-xlight); color: var(--mint-dark);
  font-size: 11px; font-weight: 700; padding: 4px 12px;
  border-radius: 20px; letter-spacing: 0.5px;
  border: 1px solid var(--border-mint); display: inline-block;
}
.section-title {
  font-family: 'Manrope', sans-serif; font-size: 15px; font-weight: 700;
  color: var(--text-dark); margin: 18px 0 10px 0;
}
.attrition-badge-yes { color: #ef4444; font-weight: 700; font-size: 11.5px; background: #fee2e2; padding: 3px 8px; border-radius: 6px; }
.attrition-badge-no  { color: #059669; font-weight: 700; font-size: 11.5px; background: #d1fae5; padding: 3px 8px; border-radius: 6px; }
.risk-high   { color: #ef4444; font-weight: 700; font-size: 11px; background: #fee2e2; padding: 2px 8px; border-radius: 5px; }
.risk-med    { color: #d97706; font-weight: 700; font-size: 11px; background: #fef3c7; padding: 2px 8px; border-radius: 5px; }
.risk-low    { color: #059669; font-weight: 700; font-size: 11px; background: #d1fae5; padding: 2px 8px; border-radius: 5px; }
.footer-bar {
  background: linear-gradient(90deg, #ffffff 0%, #f0fdf4 50%, #ffffff 100%);
  border: 1.5px solid var(--border); border-top: 3px solid var(--mint);
  border-radius: 14px; padding: 16px 28px; margin-top: 30px;
  display: flex; align-items: center; justify-content: space-between;
  font-size: 13px; color: var(--text-muted); box-shadow: var(--shadow-sm);
}
.footer-brand { font-family: 'Fraunces', serif; font-weight: 700; color: var(--text-dark); }

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
.stDeployButton { display: none; }
header[data-testid="stHeader"] { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA — IBM HR Analytics Simulation
# ─────────────────────────────────────────────
@st.cache_data
def generate_ibm_hr(n=1470):
    np.random.seed(42)
    random.seed(42)
    departments   = ["Sales", "Research & Development", "Human Resources"]
    edu_fields    = ["Life Sciences", "Medical", "Marketing", "Technical Degree", "Human Resources", "Other"]
    job_roles     = {
        "Sales":                    ["Sales Executive", "Sales Representative", "Manager"],
        "Research & Development":   ["Research Scientist", "Laboratory Technician", "Healthcare Representative", "Manufacturing Director", "Manager"],
        "Human Resources":          ["Human Resources", "Manager"],
    }
    marital_status = ["Single", "Married", "Divorced"]
    over_time_prob = 0.28

    rows = []
    for i in range(n):
        dept = random.choice(departments)
        role = random.choice(job_roles[dept])
        age  = int(np.random.normal(37, 9))
        edu  = np.random.choice([1,2,3,4,5], p=[0.11,0.19,0.39,0.21,0.10])
        edu_field = np.random.choice(edu_fields, p=[0.41,0.21,0.11,0.14,0.06,0.07])
        yrs  = max(0, int(np.random.exponential(7)))
        satisfaction = np.random.choice([1,2,3,4], p=[0.12,0.20,0.35,0.33])
        env_satisfaction = np.random.choice([1,2,3,4], p=[0.10,0.22,0.36,0.32])
        perf = np.random.choice([3,4], p=[0.85, 0.15])
        income_base = {"Sales":5500,"Research & Development":6500,"Human Resources":4800}
        income = int(income_base[dept] * np.random.uniform(0.55, 1.90))
        hours  = int(np.random.normal(80, 12))
        gender = np.random.choice(["Male","Female"], p=[0.60,0.40])
        overtime = np.random.choice(["Yes","No"], p=[over_time_prob, 1-over_time_prob])
        travel = np.random.choice(["Non-Travel","Travel_Rarely","Travel_Frequently"], p=[0.19,0.71,0.10])
        last_promo = np.random.randint(0, min(yrs+1, 15)+1)

        # Attrition logic: low satisfaction + overtime + young + low income → higher risk
        attrition_prob = 0.12
        if satisfaction <= 2: attrition_prob += 0.12
        if overtime == "Yes":  attrition_prob += 0.10
        if age < 30:           attrition_prob += 0.07
        if income < 4000:      attrition_prob += 0.06
        if yrs < 2:            attrition_prob += 0.08
        attrition = "Yes" if random.random() < attrition_prob else "No"

        # Risk score
        risk = int(min(100, (5-satisfaction)*12 + (int(overtime=="Yes")*20) +
                       max(0,(32-age))*0.8 + max(0,(5000-income)/200) + (yrs<2)*15))

        rows.append({
            "EmployeeID": f"IBM{i+1001:04d}",
            "Age": max(18, min(65, age)),
            "Gender": gender,
            "Department": dept,
            "JobRole": role,
            "EducationField": edu_field,
            "Education": edu,
            "YearsAtCompany": min(40, yrs),
            "JobSatisfaction": satisfaction,
            "EnvironmentSatisfaction": env_satisfaction,
            "PerformanceRating": perf,
            "MonthlyIncome": income,
            "MonthlyHours": max(40, min(120, hours)),
            "OverTime": overtime,
            "BusinessTravel": travel,
            "MaritalStatus": np.random.choice(marital_status, p=[0.32,0.46,0.22]),
            "YearsSinceLastPromotion": last_promo,
            "Attrition": attrition,
            "RiskScore": risk,
        })
    return pd.DataFrame(rows)

df_full = generate_ibm_hr(1470)

# ─────────────────────────────────────────────
# CHART THEME
# ─────────────────────────────────────────────
_BG    = "rgba(240,253,244,0)"
_PAPER = "rgba(240,253,244,0)"
_GRID  = "rgba(226,232,240,0.7)"
_FC    = "#64748b"
MINT   = "#10b981"; STEEL  = "#3b82f6"; AMBER  = "#f59e0b"
ROSE   = "#ef4444"; VIOLET = "#8b5cf6"; CYAN   = "#06b6d4"
EMLD   = "#059669"; PINK   = "#ec4899"
CAT7   = [MINT, STEEL, AMBER, ROSE, VIOLET, CYAN, PINK]

def _L(**extra):
    base = dict(
        paper_bgcolor=_PAPER, plot_bgcolor=_BG,
        font=dict(family="Manrope", color=_FC, size=12),
        margin=dict(t=36, b=40, l=50, r=20),
        legend=dict(bgcolor="rgba(255,255,255,0.9)", bordercolor=_GRID, borderwidth=1,
                    font=dict(color=_FC, size=11)),
        xaxis=dict(gridcolor=_GRID, linecolor=_GRID, tickfont=dict(color=_FC), zeroline=False),
        yaxis=dict(gridcolor=_GRID, linecolor=_GRID, tickfont=dict(color=_FC), zeroline=False),
    )
    base.update(extra)
    return base

def _L_no(*skip, **extra):
    base = dict(
        paper_bgcolor=_PAPER, plot_bgcolor=_BG,
        font=dict(family="Manrope", color=_FC, size=12),
        margin=dict(t=36, b=40, l=50, r=20),
        legend=dict(bgcolor="rgba(255,255,255,0.9)", bordercolor=_GRID, borderwidth=1,
                    font=dict(color=_FC, size=11)),
    )
    if "xaxis" not in skip:
        base["xaxis"] = dict(gridcolor=_GRID, linecolor=_GRID, tickfont=dict(color=_FC), zeroline=False)
    if "yaxis" not in skip:
        base["yaxis"] = dict(gridcolor=_GRID, linecolor=_GRID, tickfont=dict(color=_FC), zeroline=False)
    base.update(extra)
    return base

# ─────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:10px 0 22px;'>
      <div style='font-family:Fraunces,serif; font-size:22px; font-weight:700; color:#10b981;'>🌿 PeopleFlow</div>
      <div style='font-size:10px; color:#94a3b8; letter-spacing:1.6px; text-transform:uppercase; margin-top:3px;'>IBM HR Analytics</div>
    </div>
    """, unsafe_allow_html=True)

    dept_opts = df_full["Department"].unique().tolist()
    dept_sel  = st.multiselect("👥 Department", dept_opts, default=dept_opts)

    edu_opts = df_full["EducationField"].unique().tolist()
    edu_sel  = st.multiselect("🎓 Education Field", edu_opts, default=edu_opts)

    gender_opts = ["All", "Male", "Female"]
    gender_sel  = st.selectbox("👤 Gender", gender_opts)

    sat_range = st.slider("📊 Job Satisfaction (1–4)", 1, 4, (1, 4))

    yrs_range = st.slider("📅 Years at Company", 0, 40, (0, 40))

    attr_opts = ["All", "Yes (Left)", "No (Stayed)"]
    attr_sel  = st.selectbox("⚠️ Attrition Status", attr_opts)

    search_role = st.text_input("🔍 Search Job Role", placeholder="e.g. Scientist, Manager...")

    st.markdown("<br>", unsafe_allow_html=True)
    st.button("✦ APPLY FILTERS", use_container_width=True)
    st.button("↺ Reset All", use_container_width=True)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:11px; color:#94a3b8; text-align:center; line-height:2;'>
    📋 1,470 IBM Employees<br>
    🏢 3 Departments<br>
    📊 Based on Kaggle Dataset
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FILTER LOGIC
# ─────────────────────────────────────────────
df = df_full.copy()
if dept_sel:        df = df[df["Department"].isin(dept_sel)]
if edu_sel:         df = df[df["EducationField"].isin(edu_sel)]
if gender_sel != "All": df = df[df["Gender"] == gender_sel]
df = df[(df["JobSatisfaction"] >= sat_range[0]) & (df["JobSatisfaction"] <= sat_range[1])]
df = df[(df["YearsAtCompany"]  >= yrs_range[0])  & (df["YearsAtCompany"]  <= yrs_range[1])]
if attr_sel == "Yes (Left)":    df = df[df["Attrition"] == "Yes"]
elif attr_sel == "No (Stayed)": df = df[df["Attrition"] == "No"]
if search_role: df = df[df["JobRole"].str.lower().str.contains(search_role.lower())]

# ─────────────────────────────────────────────
# KPIs
# ─────────────────────────────────────────────
total       = len(df)
attr_rate   = (df["Attrition"] == "Yes").sum() / max(total, 1) * 100
avg_tenure  = df["YearsAtCompany"].mean()
top_perf    = (df["PerformanceRating"] == 4).sum() / max(total, 1) * 100
avg_income  = df["MonthlyIncome"].mean()
avg_sat     = df["JobSatisfaction"].mean()
ot_pct      = (df["OverTime"] == "Yes").sum() / max(total, 1) * 100
high_risk   = (df["RiskScore"] > 55).sum()

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class='pf-header'>
  <div>
    <div class='pf-title'>🌿 PeopleFlow Analytics</div>
    <div class='pf-subtitle'>IBM HR Workforce Intelligence · {total:,} Employees</div>
  </div>
  <div style='text-align:center;'>
    <div style='font-size:11px; color:#94a3b8; font-weight:700; letter-spacing:1px; text-transform:uppercase;'>Attrition Risk</div>
    <div style='font-size:40px; font-weight:800; color:{"#ef4444" if attr_rate>15 else "#10b981"}; font-family:Fraunces,serif; line-height:1;'>{attr_rate:.1f}%</div>
    <div class='kpi-tag'>{"⚠️ High Risk" if attr_rate > 15 else "✓ Healthy"}</div>
  </div>
  <div style='text-align:right;'>
    <div style='font-size:13px; color:#64748b; font-weight:600;'>💰 Avg Income: <strong style="color:#1e293b;">${avg_income:,.0f}</strong></div>
    <div style='font-size:13px; color:#64748b; font-weight:600; margin-top:4px;'>⏱️ Overtime: <strong style="color:#f59e0b;">{ot_pct:.0f}%</strong></div>
    <div style='font-size:11px; color:#94a3b8; margin-top:6px;'>© 2026 PeopleFlow</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI ROW
# ─────────────────────────────────────────────
k1,k2,k3,k4,k5,k6 = st.columns(6)
with k1: st.metric("👥 Headcount",     f"{total:,}",          f"+{total - int(total*0.95)} growth")
with k2: st.metric("⚠️ Attrition Rate", f"{attr_rate:.1f}%",   "⚠️ High" if attr_rate>15 else "✓ Stable", delta_color="inverse")
with k3: st.metric("📅 Avg Tenure",    f"{avg_tenure:.1f} yrs","vs 4.2y industry")
with k4: st.metric("🏆 Top Performers",f"{top_perf:.1f}%",     f"{int(top_perf/100*total)} employees")
with k5: st.metric("😊 Avg Satisfaction",f"{avg_sat:.1f}/4",   "😀 Good" if avg_sat >= 3 else "😐 Watch")
with k6: st.metric("🔴 High Risk",     f"{high_risk:,}",       f"{high_risk/max(total,1)*100:.0f}% flagged", delta_color="inverse")

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🎯 Performance", "🔄 Retention", "🧬 Demographics"])

# ══════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════
with tab1:
    c1, c2 = st.columns(2, gap="medium")

    # CHART 1 — Attrition by Dept (Grouped Bar)
    with c1:
        st.markdown("<div class='section-title'>⚠️ Attrition Rate by Department</div>", unsafe_allow_html=True)
        att_dept = df.groupby("Department")["Attrition"].apply(lambda x: (x=="Yes").mean()*100).reset_index()
        att_dept.columns = ["Department","Attrition Rate (%)"]
        fig1 = go.Figure(go.Bar(
            x=att_dept["Department"], y=att_dept["Attrition Rate (%)"],
            marker=dict(
                color=att_dept["Attrition Rate (%)"],
                colorscale=[[0,"#d1fae5"],[0.4,AMBER],[1,ROSE]],
                showscale=False, line=dict(color="white", width=1),
            ),
            text=att_dept["Attrition Rate (%)"].apply(lambda x: f"{x:.1f}%"),
            textposition="outside",
            textfont=dict(color=_FC, size=11),
            hovertemplate="<b>%{x}</b><br>Attrition: %{y:.1f}%<extra></extra>",
        ))
        fig1.update_layout(**_L(height=300, yaxis_title="Attrition Rate (%)", xaxis_title=""))
        st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

    # CHART 2 — Dept Turnover Donut
    with c2:
        st.markdown("<div class='section-title'>🍩 Department Size Split</div>", unsafe_allow_html=True)
        dept_size = df.groupby("Department").size().reset_index(name="count")
        fig2 = go.Figure(go.Pie(
            labels=dept_size["Department"], values=dept_size["count"],
            hole=0.58,
            marker=dict(colors=[MINT, STEEL, AMBER], line=dict(color="white", width=3)),
            textfont=dict(family="Manrope", size=11),
            hovertemplate="<b>%{label}</b><br>%{value} employees (%{percent})<extra></extra>",
        ))
        fig2.update_layout(
            **_L_no("xaxis","yaxis", height=300),
            annotations=[dict(text=f"<b>{total:,}</b><br>Total",
                x=0.5, y=0.5, font=dict(size=14, color="#1e293b", family="Manrope"), showarrow=False)],
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    c3, c4 = st.columns(2, gap="medium")

    # CHART 3 — Income vs Satisfaction Scatter
    with c3:
        st.markdown("<div class='section-title'>💰 Income vs Job Satisfaction</div>", unsafe_allow_html=True)
        fig3 = px.scatter(
            df.sample(min(500,len(df))),
            x="JobSatisfaction", y="MonthlyIncome",
            color="Department",
            size="YearsAtCompany", size_max=18,
            color_discrete_map={"Sales":MINT,"Research & Development":STEEL,"Human Resources":AMBER},
            opacity=0.7,
            hover_data={"JobRole":True,"Age":True},
            labels={"JobSatisfaction":"Satisfaction (1-4)","MonthlyIncome":"Monthly Income ($)"},
        )
        fig3.update_layout(**_L(height=300))
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    # CHART 4 — Monthly Hours Histogram
    with c4:
        st.markdown("<div class='section-title'>⏱️ Monthly Hours Distribution</div>", unsafe_allow_html=True)
        fig4 = px.histogram(
            df, x="MonthlyHours", nbins=30,
            color="OverTime",
            color_discrete_map={"Yes": ROSE, "No": MINT},
            barmode="overlay", opacity=0.75,
            labels={"MonthlyHours":"Monthly Hours"},
        )
        fig4.update_layout(**_L(height=300, yaxis_title="Count"), bargap=0.04)
        fig4.add_vline(x=df["MonthlyHours"].mean(), line_dash="dash",
                       line_color=STEEL, annotation_text=f"Avg {df['MonthlyHours'].mean():.0f}h",
                       annotation_font_color=STEEL, annotation_font_size=11)
        fig4.add_vrect(x0=100, x1=120, fillcolor=ROSE, opacity=0.07, line_width=0,
                       annotation_text="⚠️ Overwork Zone", annotation_font_color=ROSE,
                       annotation_font_size=10)
        st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

    # CHART 5 — Tenure by Dept Grouped Bar
    st.markdown("<div class='section-title'>📅 Avg Tenure by Department & Attrition</div>", unsafe_allow_html=True)
    ten_dept = df.groupby(["Department","Attrition"])["YearsAtCompany"].mean().reset_index()
    fig5 = px.bar(ten_dept, x="Department", y="YearsAtCompany", color="Attrition",
                  barmode="group",
                  color_discrete_map={"Yes":ROSE,"No":MINT},
                  text=ten_dept["YearsAtCompany"].apply(lambda x: f"{x:.1f}y"),
                  labels={"YearsAtCompany":"Avg Tenure (Years)","Department":""})
    fig5.update_traces(textposition="outside", marker_line_width=0)
    fig5.update_layout(**_L(height=280))
    st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════════
# TAB 2 — PERFORMANCE
# ══════════════════════════════════════════════
with tab2:
    c5, c6 = st.columns(2, gap="medium")

    # CHART 6 — Performance Rating Distribution
    with c5:
        st.markdown("<div class='section-title'>🏆 Performance Rating by Department</div>", unsafe_allow_html=True)
        perf_dept = df.groupby(["Department","PerformanceRating"]).size().reset_index(name="count")
        perf_dept["Rating Label"] = perf_dept["PerformanceRating"].map({3:"Excellent", 4:"Outstanding"})
        fig6 = px.bar(perf_dept, x="Department", y="count", color="Rating Label",
                      barmode="group",
                      color_discrete_map={"Excellent":STEEL, "Outstanding":MINT},
                      labels={"count":"Employees","Department":""})
        fig6.update_traces(marker_line_width=0)
        fig6.update_layout(**_L(height=320))
        st.plotly_chart(fig6, use_container_width=True, config={"displayModeBar": False})

    # CHART 7 — Performance vs Income box
    with c6:
        st.markdown("<div class='section-title'>💰 Income by Performance Rating</div>", unsafe_allow_html=True)
        df["Rating Label"] = df["PerformanceRating"].map({3:"Excellent", 4:"Outstanding"})
        fig7 = px.box(df, x="Rating Label", y="MonthlyIncome", color="Rating Label",
                      color_discrete_map={"Excellent":STEEL,"Outstanding":MINT},
                      points="outliers",
                      labels={"MonthlyIncome":"Monthly Income ($)","Rating Label":""})
        fig7.update_layout(**_L_no("legend", height=320), showlegend=False)
        st.plotly_chart(fig7, use_container_width=True, config={"displayModeBar": False})

    # CHART 8 — Performance by Education Field
    st.markdown("<div class='section-title'>🎓 Top Performer % by Education Field</div>", unsafe_allow_html=True)
    top_edu = df.groupby("EducationField")["PerformanceRating"].apply(lambda x: (x==4).mean()*100).reset_index()
    top_edu.columns = ["EducationField","Top Performer (%)"]
    top_edu = top_edu.sort_values("Top Performer (%)", ascending=True)
    fig8 = go.Figure(go.Bar(
        y=top_edu["EducationField"], x=top_edu["Top Performer (%)"],
        orientation="h",
        marker=dict(color=top_edu["Top Performer (%)"],
                    colorscale=[[0,"#dbeafe"],[0.5,STEEL],[1,MINT]],
                    showscale=False, line=dict(color="white",width=1)),
        text=top_edu["Top Performer (%)"].apply(lambda x: f"{x:.1f}%"),
        textposition="outside",
        textfont=dict(color=_FC, size=11),
    ))
    fig8.update_layout(**_L(height=300, xaxis_title="Top Performer (%)", yaxis_title=""))
    st.plotly_chart(fig8, use_container_width=True, config={"displayModeBar": False})

    # Top Performers Table
    st.markdown("<div class='section-title'>🌟 Top Performers (Rating 4 — Outstanding)</div>", unsafe_allow_html=True)
    top_df = df[df["PerformanceRating"]==4].nlargest(20,"MonthlyIncome")[
        ["EmployeeID","Age","Gender","Department","JobRole","YearsAtCompany","JobSatisfaction","MonthlyIncome","RiskScore"]
    ].copy()
    top_df["Monthly Income"] = top_df["MonthlyIncome"].apply(lambda x: f"${x:,}")
    top_df["Risk"] = top_df["RiskScore"].apply(lambda r: "🔴 HIGH" if r>55 else ("🟡 MED" if r>30 else "🟢 LOW"))
    top_df = top_df.drop(columns=["MonthlyIncome","RiskScore"])
    top_df.columns = ["ID","Age","Gender","Department","Job Role","Tenure (y)","Satisfaction","Income","Risk"]
    st.dataframe(top_df.reset_index(drop=True), use_container_width=True, height=340)

# ══════════════════════════════════════════════
# TAB 3 — RETENTION
# ══════════════════════════════════════════════
with tab3:
    c7, c8 = st.columns(2, gap="medium")

    # CHART 9 — Survival Curve (Kaplan-Meier style)
    with c7:
        st.markdown("<div class='section-title'>📈 Retention Survival Curve</div>", unsafe_allow_html=True)
        yrs_bins = list(range(0, 41))
        stayed_pct, left_pct = [], []
        for y in yrs_bins:
            cohort = df[df["YearsAtCompany"] >= y]
            if len(cohort) == 0: stayed_pct.append(np.nan); left_pct.append(np.nan); continue
            survived = (cohort["Attrition"] == "No").mean() * 100
            stayed_pct.append(survived)
            left_pct.append(100 - survived)
        surv_df = pd.DataFrame({"Year": yrs_bins, "Retained (%)": stayed_pct})
        surv_df = surv_df.dropna()
        fig9 = go.Figure()
        fig9.add_trace(go.Scatter(
            x=surv_df["Year"], y=surv_df["Retained (%)"],
            mode="lines", fill="tozeroy",
            fillcolor="rgba(16,185,129,0.10)",
            line=dict(color=MINT, width=2.5),
            name="Retention %",
            hovertemplate="Year %{x}: %{y:.1f}% retained<extra></extra>",
        ))
        fig9.add_hline(y=80, line_dash="dot", line_color=AMBER,
                       annotation_text="80% threshold", annotation_font_color=AMBER)
        fig9.update_layout(**_L(height=330, xaxis_title="Years at Company", yaxis_title="% Retained"))
        st.plotly_chart(fig9, use_container_width=True, config={"displayModeBar": False})

    # CHART 10 — Attrition Risk Heatmap
    with c8:
        st.markdown("<div class='section-title'>🔥 Attrition Heatmap (Dept × Satisfaction)</div>", unsafe_allow_html=True)
        heat = df.groupby(["Department","JobSatisfaction"])["Attrition"].apply(
            lambda x: (x=="Yes").mean()*100).reset_index()
        heat.columns = ["Department","JobSatisfaction","Attrition (%)"]
        pivot = heat.pivot(index="Department", columns="JobSatisfaction", values="Attrition (%)").fillna(0)
        pivot.columns = [f"Sat {c}" for c in pivot.columns]
        fig10 = go.Figure(go.Heatmap(
            z=pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
            colorscale=[[0,"#d1fae5"],[0.4,AMBER],[1,ROSE]],
            text=pivot.values.round(1), texttemplate="%{text}%",
            textfont=dict(color="#1e293b", size=11),
            hovertemplate="Dept: %{y}<br>%{x}<br>Attrition: %{z:.1f}%<extra></extra>",
            colorbar=dict(title="Att %", tickfont=dict(color=_FC), thickness=14),
        ))
        fig10.update_layout(
            paper_bgcolor=_PAPER, plot_bgcolor=_BG,
            font=dict(family="Manrope", color=_FC, size=12),
            margin=dict(t=36,b=40,l=160,r=20),
            height=330,
            xaxis=dict(title="", tickfont=dict(color=_FC), gridcolor=_GRID),
            yaxis=dict(title="", tickfont=dict(color=_FC), gridcolor=_GRID),
        )
        st.plotly_chart(fig10, use_container_width=True, config={"displayModeBar": False})

    # CHART 11 — High Risk Employees
    st.markdown("<div class='section-title'>🚨 High-Risk Employees (Low Satisfaction + High Hours)</div>", unsafe_allow_html=True)
    risk_df = df[(df["JobSatisfaction"]<=2) | (df["MonthlyHours"]>=95)].nlargest(25,"RiskScore")[
        ["EmployeeID","Age","Department","JobRole","JobSatisfaction","MonthlyHours","OverTime","YearsAtCompany","MonthlyIncome","RiskScore","Attrition"]
    ].copy()
    risk_df["Risk Level"] = risk_df["RiskScore"].apply(lambda r: "🔴 CRITICAL" if r>70 else ("🟡 HIGH" if r>45 else "🟢 WATCH"))
    risk_df["Income"] = risk_df["MonthlyIncome"].apply(lambda x: f"${x:,}")
    risk_df = risk_df.drop(columns=["MonthlyIncome"])
    risk_df.columns = ["ID","Age","Dept","Role","Satisfaction","Hours/Mo","OT","Tenure","Score","Left?","Risk","Income"]
    st.dataframe(risk_df.reset_index(drop=True), use_container_width=True, height=350)

# ══════════════════════════════════════════════
# TAB 4 — DEMOGRAPHICS
# ══════════════════════════════════════════════
with tab4:
    c9, c10 = st.columns(2, gap="medium")

    # CHART 12 — Age Pyramid
    with c9:
        st.markdown("<div class='section-title'>👥 Age Distribution by Gender</div>", unsafe_allow_html=True)
        age_bins = [18,25,30,35,40,45,50,55,65]
        age_labels = ["18-25","25-30","30-35","35-40","40-45","45-50","50-55","55+"]
        df["AgeBin"] = pd.cut(df["Age"], bins=age_bins, labels=age_labels, right=False)
        male_counts   = df[df["Gender"]=="Male"].groupby("AgeBin", observed=True).size().reset_index(name="count")
        female_counts = df[df["Gender"]=="Female"].groupby("AgeBin", observed=True).size().reset_index(name="count")
        fig12 = go.Figure()
        fig12.add_trace(go.Bar(y=male_counts["AgeBin"], x=-male_counts["count"],
                               orientation="h", name="Male",
                               marker=dict(color=STEEL, line=dict(color="white",width=1)),
                               hovertemplate="Male %{y}: %{x:.0f}<extra></extra>"))
        fig12.add_trace(go.Bar(y=female_counts["AgeBin"], x=female_counts["count"],
                               orientation="h", name="Female",
                               marker=dict(color=MINT, line=dict(color="white",width=1)),
                               hovertemplate="Female %{y}: %{x}<extra></extra>"))
        fig12.update_layout(**_L_no("xaxis",
            height=340, barmode="overlay",
            xaxis=dict(tickvals=[-120,-80,-40,0,40,80,120],
                       ticktext=["120","80","40","0","40","80","120"],
                       gridcolor=_GRID, linecolor=_GRID, tickfont=dict(color=_FC),zeroline=True,
                       zerolinecolor=_GRID, zerolinewidth=2),
            yaxis_title="Age Group",
        ))
        st.plotly_chart(fig12, use_container_width=True, config={"displayModeBar": False})

    # CHART 13 — Gender x Dept Heatmap
    with c10:
        st.markdown("<div class='section-title'>🔲 Gender Distribution by Department</div>", unsafe_allow_html=True)
        gd = df.groupby(["Department","Gender"]).size().reset_index(name="count")
        gd_pivot = gd.pivot(index="Department", columns="Gender", values="count").fillna(0)
        fig13 = go.Figure(go.Heatmap(
            z=gd_pivot.values, x=gd_pivot.columns.tolist(), y=gd_pivot.index.tolist(),
            colorscale=[[0,"#dbeafe"],[0.5,STEEL],[1,MINT]],
            text=gd_pivot.values.astype(int), texttemplate="%{text}",
            textfont=dict(color="#1e293b", size=12),
            hovertemplate="%{y} — %{x}: %{z}<extra></extra>",
            colorbar=dict(title="Count", tickfont=dict(color=_FC), thickness=14),
        ))
        fig13.update_layout(
            paper_bgcolor=_PAPER, plot_bgcolor=_BG,
            font=dict(family="Manrope", color=_FC, size=12),
            margin=dict(t=36,b=40,l=200,r=20),
            height=340,
            xaxis=dict(title="", tickfont=dict(color=_FC)),
            yaxis=dict(title="", tickfont=dict(color=_FC)),
        )
        st.plotly_chart(fig13, use_container_width=True, config={"displayModeBar": False})

    c11, c12 = st.columns(2, gap="medium")

    # CHART 14 — Education Field Spread
    with c11:
        st.markdown("<div class='section-title'>🎓 Education Field Distribution</div>", unsafe_allow_html=True)
        edu_dept = df.groupby(["EducationField","Department"]).size().reset_index(name="count")
        fig14 = px.bar(edu_dept, x="EducationField", y="count", color="Department",
                       barmode="stack",
                       color_discrete_map={"Sales":MINT,"Research & Development":STEEL,"Human Resources":AMBER})
        fig14.update_traces(marker_line_width=0)
        fig14.update_layout(**_L_no("xaxis", height=320, yaxis_title="Employees"),
                            xaxis=dict(title="", gridcolor=_GRID, linecolor=_GRID, tickfont=dict(color=_FC),
                                       zeroline=False, tickangle=-25))
        st.plotly_chart(fig14, use_container_width=True, config={"displayModeBar": False})

    # CHART 15 — Business Travel Attrition
    with c12:
        st.markdown("<div class='section-title'>✈️ Business Travel vs Attrition</div>", unsafe_allow_html=True)
        travel_attr = df.groupby(["BusinessTravel","Attrition"]).size().reset_index(name="count")
        fig15 = px.bar(travel_attr, x="BusinessTravel", y="count", color="Attrition",
                       barmode="group",
                       color_discrete_map={"Yes":ROSE,"No":MINT},
                       labels={"BusinessTravel":"Travel Frequency","count":"Employees"})
        fig15.update_traces(marker_line_width=0)
        fig15.update_layout(**_L(height=320, xaxis_title="", yaxis_title="Count"))
        st.plotly_chart(fig15, use_container_width=True, config={"displayModeBar": False})

# ─────────────────────────────────────────────
# FULL EMPLOYEE TABLE
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<div class='section-title'>👥 Live Employee Directory (Top 30 by Risk Score)</div>", unsafe_allow_html=True)

tbl = df.nlargest(30,"RiskScore")[
    ["EmployeeID","Age","Gender","Department","JobRole","YearsAtCompany",
     "JobSatisfaction","PerformanceRating","MonthlyIncome","OverTime","Attrition","RiskScore"]
].copy()
tbl["Risk Level"] = tbl["RiskScore"].apply(lambda r: "🔴 CRITICAL" if r>70 else ("🟡 HIGH" if r>45 else "🟢 WATCH"))
tbl["MonthlyIncome"] = tbl["MonthlyIncome"].apply(lambda x: f"${x:,}")
tbl["Perf"] = tbl["PerformanceRating"].map({3:"⭐ Excellent", 4:"⭐⭐ Outstanding"})
tbl = tbl.drop(columns=["PerformanceRating"])
tbl.columns = ["ID","Age","Gender","Dept","Job Role","Tenure","Satisfaction","Income","OT","Attrition","Score","Risk","Perf"]
st.dataframe(tbl.reset_index(drop=True), use_container_width=True, height=400)

# Risk summary row
m1,m2,m3,m4 = st.columns(4)
with m1: st.metric("🔴 Critical Risk", f"{(df['RiskScore']>70).sum():,}", "Immediate attention", delta_color="inverse")
with m2: st.metric("🟡 High Risk",     f"{((df['RiskScore']>45)&(df['RiskScore']<=70)).sum():,}", "Monitor closely", delta_color="off")
with m3: st.metric("🟢 Stable",        f"{(df['RiskScore']<=45).sum():,}", f"{(df['RiskScore']<=45).sum()/max(total,1)*100:.0f}% of workforce")
with m4: st.metric("✈️ Overtime Staff",f"{(df['OverTime']=='Yes').sum():,}", f"{ot_pct:.0f}% of workforce", delta_color="inverse")

# ─────────────────────────────────────────────
# ACTION BUTTONS
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<div class='section-title'>⚡ Quick Actions</div>", unsafe_allow_html=True)

a1, a2, a3 = st.columns(3, gap="medium")
with a1:
    if st.button("📊 Export HR Report (CSV)", use_container_width=True):
        csv = df.to_csv(index=False)
        st.download_button("⬇️ Download HR Data CSV", csv, "peopleflow_hr_export.csv", "text/csv", use_container_width=True)
with a2:
    if st.button("💎 Order Custom Dashboard — $25", use_container_width=True):
        st.info("🌐 Visit our website to place your order for a custom dashboard. https://ilyasarain943.github.io/ilyas-dashboard-portfolio/")
with a3:
    if st.button("➕ Upload Your Employee Data", use_container_width=True):
        st.info("📂 Replace the sample data with your own CSV file containing the same column structure.")

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class='footer-bar'>
  <div>
    <span class='footer-brand'>🌿 PeopleFlow Analytics</span>
    &nbsp;·&nbsp; Mint Arctic Edition &nbsp;·&nbsp; © 2026
  </div>
  <div style='font-size:12px; color:#94a3b8;'>
    IBM HR Workforce Intelligence Dashboard
  </div>
  <div style='font-size:12px; color:#94a3b8;'>
    Custom HR dashboards available — visit our website to order
  </div>
</div>
""", unsafe_allow_html=True)