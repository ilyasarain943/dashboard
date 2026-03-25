import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Import Google Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* ── Main background ── */
.stApp {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    color: #e0e0e0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #0f3460 100%);
    border-right: 1px solid #00d4ff33;
}
[data-testid="stSidebar"] * {
    color: #e0e0e0 !important;
}

/* ── Header banner ── */
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
    font-size: 2.6rem;
    font-weight: 700;
    color: #00d4ff;
    margin: 0 0 6px 0;
    letter-spacing: 2px;
    text-shadow: 0 0 20px #00d4ff88;
}
.dashboard-header p {
    font-size: 1rem;
    color: #a0c4ff;
    margin: 0;
}

/* ── Metric cards ── */
.metric-row {
    display: flex;
    gap: 16px;
    margin-bottom: 28px;
}
.metric-card {
    flex: 1;
    background: linear-gradient(135deg, #1e1e3a, #2a2a4a);
    border: 1px solid #00d4ff44;
    border-radius: 14px;
    padding: 20px 24px;
    text-align: center;
    box-shadow: 0 4px 20px #00000055;
    transition: transform 0.2s;
}
.metric-card:hover { transform: translateY(-3px); }
.metric-icon { font-size: 2rem; margin-bottom: 8px; }
.metric-label { font-size: 0.78rem; color: #8899bb; letter-spacing: 1px; text-transform: uppercase; }
.metric-value { font-size: 1.7rem; font-weight: 700; color: #00d4ff; }

/* ── Chart containers ── */
.chart-card {
    background: #1a1a2e;
    border: 1px solid #00d4ff22;
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 20px;
}

/* ── Section title ── */
.section-title {
    font-size: 1.15rem;
    font-weight: 600;
    color: #00d4ff;
    border-left: 4px solid #e94560;
    padding-left: 12px;
    margin: 28px 0 14px 0;
    letter-spacing: 0.5px;
}

/* ── Tab styling ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: #1a1a2e;
    border-radius: 10px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #8899bb;
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 600;
    font-size: 0.85rem;
    letter-spacing: 0.5px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, #00d4ff, #0099cc) !important;
    color: #0f0f1a !important;
}

/* ── Dataframe dark theme ── */
[data-testid="stDataFrame"] {
    border: 1px solid #00d4ff33;
    border-radius: 10px;
    overflow: hidden;
}
[data-testid="stDataFrame"] iframe {
    border-radius: 10px;
}
/* Target the inner dataframe table */
.dvn-scroller, .glideDataEditor, [class*="wzrd"] {
    background-color: #1a1a2e !important;
    color: #e0e0e0 !important;
}
/* Streamlit dataframe wrapper */
div[data-testid="stDataFrame"] > div {
    background: #1a1a2e !important;
    border-radius: 10px;
}
/* Force all dataframe elements dark */
.stDataFrame {
    background: #1a1a2e !important;
}


/* ── All Buttons ── */
.stButton > button {
    background: linear-gradient(90deg, #00d4ff, #0077aa) !important;
    color: #0f0f1a !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    padding: 10px 22px !important;
    font-size: 0.85rem !important;
    box-shadow: 0 0 14px #00d4ff44 !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover {
    box-shadow: 0 0 24px #00d4ff88 !important;
    transform: translateY(-2px) !important;
}

/* ── Link button (GitHub) ── */
[data-testid="stLinkButton"] a {
    background: linear-gradient(90deg, #e94560, #aa1133) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    padding: 10px 22px !important;
    font-size: 0.85rem !important;
    box-shadow: 0 0 14px #e9456044 !important;
    text-decoration: none !important;
    display: block !important;
    text-align: center !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
[data-testid="stLinkButton"] a:hover {
    box-shadow: 0 0 24px #e9456088 !important;
    transform: translateY(-2px) !important;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background: linear-gradient(90deg, #00ff99, #00aa66) !important;
    color: #0f0f1a !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    padding: 10px 22px !important;
    box-shadow: 0 0 14px #00ff9944 !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
[data-testid="stDownloadButton"] > button:hover {
    box-shadow: 0 0 24px #00ff9988 !important;
    transform: translateY(-2px) !important;
}

/* ── Filter multiselect dark background ── */
[data-testid="stSidebar"] .stMultiSelect > div > div {
    background: #0f1a2e !important;
    border: 1px solid #00d4ff44 !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #0f1a2e !important;
    border-color: #00d4ff44 !important;
    color: #e0e0e0 !important;
}
[data-testid="stSidebar"] input {
    background: #0f1a2e !important;
    color: #e0e0e0 !important;
}
[data-baseweb="popover"] ul, [data-baseweb="menu"] {
    background: #1a1a2e !important;
    border: 1px solid #00d4ff33 !important;
}
[data-baseweb="option"]:hover {
    background: #00d4ff22 !important;
}

/* ── Footer ── */
.footer {
    text-align: center;
    color: #445566;
    font-size: 0.78rem;
    margin-top: 40px;
    padding-top: 16px;
    border-top: 1px solid #00d4ff22;
}
</style>
""", unsafe_allow_html=True)

# ── Helpers ──────────────────────────────────────────────────────────────────
CHART_BG   = "#1a1a2e"
TEXT_COLOR = "#e0e0e0"
GRID_COLOR = "#2a2a4a"

def style_ax(ax, title="", xlabel="", ylabel=""):
    ax.set_facecolor(CHART_BG)
    ax.figure.patch.set_facecolor(CHART_BG)
    ax.set_title(title, fontsize=13, fontweight="bold", color=TEXT_COLOR, pad=12)
    ax.set_xlabel(xlabel, fontsize=10, color="#8899bb")
    ax.set_ylabel(ylabel, fontsize=10, color="#8899bb")
    ax.tick_params(colors=TEXT_COLOR, labelsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID_COLOR)
    ax.yaxis.grid(True, color=GRID_COLOR, linewidth=0.6, linestyle="--")
    ax.set_axisbelow(True)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(path):
    try:
        return pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="ISO-8859-1")

data = load_data("sales_data.csv")

# ── Session state ─────────────────────────────────────────────────────────────
if "show_filters" not in st.session_state:
    st.session_state.show_filters = False

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 👨‍💻 Developer")
    st.markdown("---")
    st.markdown("**🙋 Name:** Muhammed Ilyas Arain")
    st.markdown("**💼 Role:** Developer")
    st.markdown("**🏫 Experience:** 6-month internship at IBA University")
    st.markdown("**🛠️ Skills:** Python · Streamlit · ML · Data Analysis")
    st.markdown("**📌 Project:** Interactive Sales Dashboard")
    st.markdown("---")
    st.link_button("🔗 GitHub Profile", "https://github.com/ilyasarain943")
    st.markdown("---")

    # ── Filter toggle ──
    if st.button("🔧 Show/Hide Filters"):
        st.session_state.show_filters = not st.session_state.show_filters

    if st.session_state.show_filters:
        st.markdown("### 🎛️ Filters")
        category_filter = st.multiselect("Category", options=data["Category"].unique(), default=data["Category"].unique())
        region_filter   = st.multiselect("Region",   options=data["Region"].unique(),   default=data["Region"].unique())
        customer_filter = st.multiselect("Customer Type", options=data["Customer Type"].unique(), default=data["Customer Type"].unique())
        filtered_data = data[
            data["Category"].isin(category_filter) &
            data["Region"].isin(region_filter) &
            data["Customer Type"].isin(customer_filter)
        ]
    else:
        filtered_data = data

    # ── Quick summary metrics ──
    st.markdown("---")
    st.markdown("### 📊 Quick Summary")
    total_sales    = filtered_data["Sales"].sum()
    total_quantity = filtered_data["Quantity"].sum()
    unique_products = filtered_data["Product"].nunique()

    st.markdown(f"""
    <div style='background:#1e1e3a;border:1px solid #00d4ff33;border-radius:10px;padding:14px;margin-bottom:8px;'>
        <div style='font-size:0.7rem;color:#8899bb;text-transform:uppercase;letter-spacing:1px;'>💰 Total Sales</div>
        <div style='font-size:1.4rem;font-weight:700;color:#00d4ff;'>${total_sales:,.2f}</div>
    </div>
    <div style='background:#1e1e3a;border:1px solid #00d4ff33;border-radius:10px;padding:14px;margin-bottom:8px;'>
        <div style='font-size:0.7rem;color:#8899bb;text-transform:uppercase;letter-spacing:1px;'>📦 Qty Sold</div>
        <div style='font-size:1.4rem;font-weight:700;color:#e94560;'>{total_quantity:,}</div>
    </div>
    <div style='background:#1e1e3a;border:1px solid #00d4ff33;border-radius:10px;padding:14px;'>
        <div style='font-size:0.7rem;color:#8899bb;text-transform:uppercase;letter-spacing:1px;'>🛍️ Unique Products</div>
        <div style='font-size:1.4rem;font-weight:700;color:#a0e0a0;'>{unique_products}</div>
    </div>
    """, unsafe_allow_html=True)

# ── MAIN AREA ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class='dashboard-header'>
    <h1>📊 Sales Dashboard</h1>
    <p>Explore sales trends, top-performing products & regional insights</p>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📦 Overview", "📈 Trends", "🗂️ Raw Data"])

# ════════════════════════════════════════════════════
# TAB 1 — Overview  (2 charts per row)
# ════════════════════════════════════════════════════
with tab1:
    # ROW 1: Region sales  |  Top 5 Products
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-title'>🌍 Total Sales by Region</div>", unsafe_allow_html=True)
        region_sales = filtered_data.groupby("Region")["Sales"].sum().sort_values(ascending=False)
        palette_blues = sns.color_palette("Blues_d", len(region_sales))

        fig, ax = plt.subplots(figsize=(6, 4))
        bars = sns.barplot(x=region_sales.index, y=region_sales.values, palette=palette_blues, ax=ax)
        style_ax(ax, title="Sales by Region", xlabel="Region", ylabel="Total Sales (USD)")
        for container in ax.containers:
            ax.bar_label(container, fmt="%.0f", fontsize=8, color=TEXT_COLOR, label_type="edge", padding=2)
        # Legend
        legend_patches = [mpatches.Patch(color=palette_blues[i], label=r) for i, r in enumerate(region_sales.index)]
        ax.legend(handles=legend_patches, title="Region", title_fontsize=8,
                  fontsize=7, loc="upper right",
                  facecolor=CHART_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with col2:
        st.markdown("<div class='section-title'>🏆 Top 5 Products by Sales</div>", unsafe_allow_html=True)
        top_products = filtered_data.groupby("Product")["Sales"].sum().sort_values(ascending=False).head(5)
        palette_orange = sns.color_palette("Oranges_r", len(top_products))

        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x=top_products.values, y=top_products.index, palette=palette_orange, ax=ax)
        style_ax(ax, title="Top 5 Products", xlabel="Total Sales (USD)", ylabel="Product")
        for container in ax.containers:
            ax.bar_label(container, fmt="%.0f", fontsize=8, color=TEXT_COLOR, label_type="edge", padding=2)
        legend_patches = [mpatches.Patch(color=palette_orange[i], label=p) for i, p in enumerate(top_products.index)]
        ax.legend(handles=legend_patches, title="Product", title_fontsize=8,
                  fontsize=7, loc="lower right",
                  facecolor=CHART_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # ROW 2: Category pie  |  Customer type bar
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("<div class='section-title'>🗂️ Sales by Category</div>", unsafe_allow_html=True)
        cat_sales = filtered_data.groupby("Category")["Sales"].sum()
        palette_cat = sns.color_palette("Set2", len(cat_sales))

        fig, ax = plt.subplots(figsize=(6, 4))
        wedges, texts, autotexts = ax.pie(
            cat_sales.values, labels=None, autopct="%1.1f%%",
            colors=palette_cat, startangle=140,
            pctdistance=0.75, wedgeprops=dict(width=0.6, edgecolor=CHART_BG, linewidth=2)
        )
        for at in autotexts:
            at.set_color(TEXT_COLOR); at.set_fontsize(8)
        ax.set_title("Sales by Category", fontsize=13, fontweight="bold", color=TEXT_COLOR, pad=12)
        ax.figure.patch.set_facecolor(CHART_BG)
        legend_patches = [mpatches.Patch(color=palette_cat[i], label=c) for i, c in enumerate(cat_sales.index)]
        ax.legend(handles=legend_patches, title="Category", title_fontsize=8,
                  fontsize=7, loc="lower left",
                  facecolor=CHART_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with col4:
        st.markdown("<div class='section-title'>👤 Sales by Customer Type</div>", unsafe_allow_html=True)
        cust_sales = filtered_data.groupby("Customer Type")["Sales"].sum().sort_values(ascending=False)
        palette_cust = sns.color_palette("cool", len(cust_sales))

        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x=cust_sales.index, y=cust_sales.values, palette=palette_cust, ax=ax)
        style_ax(ax, title="Sales by Customer Type", xlabel="Customer Type", ylabel="Total Sales (USD)")
        for container in ax.containers:
            ax.bar_label(container, fmt="%.0f", fontsize=8, color=TEXT_COLOR, label_type="edge", padding=2)
        legend_patches = [mpatches.Patch(color=palette_cust[i], label=c) for i, c in enumerate(cust_sales.index)]
        ax.legend(handles=legend_patches, title="Customer", title_fontsize=8,
                  fontsize=7, loc="upper right",
                  facecolor=CHART_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

# ════════════════════════════════════════════════════
# TAB 2 — Trends
# ════════════════════════════════════════════════════
with tab2:
    st.markdown("<div class='section-title'>📅 Sales Trend Over Time</div>", unsafe_allow_html=True)
    sales_trend = filtered_data.groupby("Date")["Sales"].sum()
    sales_trend.index = pd.to_datetime(sales_trend.index, errors="coerce")
    sales_trend = sales_trend.sort_index()

    fig, ax = plt.subplots(figsize=(12, 4.5))
    ax.fill_between(sales_trend.index, sales_trend.values, alpha=0.18, color="#00d4ff")
    sns.lineplot(x=sales_trend.index, y=sales_trend.values, marker="o",
                 color="#00d4ff", linewidth=2, markersize=5, ax=ax)
    style_ax(ax, title="Sales Trend Over Time", xlabel="Date", ylabel="Total Sales (USD)")
    plt.xticks(rotation=45)
    # Legend
    line_patch = mpatches.Patch(color="#00d4ff", label="Daily Sales")
    ax.legend(handles=[line_patch], title="Metric", title_fontsize=8,
              fontsize=8, loc="upper left",
              facecolor=CHART_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    # Monthly sales bar
    st.markdown("<div class='section-title'>📆 Monthly Sales Summary</div>", unsafe_allow_html=True)
    monthly = filtered_data.copy()
    monthly["Date"] = pd.to_datetime(monthly["Date"], errors="coerce")
    monthly["Month"] = monthly["Date"].dt.to_period("M").astype(str)
    monthly_sales = monthly.groupby("Month")["Sales"].sum()
    palette_monthly = sns.color_palette("viridis", len(monthly_sales))

    fig, ax = plt.subplots(figsize=(12, 4))
    sns.barplot(x=monthly_sales.index, y=monthly_sales.values, palette=palette_monthly, ax=ax)
    style_ax(ax, title="Monthly Sales", xlabel="Month", ylabel="Total Sales (USD)")
    plt.xticks(rotation=45)
    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f", fontsize=7, color=TEXT_COLOR, label_type="edge", padding=2)
    legend_patches = [mpatches.Patch(color=palette_monthly[i], label=m) for i, m in enumerate(monthly_sales.index)]
    ax.legend(handles=legend_patches, title="Month", title_fontsize=7,
              fontsize=6, loc="upper right", ncol=2,
              facecolor=CHART_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# ════════════════════════════════════════════════════
# TAB 3 — Raw Data
# ════════════════════════════════════════════════════
with tab3:
    st.markdown("<div class='section-title'>🗂️ Filtered Data Table</div>", unsafe_allow_html=True)
    st.markdown(f"Showing **{len(filtered_data):,}** rows · Use sidebar filters to narrow down.")

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
                ('background-color', '#0f3460'),
                ('color', '#00d4ff'),
                ('font-weight', '700'),
                ('border-bottom', '2px solid #00d4ff44'),
                ('padding', '10px 14px'),
                ('font-size', '12px'),
                ('letter-spacing', '0.5px'),
                ('text-transform', 'uppercase'),
            ]},
            {'selector': 'tbody tr:nth-child(even)', 'props': [
                ('background-color', '#16213e'),
            ]},
            {'selector': 'tbody tr:nth-child(odd)', 'props': [
                ('background-color', '#1a1a2e'),
            ]},
            {'selector': 'tbody tr:hover', 'props': [
                ('background-color', '#00d4ff15'),
            ]},
            {'selector': 'td', 'props': [
                ('border-bottom', '1px solid #2a2a4a'),
                ('padding', '8px 14px'),
                ('color', '#e0e0e0'),
            ]},
        ])\
        .highlight_max(subset=["Sales"], color="#00d4ff33")\
        .highlight_min(subset=["Sales"], color="#e9456022")

    st.markdown(
        '<div style="overflow-x:auto;border:1px solid #00d4ff22;border-radius:12px;padding:4px;">'
        + styled_df.to_html()
        + '</div>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    csv = filtered_data.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download CSV", csv, "filtered_sales.csv", "text/csv")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='footer'>
    ✨ Built with Streamlit · Matplotlib · Seaborn &nbsp;|&nbsp; 
    Developer: <strong>Muhammed Ilyas Arain</strong> &nbsp;|&nbsp; IBA University Intern
</div>
""", unsafe_allow_html=True)