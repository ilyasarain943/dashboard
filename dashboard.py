# ============================================================
#   SALES DASHBOARD — by Muhammed Ilyas Arain
#   Built with: Streamlit, Pandas, Plotly
#   GitHub: https://github.com/ilyasarain943
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# SECTION 1 — PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# SECTION 2 — GLOBAL THEME SETTINGS
# Change these to restyle everything at once
# ============================================================
CHART_BG   = "#1a1a2e"
PAPER_BG   = "#1a1a2e"
TEXT_COLOR = "#e0e0e0"
GRID_COLOR = "#2a2a4a"
ACCENT     = "#00d4ff"
RED_ACCENT = "#e94560"

# Plotly chart layout applied to every chart
# Edit this dict to change all charts at once
BASE_LAYOUT = dict(
    paper_bgcolor = PAPER_BG,
    plot_bgcolor  = CHART_BG,
    font          = dict(color=TEXT_COLOR, family="Poppins, sans-serif"),
    title_font    = dict(size=14, color=TEXT_COLOR),
    showlegend    = False,
    xaxis = dict(
        gridcolor    = GRID_COLOR,
        linecolor    = GRID_COLOR,
        tickfont     = dict(color=TEXT_COLOR),
        title_font   = dict(color="#8899bb"),
    ),
    yaxis = dict(
        gridcolor    = GRID_COLOR,
        linecolor    = GRID_COLOR,
        tickfont     = dict(color=TEXT_COLOR),
        title_font   = dict(color="#8899bb"),
    ),
    margin      = dict(l=40, r=40, t=50, b=40),
    hoverlabel  = dict(
        bgcolor   = "#0f3460",
        font_size = 13,
        font_color= TEXT_COLOR,
    ),
)

# ============================================================
# SECTION 3 — CUSTOM CSS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    color: #e0e0e0;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #0f3460 100%);
    border-right: 1px solid #00d4ff33;
}
[data-testid="stSidebar"] * { color: #e0e0e0 !important; }

.dashboard-header {
    background: linear-gradient(90deg, #00d4ff22, #e94560aa, #00d4ff22);
    border: 1px solid #00d4ff55;
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 24px;
    text-align: center;
    backdrop-filter: blur(10px);
}
.dashboard-header h1 {
    font-size: 2.6rem; font-weight: 700; color: #00d4ff;
    margin: 0 0 6px 0; letter-spacing: 2px;
    text-shadow: 0 0 20px #00d4ff88;
}
.dashboard-header p { font-size: 1rem; color: #a0c4ff; margin: 0; }

.kpi-card {
    background: linear-gradient(135deg, #1e1e3a, #2a2a4a);
    border: 1px solid #00d4ff44;
    border-radius: 14px;
    padding: 20px 16px;
    text-align: center;
    box-shadow: 0 4px 20px #00000055;
    transition: transform 0.2s, box-shadow 0.2s;
    margin-bottom: 8px;
}
.kpi-card:hover { transform: translateY(-4px); box-shadow: 0 8px 30px #00d4ff22; }
.kpi-icon  { font-size: 1.8rem; margin-bottom: 6px; }
.kpi-label { font-size: 0.72rem; color: #8899bb; letter-spacing: 1px; text-transform: uppercase; }
.kpi-value { font-size: 1.55rem; font-weight: 700; color: #00d4ff; margin-top: 4px; }
.kpi-value.red   { color: #e94560; }
.kpi-value.green { color: #00ff99; }
.kpi-value.gold  { color: #ffd700; }

.section-title {
    font-size: 1.1rem; font-weight: 600; color: #00d4ff;
    border-left: 4px solid #e94560;
    padding-left: 12px; margin: 24px 0 12px 0; letter-spacing: 0.5px;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px; background: #1a1a2e; border-radius: 10px; padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent; color: #8899bb; border-radius: 8px;
    padding: 8px 20px; font-weight: 600; font-size: 0.85rem; letter-spacing: 0.5px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, #00d4ff, #0099cc) !important;
    color: #0f0f1a !important;
}

.stButton > button {
    background: linear-gradient(90deg, #00d4ff, #0077aa) !important;
    color: #0f0f1a !important; border: none !important; border-radius: 10px !important;
    font-weight: 700 !important; padding: 10px 22px !important; font-size: 0.85rem !important;
    box-shadow: 0 0 14px #00d4ff44 !important; transition: all 0.2s !important; width: 100% !important;
}
.stButton > button:hover { box-shadow: 0 0 24px #00d4ff88 !important; transform: translateY(-2px) !important; }

[data-testid="stLinkButton"] a {
    background: linear-gradient(90deg, #e94560, #aa1133) !important;
    color: #ffffff !important; border: none !important; border-radius: 10px !important;
    font-weight: 700 !important; padding: 10px 22px !important; font-size: 0.85rem !important;
    box-shadow: 0 0 14px #e9456044 !important; text-decoration: none !important;
    display: block !important; text-align: center !important; transition: all 0.2s !important; width: 100% !important;
}
[data-testid="stLinkButton"] a:hover { box-shadow: 0 0 24px #e9456088 !important; transform: translateY(-2px) !important; }

[data-testid="stDownloadButton"] > button {
    background: linear-gradient(90deg, #00ff99, #00aa66) !important;
    color: #0f0f1a !important; border: none !important; border-radius: 10px !important;
    font-weight: 700 !important; padding: 10px 22px !important;
    box-shadow: 0 0 14px #00ff9944 !important; transition: all 0.2s !important; width: 100% !important;
}
[data-testid="stDownloadButton"] > button:hover { box-shadow: 0 0 24px #00ff9988 !important; transform: translateY(-2px) !important; }

[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #0f1a2e !important; border-color: #00d4ff44 !important; color: #e0e0e0 !important;
}
[data-testid="stSidebar"] input { background: #0f1a2e !important; color: #e0e0e0 !important; }
[data-baseweb="popover"] ul, [data-baseweb="menu"] {
    background: #1a1a2e !important; border: 1px solid #00d4ff33 !important;
}
[data-baseweb="option"]:hover { background: #00d4ff22 !important; }

.stAlert { background: #1e1e3a !important; border: 1px solid #00d4ff33 !important; border-radius: 10px !important; }

div[style*="max-height:420px"]::-webkit-scrollbar { width: 8px; height: 8px; }
div[style*="max-height:420px"]::-webkit-scrollbar-track { background: #0f0f1a; border-radius: 4px; }
div[style*="max-height:420px"]::-webkit-scrollbar-thumb { background: #00d4ff55; border-radius: 4px; }
div[style*="max-height:420px"]::-webkit-scrollbar-thumb:hover { background: #00d4ffaa; }

/* Plotly chart border */
.js-plotly-plot {
    border-radius: 12px;
    border: 1px solid #00d4ff22;
}

.footer {
    text-align: center; color: #445566; font-size: 0.78rem;
    margin-top: 40px; padding-top: 16px; border-top: 1px solid #00d4ff22;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# SECTION 4 — HELPER FUNCTIONS
# ============================================================

def apply_layout(fig, title=""):
    """
    Applies the dark theme BASE_LAYOUT to any Plotly figure.
    Always call this after creating a chart.
    """
    fig.update_layout(
        title=title,
        **BASE_LAYOUT
    )
    return fig


def kpi_card(icon, label, value, color_class=""):
    """Returns HTML for a single KPI card."""
    return f"""
    <div class='kpi-card'>
        <div class='kpi-icon'>{icon}</div>
        <div class='kpi-label'>{label}</div>
        <div class='kpi-value {color_class}'>{value}</div>
    </div>
    """


def empty_state_check(df, context="filters"):
    """Shows warning if dataframe is empty. Returns True if empty."""
    if df.empty:
        st.warning(f"⚠️ No data found for selected {context}. Try adjusting your filters.")
        return True
    return False


# ============================================================
# SECTION 5 — DATA LOADING
# ============================================================
@st.cache_data
def load_data(path):
    """Loads CSV with auto encoding detection."""
    try:
        df = pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="ISO-8859-1")
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df

data = load_data("sales_data.csv")


# ============================================================
# SECTION 6 — SESSION STATE
# ============================================================
if "show_filters" not in st.session_state:
    st.session_state.show_filters = False


# ============================================================
# SECTION 7 — SIDEBAR
# ============================================================
with st.sidebar:

    if st.button("🔧 Show/Hide Filters"):
        st.session_state.show_filters = not st.session_state.show_filters

    if st.session_state.show_filters:
        st.markdown("### 🎛️ Filters")

        search_query = st.text_input("🔍 Search Product", placeholder="e.g. Chair, Watch...")

        category_filter = st.multiselect(
            "📦 Category",
            options=data["Category"].unique(),
            default=data["Category"].unique()
        )
        region_filter = st.multiselect(
            "🌍 Region",
            options=data["Region"].unique(),
            default=data["Region"].unique()
        )
        customer_filter = st.multiselect(
            "👤 Customer Type",
            options=data["Customer Type"].unique(),
            default=data["Customer Type"].unique()
        )

        min_date = data["Date"].min().date()
        max_date = data["Date"].max().date()
        date_range = st.date_input(
            "📅 Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        filtered_data = data[
            data["Category"].isin(category_filter) &
            data["Region"].isin(region_filter) &
            data["Customer Type"].isin(customer_filter)
        ]

        if len(date_range) == 2:
            s = pd.Timestamp(date_range[0])
            e = pd.Timestamp(date_range[1])
            filtered_data = filtered_data[
                (filtered_data["Date"] >= s) & (filtered_data["Date"] <= e)
            ]

        if search_query:
            filtered_data = filtered_data[
                filtered_data["Product"].str.contains(search_query, case=False, na=False)
            ]
    else:
        filtered_data = data

    # ── Quick Summary ────────────────────────────────────────
    st.markdown("### 📊 Quick Summary")
    total_sales     = filtered_data["Sales"].sum()
    total_quantity  = filtered_data["Quantity"].sum()
    unique_products = filtered_data["Product"].nunique()
    avg_sale        = filtered_data["Sales"].mean() if not filtered_data.empty else 0

    st.markdown(f"""
    <div style='background:#1e1e3a;border:1px solid #00d4ff33;border-radius:10px;padding:14px;margin-bottom:8px;'>
        <div style='font-size:0.7rem;color:#8899bb;text-transform:uppercase;letter-spacing:1px;'>💰 Total Sales</div>
        <div style='font-size:1.3rem;font-weight:700;color:#00d4ff;'>${total_sales:,.2f}</div>
    </div>
    <div style='background:#1e1e3a;border:1px solid #00d4ff33;border-radius:10px;padding:14px;margin-bottom:8px;'>
        <div style='font-size:0.7rem;color:#8899bb;text-transform:uppercase;letter-spacing:1px;'>📦 Qty Sold</div>
        <div style='font-size:1.3rem;font-weight:700;color:#e94560;'>{total_quantity:,}</div>
    </div>
    <div style='background:#1e1e3a;border:1px solid #00d4ff33;border-radius:10px;padding:14px;margin-bottom:8px;'>
        <div style='font-size:0.7rem;color:#8899bb;text-transform:uppercase;letter-spacing:1px;'>🛍️ Unique Products</div>
        <div style='font-size:1.3rem;font-weight:700;color:#a0e0a0;'>{unique_products}</div>
    </div>
    <div style='background:#1e1e3a;border:1px solid #00d4ff33;border-radius:10px;padding:14px;'>
        <div style='font-size:0.7rem;color:#8899bb;text-transform:uppercase;letter-spacing:1px;'>📈 Avg Sale</div>
        <div style='font-size:1.3rem;font-weight:700;color:#ffd700;'>${avg_sale:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 👨‍💻 Developer")
    st.markdown("**🙋 Name:** Muhammed Ilyas Arain")
    st.markdown("**💼 Role:** Python Developer")
    st.markdown("**🏫 Experience:** 6-month internship at IBA University")
    st.markdown("**🛠️ Skills:** Python · Streamlit · Plotly · ML · Data Analysis")
    st.markdown("**📌 Project:** Interactive Sales Dashboard")
    st.link_button("🔗 GitHub Profile", "https://github.com/ilyasarain943")
    st.markdown("---")


# ============================================================
# SECTION 8 — MAIN HEADER
# ============================================================
st.markdown("""
<div class='dashboard-header'>
    <h1>📊 Sales Dashboard</h1>
    <p>Explore sales trends, top-performing products & regional insights</p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# SECTION 9 — KPI CARDS
# ============================================================
if not filtered_data.empty:
    k1, k2, k3, k4 = st.columns(4)
    best_product = filtered_data.groupby("Product")["Sales"].sum().idxmax()
    best_region  = filtered_data.groupby("Region")["Sales"].sum().idxmax()
    with k1:
        st.markdown(kpi_card("💰", "Total Sales",  f"${total_sales:,.0f}"),          unsafe_allow_html=True)
    with k2:
        st.markdown(kpi_card("📦", "Units Sold",   f"{total_quantity:,}",  "red"),   unsafe_allow_html=True)
    with k3:
        st.markdown(kpi_card("🏆", "Best Product", best_product,           "gold"),  unsafe_allow_html=True)
    with k4:
        st.markdown(kpi_card("🌍", "Top Region",   best_region,            "green"), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# SECTION 10 — TABS
# ============================================================
tab1, tab2, tab3 = st.tabs(["📦 Overview", "📈 Trends", "🗂️ Raw Data"])

# Plotly config — shows download button on hover, hides other buttons
# modeBarButtonsToRemove removes clutter, toImageButton stays visible
PLOTLY_CONFIG = {
    "displaylogo"             : False,
    "modeBarButtonsToRemove"  : [
        "zoom2d","pan2d","select2d","lasso2d",
        "zoomIn2d","zoomOut2d","autoScale2d","resetScale2d"
    ],
    # Download button always visible on hover — top right of chart
    "toImageButtonOptions": {
        "format" : "png",
        "scale"  : 2,        # high resolution download
        "width"  : 900,
        "height" : 500,
    }
}


# ════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ════════════════════════════════════════════════════════════
with tab1:

    if empty_state_check(filtered_data):
        st.stop()

    col1, col2 = st.columns(2)

    # ── Chart 1 — Sales by Region ────────────────────────────
    with col1:
        st.markdown("<div class='section-title'>🌍 Total Sales by Region</div>", unsafe_allow_html=True)
        region_sales = filtered_data.groupby("Region")["Sales"].sum().sort_values(ascending=False).reset_index()

        fig = px.bar(
            region_sales,
            x="Region", y="Sales",
            color="Region",                          # each region gets unique color
            color_discrete_sequence=px.colors.sequential.Blues_r,
            text="Sales",                            # value label on bar
            labels={"Sales": "Total Sales (USD)"},
        )
        fig.update_traces(
            texttemplate="$%{text:,.0f}",
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.2f}<extra></extra>"
        )
        fig = apply_layout(fig, "")
        # Set filename for download button
        PLOTLY_CONFIG["toImageButtonOptions"]["filename"] = "sales_by_region"
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)

    # ── Chart 2 — Top 5 Products ─────────────────────────────
    with col2:
        st.markdown("<div class='section-title'>🏆 Top 5 Products by Sales</div>", unsafe_allow_html=True)
        top_products = filtered_data.groupby("Product")["Sales"].sum().sort_values(ascending=False).head(5).reset_index()

        fig = px.bar(
            top_products,
            x="Sales", y="Product",
            orientation="h",                         # horizontal bar
            color="Product",
            color_discrete_sequence=px.colors.sequential.Oranges_r,
            text="Sales",
            labels={"Sales": "Total Sales (USD)"},
        )
        fig.update_traces(
            texttemplate="$%{x:,.0f}",
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Sales: $%{x:,.2f}<extra></extra>"
        )
        fig = apply_layout(fig, " ")
        PLOTLY_CONFIG["toImageButtonOptions"]["filename"] = "top_5_products"
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)

    col3, col4 = st.columns(2)

    # ── Chart 3 — Sales by Category (Donut) ──────────────────
    with col3:
        st.markdown("<div class='section-title'>🗂️ Sales by Category</div>", unsafe_allow_html=True)
        cat_sales = filtered_data.groupby("Category")["Sales"].sum().reset_index()

        fig = px.pie(
            cat_sales,
            names="Category", values="Sales",
            hole=0.5,                                # donut style
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>Sales: $%{value:,.2f}<br>%{percent}<extra></extra>",
            marker=dict(line=dict(color=CHART_BG, width=2))
        )
        fig = apply_layout(fig, "")
        PLOTLY_CONFIG["toImageButtonOptions"]["filename"] = "sales_by_category"
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)

    # ── Chart 4 — Sales by Customer Type ─────────────────────
    with col4:
        st.markdown("<div class='section-title'>👤 Sales by Customer Type</div>", unsafe_allow_html=True)
        cust_sales = filtered_data.groupby("Customer Type")["Sales"].sum().sort_values(ascending=False).reset_index()

        fig = px.bar(
            cust_sales,
            x="Customer Type", y="Sales",
            color="Customer Type",
            color_discrete_sequence=["#00d4ff", "#e94560", "#00ff99", "#ffd700"],
            text="Sales",
            labels={"Sales": "Total Sales (USD)"},
        )
        fig.update_traces(
            texttemplate="$%{text:,.0f}",
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.2f}<extra></extra>"
        )
        fig = apply_layout(fig, " ")
        PLOTLY_CONFIG["toImageButtonOptions"]["filename"] = "sales_by_customer"
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)


# ════════════════════════════════════════════════════════════
# TAB 2 — TRENDS
# ════════════════════════════════════════════════════════════
with tab2:

    if empty_state_check(filtered_data):
        st.stop()

    # ── Chart 5 — Daily Sales Trend ──────────────────────────
    st.markdown("<div class='section-title'>📅 Daily Sales Trend</div>", unsafe_allow_html=True)
    sales_trend = filtered_data.groupby("Date")["Sales"].sum().reset_index()

    fig = px.area(
        sales_trend,
        x="Date", y="Sales",
        labels={"Sales": "Total Sales (USD)"},
        color_discrete_sequence=[ACCENT],
    )
    fig.update_traces(
        line=dict(width=2, color=ACCENT),
        fillcolor="rgba(0,212,255,0.15)",
        hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.2f}<extra></extra>"
    )
    fig = apply_layout(fig, " ")
    PLOTLY_CONFIG["toImageButtonOptions"]["filename"] = "daily_sales_trend"
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)

    # ── Chart 6 — Sales by Weekday ───────────────────────────
    st.markdown("<div class='section-title'>📅 Sales by Day of Week</div>", unsafe_allow_html=True)
    weekday             = filtered_data.copy()
    weekday["Weekday"]  = weekday["Date"].dt.day_name()
    day_order           = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    weekday_sales       = weekday.groupby("Weekday")["Sales"].sum().reindex(day_order).fillna(0).reset_index()

    # Highlight best day in cyan, others in steel blue
    max_day = weekday_sales.loc[weekday_sales["Sales"].idxmax(), "Weekday"]
    weekday_sales["Color"] = weekday_sales["Weekday"].apply(
        lambda d: ACCENT if d == max_day else "#2a5298"
    )

    fig = go.Figure(go.Bar(
        x=weekday_sales["Weekday"],
        y=weekday_sales["Sales"],
        marker_color=weekday_sales["Color"],
        marker_line_color=CHART_BG,
        marker_line_width=1.5,
        text=weekday_sales["Sales"],
        texttemplate="$%{text:,.0f}",
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.2f}<extra></extra>",
        name="Sales"
    ))
    fig = apply_layout(fig, "Sales by Day of Week")
    fig.update_layout(
        xaxis_title="Day of Week",
        yaxis_title="Total Sales (USD)",
        showlegend=False,
        # Add annotation for best day
        annotations=[dict(
            x=max_day, y=weekday_sales[weekday_sales["Weekday"]==max_day]["Sales"].values[0],
            text=f"⭐ Best Day",
            showarrow=True, arrowhead=2,
            arrowcolor=ACCENT, font=dict(color=ACCENT, size=11),
            ay=-40
        )]
    )
    PLOTLY_CONFIG["toImageButtonOptions"]["filename"] = "weekday_sales"
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)


# ════════════════════════════════════════════════════════════
# TAB 3 — RAW DATA
# ════════════════════════════════════════════════════════════
with tab3:

    st.markdown("<div class='section-title'>🗂️ Filtered Data Table</div>", unsafe_allow_html=True)
    st.markdown(f"Showing **{len(filtered_data):,}** of **{len(data):,}** rows · Use sidebar filters to narrow down.")

    if empty_state_check(filtered_data):
        st.stop()

    styled_df = filtered_data.style\
        .format({"Sales": "${:,.2f}"})\
        .set_properties(**{
            'background-color': '#1a1a2e',
            'color': '#e0e0e0',
            'border-color': '#2a2a4a',
            'font-size': '13px',
        })\
        .set_table_styles([
            {'selector': 'thead th', 'props': [
                ('background-color', '#0f3460'), ('color', '#00d4ff'),
                ('font-weight', '700'), ('border-bottom', '2px solid #00d4ff44'),
                ('padding', '10px 14px'), ('font-size', '12px'),
                ('letter-spacing', '0.5px'), ('text-transform', 'uppercase'),
            ]},
            {'selector': 'tbody tr:nth-child(even)', 'props': [('background-color', '#16213e')]},
            {'selector': 'tbody tr:nth-child(odd)',  'props': [('background-color', '#1a1a2e')]},
            {'selector': 'tbody tr:hover',           'props': [('background-color', '#00d4ff15')]},
            {'selector': 'td', 'props': [
                ('border-bottom', '1px solid #2a2a4a'),
                ('padding', '8px 14px'), ('color', '#e0e0e0'),
            ]},
        ])\
        .highlight_max(subset=["Sales"], color="#00d4ff33")\
        .highlight_min(subset=["Sales"], color="#e9456022")

    st.markdown(
        '<div style="overflow-x:auto;overflow-y:auto;max-height:420px;border:1px solid #00d4ff22;border-radius:12px;padding:4px;">'
        + styled_df.to_html()
        + '</div>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    csv = filtered_data.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Filtered CSV",
        data=csv,
        file_name="filtered_sales_data.csv",
        mime="text/csv"
    )


# ============================================================
# SECTION 11 — FOOTER
# ============================================================
st.markdown("""
<div class='footer'>
    ✨ Built with Streamlit · Plotly · Pandas &nbsp;|&nbsp;
    Developer: <strong>Muhammed Ilyas Arain</strong> &nbsp;|&nbsp;
    IBA University Intern &nbsp;|&nbsp;
    <a href='https://github.com/ilyasarain943' style='color:#00d4ff;text-decoration:none;'>GitHub 🔗</a>
</div>
""", unsafe_allow_html=True) 
