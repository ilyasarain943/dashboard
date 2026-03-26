# ============================================================
#   SALES DASHBOARD — by Muhammed Ilyas Arain
#   Built with: Streamlit, Pandas, Matplotlib, Seaborn
#   GitHub: https://github.com/ilyasarain943
# ============================================================

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import io  # ← needed for chart download buttons

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
# SECTION 2 — GLOBAL CHART SETTINGS
# ============================================================
CHART_BG   = "#1a1a2e"
TEXT_COLOR = "#e0e0e0"
GRID_COLOR = "#2a2a4a"
ACCENT     = "#00d4ff"
RED_ACCENT = "#e94560"

plt.rcParams["font.family"] = "DejaVu Sans"

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

[data-testid="stDataFrame"] { border: 1px solid #00d4ff33; border-radius: 10px; overflow: hidden; }
div[data-testid="stDataFrame"] > div { background: #1a1a2e !important; border-radius: 10px; }
.dvn-scroller, .glideDataEditor { background-color: #1a1a2e !important; color: #e0e0e0 !important; }

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

[data-testid="stImage"], .stPlotlyChart, canvas {
    cursor: crosshair !important;
    transition: opacity 0.2s;
}
[data-testid="stImage"]:hover { opacity: 0.92; filter: brightness(1.06); }

.stAlert { background: #1e1e3a !important; border: 1px solid #00d4ff33 !important; border-radius: 10px !important; }

div[style*="max-height:420px"]::-webkit-scrollbar { width: 8px; height: 8px; }
div[style*="max-height:420px"]::-webkit-scrollbar-track { background: #0f0f1a; border-radius: 4px; }
div[style*="max-height:420px"]::-webkit-scrollbar-thumb { background: #00d4ff55; border-radius: 4px; }
div[style*="max-height:420px"]::-webkit-scrollbar-thumb:hover { background: #00d4ffaa; }

.footer {
    text-align: center; color: #445566; font-size: 0.78rem;
    margin-top: 40px; padding-top: 16px; border-top: 1px solid #00d4ff22;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# SECTION 4 — HELPER FUNCTIONS
# ============================================================

def style_ax(ax, title="", xlabel="", ylabel=""):
    """Applies dark theme to any matplotlib chart."""
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


def chart_download_btn(fig, filename, key):
    """
    Renders a download button for any matplotlib figure.
    Parameters:
        fig      — the matplotlib figure to save
        filename — name of downloaded file e.g. "chart.png"
        key      — unique key string for this button
    """
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight", facecolor=CHART_BG)
    buf.seek(0)
    st.download_button(
        label="⬇️ Download Chart",
        data=buf,
        file_name=filename,
        mime="image/png",
        key=key
    )


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
    st.markdown("**🛠️ Skills:** Python · Streamlit · ML · Data Analysis")
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
# SECTION 9 — KPI CARDS ROW
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
        region_sales  = filtered_data.groupby("Region")["Sales"].sum().sort_values(ascending=False)
        palette_blues = sns.color_palette("Blues_d", len(region_sales))

        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x=region_sales.index, y=region_sales.values, palette=palette_blues, ax=ax)
        style_ax(ax, title="Sales by Region", xlabel="Region", ylabel="Total Sales (USD)")
        for container in ax.containers:
            ax.bar_label(container, fmt="%.0f", fontsize=8, color=TEXT_COLOR, label_type="edge", padding=2)
        patches = [mpatches.Patch(color=palette_blues[i], label=r) for i, r in enumerate(region_sales.index)]
        ax.legend(handles=patches, title="Region", title_fontsize=8, fontsize=7, loc="upper right",
                  facecolor=CHART_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
        plt.tight_layout()
        st.pyplot(fig)
        chart_download_btn(fig, "sales_by_region.png", "chart_region")  # ← download button
        plt.close(fig)

    # ── Chart 2 — Top 5 Products ─────────────────────────────
    with col2:
        st.markdown("<div class='section-title'>🏆 Top 5 Products by Sales</div>", unsafe_allow_html=True)
        top_products   = filtered_data.groupby("Product")["Sales"].sum().sort_values(ascending=False).head(5)
        palette_orange = sns.color_palette("Oranges_r", len(top_products))

        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x=top_products.values, y=top_products.index, palette=palette_orange, ax=ax)
        style_ax(ax, title="Top 5 Products", xlabel="Total Sales (USD)", ylabel="Product")
        for container in ax.containers:
            ax.bar_label(container, fmt="%.0f", fontsize=8, color=TEXT_COLOR, label_type="edge", padding=2)
        patches = [mpatches.Patch(color=palette_orange[i], label=p) for i, p in enumerate(top_products.index)]
        ax.legend(handles=patches, title="Product", title_fontsize=8, fontsize=7, loc="lower right",
                  facecolor=CHART_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
        plt.tight_layout()
        st.pyplot(fig)
        chart_download_btn(fig, "top_products.png", "chart_products")  # ← download button
        plt.close(fig)

    col3, col4 = st.columns(2)

    # ── Chart 3 — Sales by Category (Donut) ──────────────────
    with col3:
        st.markdown("<div class='section-title'>🗂️ Sales by Category</div>", unsafe_allow_html=True)
        cat_sales   = filtered_data.groupby("Category")["Sales"].sum()
        palette_cat = sns.color_palette("Set2", len(cat_sales))

        fig, ax = plt.subplots(figsize=(6, 4))
        wedges, texts, autotexts = ax.pie(
            cat_sales.values, labels=None, autopct="%1.1f%%",
            colors=palette_cat, startangle=140, pctdistance=0.75,
            wedgeprops=dict(width=0.6, edgecolor=CHART_BG, linewidth=2)
        )
        for at in autotexts:
            at.set_color(TEXT_COLOR); at.set_fontsize(8)
        ax.set_title("Sales by Category", fontsize=13, fontweight="bold", color=TEXT_COLOR, pad=12)
        ax.figure.patch.set_facecolor(CHART_BG)
        patches = [mpatches.Patch(color=palette_cat[i], label=c) for i, c in enumerate(cat_sales.index)]
        ax.legend(handles=patches, title="Category", title_fontsize=8, fontsize=7, loc="lower left",
                  facecolor=CHART_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
        plt.tight_layout()
        st.pyplot(fig)
        chart_download_btn(fig, "sales_by_category.png", "chart_category")  # ← download button
        plt.close(fig)

    # ── Chart 4 — Sales by Customer Type ─────────────────────
    with col4:
        st.markdown("<div class='section-title'>👤 Sales by Customer Type</div>", unsafe_allow_html=True)
        cust_sales   = filtered_data.groupby("Customer Type")["Sales"].sum().sort_values(ascending=False)
        palette_cust = sns.color_palette("cool", len(cust_sales))

        fig, ax = plt.subplots(figsize=(5.5, 6))
        sns.barplot(x=cust_sales.index, y=cust_sales.values, palette=palette_cust, ax=ax)
        style_ax(ax, title="Sales by Customer Type", xlabel="Customer Type", ylabel="Total Sales (USD)")
        for container in ax.containers:
            ax.bar_label(container, fmt="%.0f", fontsize=8, color=TEXT_COLOR, label_type="edge", padding=2)
        patches = [mpatches.Patch(color=palette_cust[i], label=c) for i, c in enumerate(cust_sales.index)]
        ax.legend(handles=patches, title="Customer", title_fontsize=8, fontsize=7, loc="upper right",
                  facecolor=CHART_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
        plt.tight_layout()
        st.pyplot(fig)
        chart_download_btn(fig, "sales_by_customer.png", "chart_customer")  # ← download button
        plt.close(fig)


# ════════════════════════════════════════════════════════════
# TAB 2 — TRENDS
# ════════════════════════════════════════════════════════════
with tab2:

    if empty_state_check(filtered_data):
        st.stop()

    # ── Chart 5 — Daily Sales Trend ──────────────────────────
    st.markdown("<div class='section-title'>📅 Daily Sales Trend</div>", unsafe_allow_html=True)
    sales_trend = filtered_data.groupby("Date")["Sales"].sum().sort_index()

    fig, ax = plt.subplots(figsize=(12, 4.5))
    ax.fill_between(sales_trend.index, sales_trend.values, alpha=0.18, color=ACCENT)
    sns.lineplot(x=sales_trend.index, y=sales_trend.values,
                 marker="o", color=ACCENT, linewidth=2, markersize=5, ax=ax)
    style_ax(ax, title="Daily Sales Trend", xlabel="Date", ylabel="Total Sales (USD)")
    plt.xticks(rotation=45)
    patch = mpatches.Patch(color=ACCENT, label="Daily Sales")
    ax.legend(handles=[patch], title="Metric", title_fontsize=8, fontsize=8, loc="upper left",
              facecolor=CHART_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
    plt.tight_layout()
    st.pyplot(fig)
    chart_download_btn(fig, "daily_trend.png", "chart_trend")  # ← download button
    plt.close(fig)

    # ── Chart 6 — Sales by Weekday ───────────────────────────
    st.markdown("<div class='section-title'>📅 Sales by Day of Week</div>", unsafe_allow_html=True)
    weekday            = filtered_data.copy()
    weekday["Weekday"] = weekday["Date"].dt.day_name()
    day_order          = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    weekday_sales      = weekday.groupby("Weekday")["Sales"].sum().reindex(day_order).fillna(0)
    max_day            = weekday_sales.idxmax()
    bar_colors         = [ACCENT if d == max_day else "#2a5298" for d in weekday_sales.index]

    fig, ax = plt.subplots(figsize=(12, 4))
    bars = ax.bar(weekday_sales.index, weekday_sales.values, color=bar_colors,
                  edgecolor=CHART_BG, linewidth=1.5, width=0.6)
    style_ax(ax, title="Sales by Day of Week", xlabel="Day", ylabel="Total Sales (USD)")
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 50,
                f"${height:,.0f}", ha="center", va="bottom",
                fontsize=8, color=TEXT_COLOR, fontweight="600")
    patch_best  = mpatches.Patch(color=ACCENT,   label=f"Best Day: {max_day}")
    patch_other = mpatches.Patch(color="#2a5298", label="Other Days")
    ax.legend(handles=[patch_best, patch_other], title="Weekday", title_fontsize=8,
              fontsize=8, loc="upper right",
              facecolor=CHART_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
    plt.tight_layout()
    st.pyplot(fig)
    chart_download_btn(fig, "weekday_sales.png", "chart_weekday")  # ← download button
    plt.close(fig)


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
    ✨ Built with Streamlit · Matplotlib · Seaborn &nbsp;|&nbsp;
    Developer: <strong>Muhammed Ilyas Arain</strong> &nbsp;|&nbsp;
    IBA University Intern &nbsp;|&nbsp;
    <a href='https://github.com/ilyasarain943' style='color:#00d4ff;text-decoration:none;'>GitHub 🔗</a>
</div>
""", unsafe_allow_html=True)