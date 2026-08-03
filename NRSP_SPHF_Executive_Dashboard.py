import streamlit as st
import pandas as pd
import plotly.express as px

from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4, landscape, portrait

st.set_page_config(
    page_title="NRSP SPHF MIS Dashboard",
    layout="wide",
    page_icon="🏠"
)

# =========================
# LOGO FILE NAMES (kept consistent everywhere in this file)
# =========================

NRSP_LOGO = "NRSP_Logo.png"
SPHF_LOGO = "SPHF_Logo.png"
GOVT_LOGO = "Govt_Balochistan.png"

# =========================
# LOGIN SYSTEM
# =========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.markdown(
        """
        <style>

        /* Hide default Streamlit chrome for a cleaner login look */
        #MainMenu, header, footer {visibility: hidden;}

        .stApp {
            background: radial-gradient(circle at top left, #eafaf1 0%, #f6fbf7 45%, #eef6f0 100%);
        }

        /* Login Card */
        div[data-testid="stForm"] {
            background-color: #ffffff;
            padding: 40px 45px 30px 45px;
            border-radius: 22px;
            box-shadow: 0px 15px 45px rgba(0, 80, 0, 0.12);
            border: 1px solid #e3ede4;
            max-width: 420px;
            margin: auto;
        }

        /* Input fields */
        div[data-testid="stForm"] input {
            border-radius: 10px !important;
            border: 1.5px solid #d7e5da !important;
            padding: 10px 12px !important;
            font-size: 15px !important;
            background-color: #f9fbfa !important;
        }

        div[data-testid="stForm"] input:focus {
            border: 1.5px solid #006400 !important;
            box-shadow: 0 0 0 3px rgba(0,100,0,0.12) !important;
        }

        /* Only style the SUBMIT button, never the password eye icon */
        div[data-testid="stFormSubmitButton"] button {
            background: linear-gradient(135deg, #007a00, #004d00);
            color: white !important;
            font-weight: 600;
            font-size: 16px;
            border-radius: 10px;
            height: 46px;
            width: 100%;
            border: none;
            margin-top: 10px;
            transition: 0.25s ease;
        }

        div[data-testid="stFormSubmitButton"] button:hover {
            background: linear-gradient(135deg, #005c00, #003300);
            transform: translateY(-1px);
            box-shadow: 0px 6px 18px rgba(0,80,0,0.25);
        }

        .login-logo-box {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 10px;
        }

        .login-title {
            text-align:center;
            color:#004d00;
            font-weight:800;
            font-size:30px;
            margin-bottom:2px;
            letter-spacing: 0.5px;
        }

        .login-subtitle {
            text-align:center;
            color:#5a6b5d;
            font-size:15px;
            margin-bottom:25px;
        }

        .login-footer {
            text-align:center;
            color:#8a9a8c;
            font-size:12.5px;
            margin-top:18px;
            line-height:1.6;
        }

        .login-footer b {
            color:#4a5a4c;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="login-logo-box">', unsafe_allow_html=True)
    lc1, lc2, lc3 = st.columns([2, 1, 2])
    with lc2:
        st.image(NRSP_LOGO, width=90)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="login-title">NRSP — SPHF MIS</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-subtitle">Flood Reconstruction Monitoring &amp; Information System</div>', unsafe_allow_html=True)

    with st.form("login_form"):

        username = st.text_input("👤 Username", placeholder="Enter your username")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")

        st.write("")

        submitted = st.form_submit_button("🔓  Login to Dashboard")

        if submitted:

            if username == "Waseem123" and password == "098765":
                st.session_state.logged_in = True
                st.rerun()

            else:
                st.error("❌ Invalid Username or Password")

    st.markdown(
        """
        <div class="login-footer">
            Designed &amp; Developed by <b>Waseem Baloch</b><br>
            MIS – M&amp;E Officer, NRSP SPHF Project
        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()

# =========================
# GLOBAL DASHBOARD STYLING
# =========================

import html as _html_lib

st.markdown(
    """<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    #MainMenu, footer {visibility: hidden;}

    html, body, [class*="css"], .stMarkdown, .stText, p, span, div, li {
        font-family: 'Inter', 'Segoe UI', sans-serif !important;
    }

    h1, h2, h3, h4, h5, .nrsp-section, .nrsp-title, .kpi-value {
        font-family: 'Poppins', 'Segoe UI', sans-serif !important;
    }

    .stApp {
        background:
            radial-gradient(circle at 8% 0%, #eafaf1 0%, transparent 45%),
            radial-gradient(circle at 95% 12%, #eaf3fb 0%, transparent 40%),
            linear-gradient(180deg, #f6faf8 0%, #eef3f0 100%);
    }

    /* ============ SIDEBAR ============ */
    section[data-testid="stSidebar"] {
        background: linear-gradient(200deg, #063d1e 0%, #0b6e4f 60%, #0e8a63 100%);
        border-right: none;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p {
        color: #eafaf1 !important;
        font-weight: 600 !important;
    }
    /* Force the select control itself to always have a light, readable surface
       (fixes previously invisible white-on-white text in the sidebar) */
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border-radius: 10px !important;
        border: none !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"] * {
        color: #0b3d21 !important;
        font-weight: 600 !important;
    }
    .sidebar-brand {
        text-align: center;
        padding: 6px 0 18px 0;
        border-bottom: 1px solid rgba(255,255,255,0.18);
        margin-bottom: 18px;
    }
    .sidebar-brand h3 {
        color: #ffffff !important;
        font-weight: 800 !important;
        margin: 8px 0 0 0;
        letter-spacing: 0.5px;
    }
    .sidebar-brand p {
        color: #bfe8d3 !important;
        font-size: 12.5px !important;
        margin: 2px 0 0 0 !important;
    }

    /* ============ TOP BANNER ============ */
    .nrsp-banner {
        background: linear-gradient(120deg, #ffffff 0%, #eafaf4 100%);
        border-radius: 22px;
        padding: 24px 30px;
        box-shadow: 0px 12px 34px rgba(0,80,40,0.10);
        border: 1px solid #e2efe6;
        margin-bottom: 22px;
        position: relative;
        overflow: hidden;
    }
    .nrsp-banner::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 6px;
        background: linear-gradient(90deg, #0b6e4f, #1e88e5, #8e24aa, #ef6c00);
    }
    .nrsp-title {
        text-align: center;
        color: #08341e;
        font-weight: 800;
        font-size: 32px;
        margin-bottom: 4px;
        letter-spacing: 0.3px;
        line-height: 1.3;
    }
    .nrsp-subtitle {
        text-align: center;
        font-size: 15.5px;
        color: #5c6f61;
        font-weight: 500;
        letter-spacing: 0.3px;
    }

    /* ============ HERO KPI CARDS ============ */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 18px;
        margin-bottom: 8px;
    }
    .kpi-card {
        border-radius: 18px;
        padding: 22px 20px;
        color: #ffffff;
        box-shadow: 0px 12px 30px rgba(0,0,0,0.12);
        position: relative;
        overflow: hidden;
        transition: 0.25s ease;
    }
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0px 18px 38px rgba(0,0,0,0.18);
    }
    .kpi-card::after {
        content: "";
        position: absolute;
        right: -20px;
        bottom: -20px;
        width: 90px;
        height: 90px;
        border-radius: 50%;
        background: rgba(255,255,255,0.12);
    }
    .kpi-icon { font-size: 26px; margin-bottom: 6px; }
    .kpi-value {
        font-size: 32px;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 2px;
    }
    .kpi-label {
        font-size: 13.5px;
        font-weight: 600;
        opacity: 0.92;
        letter-spacing: 0.3px;
    }

    /* ============ SECTION HEADERS ============ */
    .nrsp-section-wrap {
        margin: 30px 0 16px 0;
    }
    .nrsp-section {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 13px 22px;
        border-radius: 14px;
        font-size: 20px;
        font-weight: 700;
        color: #ffffff;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.12);
        letter-spacing: 0.2px;
    }
    .nrsp-section .badge-dot {
        width: 10px; height: 10px;
        border-radius: 50%;
        background: rgba(255,255,255,0.85);
        box-shadow: 0 0 0 4px rgba(255,255,255,0.25);
    }

    /* ============ METRIC CARDS ============ */
    div[data-testid="stMetric"] {
        background: #ffffff;
        border-radius: 16px;
        padding: 16px 14px 14px 14px;
        border: 1px solid #e6efe9;
        border-top: 5px solid #0b6e4f;
        box-shadow: 0px 8px 22px rgba(0,60,30,0.08);
        transition: 0.2s ease;
        text-align: center;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0px 14px 30px rgba(0,60,30,0.16);
    }
    div[data-testid="stMetricLabel"] {
        color: #55665a !important;
        font-weight: 600 !important;
        justify-content: center !important;
        font-size: 13.5px !important;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }
    div[data-testid="stMetricValue"] {
        color: #08341e !important;
        font-weight: 800 !important;
        font-size: 30px !important;
        justify-content: center !important;
    }

    /* ============ BUTTONS ============ */
    .stButton>button {
        background: linear-gradient(135deg, #0e8a63, #063d1e);
        color: white;
        border-radius: 10px;
        border: none;
        font-weight: 600;
        padding: 9px 20px;
        letter-spacing: 0.3px;
        transition: 0.2s ease;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0px 8px 20px rgba(0,60,30,0.28);
    }

    .stDownloadButton>button {
        background: linear-gradient(135deg, #2196f3, #0d47a1);
        color: white;
        border-radius: 10px;
        border: none;
        font-weight: 600;
        padding: 9px 20px;
        letter-spacing: 0.3px;
        transition: 0.2s ease;
    }
    .stDownloadButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0px 8px 20px rgba(13,71,161,0.30);
    }

    /* ============ DATAFRAMES (raw / large tables) ============ */
    div[data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid #e2efe6;
        box-shadow: 0px 8px 22px rgba(0,0,0,0.06);
    }

    /* ============ CUSTOM STYLED TABLES ============ */
    .nrsp-table-wrap {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0px 10px 26px rgba(0,40,20,0.10);
        border: 1px solid #e2efe6;
        margin-bottom: 6px;
    }
    table.nrsp-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 14px;
    }
    table.nrsp-table thead tr {
        background: linear-gradient(120deg, #0b6e4f, #0e8a63 55%, #1565c0);
    }
    table.nrsp-table thead th {
        color: #ffffff !important;
        font-weight: 700;
        padding: 13px 12px;
        text-align: center;
        white-space: nowrap;
        letter-spacing: 0.2px;
    }
    table.nrsp-table tbody td {
        padding: 11px 12px;
        text-align: center;
        color: #2b3a30;
        border-bottom: 1px solid #eef3ef;
    }
    table.nrsp-table tbody tr:nth-child(even) {
        background-color: #f6faf7;
    }
    table.nrsp-table tbody tr:hover {
        background-color: #eaf6ef;
        transition: 0.15s ease;
    }
    table.nrsp-table td.cell-pending {
        color: #c62828;
        font-weight: 700;
    }
    table.nrsp-table td.cell-done {
        color: #0b6e4f;
        font-weight: 700;
    }

    /* ============ INPUTS / SELECTBOXES (main area) ============ */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        border-radius: 10px !important;
    }
    .stTextInput input:focus {
        border-color: #0b6e4f !important;
        box-shadow: 0 0 0 3px rgba(11,110,79,0.15) !important;
    }

    /* ============ ALERT BOXES ============ */
    div[data-testid="stAlert"] {
        border-radius: 12px;
        font-weight: 500;
    }

    hr {
        border: none;
        border-top: 2px solid #d9ece1;
        margin: 28px 0;
    }

    /* Plotly chart container */
    div[data-testid="stPlotlyChart"] {
        background: #ffffff;
        border-radius: 16px;
        padding: 10px;
        box-shadow: 0px 8px 22px rgba(0,0,0,0.06);
        border: 1px solid #e2efe6;
    }

    /* ============ SEARCH FORM CARD ============ */
    div[data-testid="stForm"] {
        background: #ffffff;
        border-radius: 18px;
        padding: 22px 26px;
        box-shadow: 0px 10px 26px rgba(0,60,30,0.08);
        border: 1px solid #e2efe6;
    }

    /* ============ BENEFICIARY PROFILE CARD ============ */
    .nrsp-profile-card {
        background: linear-gradient(160deg, #ffffff, #f4faf7);
        border-radius: 18px;
        padding: 0 0 18px 0;
        margin-bottom: 22px;
        box-shadow: 0px 12px 32px rgba(0,60,30,0.12);
        border: 1px solid #e2efe6;
        overflow: hidden;
    }
    .nrsp-profile-header {
        background: linear-gradient(120deg, #0b6e4f, #0e8a63 55%, #1565c0);
        padding: 18px 26px;
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .nrsp-profile-avatar {
        width: 46px; height: 46px;
        border-radius: 50%;
        background: rgba(255,255,255,0.22);
        display: flex; align-items: center; justify-content: center;
        font-size: 22px;
        flex-shrink: 0;
    }
    .nrsp-profile-name {
        color: #ffffff;
        font-weight: 700;
        font-size: 20px;
        line-height: 1.3;
    }
    .nrsp-profile-tag {
        color: #dffcec;
        font-size: 12.5px;
        font-weight: 500;
        opacity: 0.9;
    }
    .nrsp-field-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 14px;
        padding: 22px 26px 6px 26px;
    }
    .nrsp-field {
        background: #ffffff;
        border: 1px solid #e9f2ec;
        border-radius: 12px;
        padding: 11px 15px;
        box-shadow: 0px 3px 10px rgba(0,0,0,0.04);
    }
    .nrsp-field-label {
        font-size: 11.5px;
        color: #6d7d70;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.4px;
        margin-bottom: 3px;
    }
    .nrsp-field-value {
        font-size: 15px;
        color: #16281d;
        font-weight: 600;
        word-break: break-word;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    """
    <div class="sidebar-brand">
        <h3>NRSP · SPHF MIS</h3>
        <p>Flood Reconstruction Monitoring</p>
    </div>
    """,
    unsafe_allow_html=True
)

_SECTION_PALETTE = [
    "#0b6e4f", "#1565c0", "#8e24aa", "#ef6c00",
    "#00897b", "#c62828", "#2c3e50", "#6a1b9a",
    "#00695c", "#ad1457", "#37474f", "#4527a0"
]
_section_state = {"i": 0}


def section_header(title):
    """Render a colorful, professional section header (replaces st.subheader)."""
    color = _SECTION_PALETTE[_section_state["i"] % len(_SECTION_PALETTE)]
    _section_state["i"] += 1
    st.markdown(
        f"""
        <div class="nrsp-section-wrap">
            <div class="nrsp-section" style="background: linear-gradient(120deg, {color}, {color}cc);">
                <span class="badge-dot"></span>{title}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_table(df):
    """Render a compact summary DataFrame as a polished, presentation-quality HTML table."""

    if df is None or df.empty:
        st.info("No data available.")
        return

    headers = df.columns.tolist()

    rows_html = ""
    for _, row in df.iterrows():
        cells_html = ""
        for h in headers:
            val = row[h]
            col_lower = str(h).lower()
            cell_class = ""

            if isinstance(val, (int, float)) and not isinstance(val, bool):
                if "pending" in col_lower and float(val) > 0:
                    cell_class = "cell-pending"
                elif ("done" in col_lower or "verified" in col_lower or "disbursed" in col_lower) and float(val) > 0:
                    cell_class = "cell-done"
                display_val = f"{val:,.0f}" if float(val) == int(val) else f"{val:,.2f}"
            else:
                display_val = _html_lib.escape(str(val)) if pd.notna(val) else ""

            cells_html += f'<td class="{cell_class}">{display_val}</td>'

        rows_html += f"<tr>{cells_html}</tr>"

    header_html = "".join(f"<th>{_html_lib.escape(str(h))}</th>" for h in headers)

    table_html = f"""
    <div class="nrsp-table-wrap">
        <table class="nrsp-table">
            <thead><tr>{header_html}</tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
    </div>
    """

    st.markdown(table_html, unsafe_allow_html=True)


def render_beneficiary_card(row, columns):
    """Render a single beneficiary record as a polished profile/ID card.
    Works with ANY set of columns — it does not assume a fixed schema."""

    name_col = next(
        (c for c in columns if "name" in c.lower() and "father" not in c.lower() and "husband" not in c.lower()),
        None
    )
    header_name = str(row[name_col]).strip() if name_col and pd.notna(row[name_col]) else "Beneficiary Record"

    id_col = next((c for c in columns if "uuid" in c.lower()), None)
    tag_text = f"UUID: {row[id_col]}" if id_col and pd.notna(row[id_col]) else ""

    fields_html = ""
    for c in columns:
        val = row[c]
        display_val = _html_lib.escape(str(val).strip()) if pd.notna(val) and str(val).strip() != "" else "—"
        fields_html += f"""
        <div class="nrsp-field">
            <div class="nrsp-field-label">{_html_lib.escape(str(c))}</div>
            <div class="nrsp-field-value">{display_val}</div>
        </div>
        """

    st.markdown(
        f"""
        <div class="nrsp-profile-card">
            <div class="nrsp-profile-header">
                <div class="nrsp-profile-avatar">👤</div>
                <div>
                    <div class="nrsp-profile-name">{_html_lib.escape(header_name)}</div>
                    <div class="nrsp-profile-tag">{_html_lib.escape(tag_text)}</div>
                </div>
            </div>
            <div class="nrsp-field-grid">
                {fields_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================
# LOAD DATA
# =========================

@st.cache_data(ttl=60)
def load_data():

    SHEET_ID = "1DefXTvqGRyq8lW7fF9Ud7ePhmi9W_Le-gYeRcImG26c"
    GID = "2141693356"

    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df

    except Exception as e:
        st.error(f"Google Sheet Load Error: {e}")
        st.stop()

STAFF_GID = "224345141"

@st.cache_data(ttl=60)
def load_staff():

    SHEET_ID = "1DefXTvqGRyq8lW7fF9Ud7ePhmi9W_Le-gYeRcImG26c"

    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={STAFF_GID}"

    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df

    except Exception as e:
        st.error(f"Staff Sheet Load Error: {e}")
        return pd.DataFrame()

def create_pending_pdf(df_report, bank, installment):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=10,
        rightMargin=10,
        topMargin=20,
        bottomMargin=20
    )

    styles = getSampleStyleSheet()

    elements = []

    # =========================
    # LOGOS
    # =========================

    try:
        logo1 = Image(
            NRSP_LOGO,
            width=90,
            height=40
        )

        logo2 = Image(
            SPHF_LOGO,
            width=90,
            height=40
        )

        logo_table = Table(
            [[logo1, "", logo2]],
                colWidths=[120, 450, 120]
        )

        logo_table.setStyle(
            TableStyle([
                ("ALIGN", (0, 0), (0, 0), "LEFT"),
                ("ALIGN", (2, 0), (2, 0), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
            ])
        )

        elements.append(logo_table)
        elements.append(Spacer(1, 10))

    except Exception:
        pass

    # =========================
    # TITLE
    # =========================

    title = Paragraph(
    f"""
    <b>NRSP - SPHF Monitoring Report</b><br/>
    <br/>
    Report : {installment}
    <br/>
    Bank : {bank}
    <br/>
    Total Beneficiaries : {len(df_report)}
    """,
    styles["Title"]
)
    
    elements.append(title)
    elements.append(Spacer(1, 12))

    # =========================
    # TABLE
    # =========================


    # Use exactly the columns received from caller
    available_columns = df_report.columns.tolist()

    table_data = [available_columns]
    table_data += df_report.fillna("").values.tolist()

    col_widths = []

    for col in available_columns:

        if col == "S. No.":
            col_widths.append(25)

        elif col == "UUID":
            col_widths.append(55)

        elif col == "Beneficiary Name":
            col_widths.append(90)

        elif col == "Father/Husband Name":
            col_widths.append(100)

        elif col == "Mobile Number":
            col_widths.append(70)

        elif col == "Gender":
            col_widths.append(40)

        elif col == "CNIC No.":
            col_widths.append(75)

        elif col == "District":
            col_widths.append(55)

        elif col == "Tehsil":
            col_widths.append(50)

        elif col == "UC":
            col_widths.append(45)

        elif col == "Village":
            col_widths.append(110)

        elif col == "Account No.":
            col_widths.append(95)

        elif col == "Bank":
            col_widths.append(90)

        elif col == "Remarks":
            col_widths.append(80)

        else:
            col_widths.append(70)
    
    table = Table(
        table_data,
        colWidths=col_widths,
        repeatRows=1
    )

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9D9D9")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),

            ("FONTSIZE", (0, 0), (-1, 0), 8),
            ("FONTSIZE", (0, 1), (-1, -1), 7),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("BOX", (0, 0), (-1, -1), 1, colors.black),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
            ("TOPPADDING", (0, 1), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 4),
        ])
    )

    elements.append(table)
    elements.append(Spacer(1, 15))

    # =========================
    # FOOTER
    # =========================

    footer = Paragraph(
        """
        <para align="center">
        <font size="9">
        Designed &amp; Developed by <b>Waseem Baloch</b>
        </font>
        </para>
        """,
        styles["Normal"]
    )

    elements.append(footer)

    # =========================
    # BUILD PDF
    # =========================

    doc.build(elements)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf

from reportlab.pdfbase import pdfmetrics
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase.ttfonts import TTFont
import datetime

try:
    pdfmetrics.registerFont(TTFont("Calibri", "calibri.ttf"))
    FONT = "Calibri"
except:
    FONT = "Helvetica"


def create_completion_certificate_pdf(beneficiary):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=portrait(A4),
        leftMargin=25,
        rightMargin=25,
        topMargin=20,
        bottomMargin=20
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.fontName = FONT
    title_style.alignment = TA_CENTER
    title_style.fontSize = 24
    title_style.leading = 30

    normal = styles["Normal"]
    normal.fontName = FONT
    normal.fontSize = 10
    normal.leading = 24

    elements = []

    # ==========================
    # LOGOS
    # ==========================

    try:

        govt = Image(
            GOVT_LOGO,
            width=65,
            height=60
        )

    except:
        govt = ""

    try:

        sphf = Image(
            SPHF_LOGO,
            width=70,
            height=60
        )

    except:
        sphf = ""

    try:

        nrsp = Image(
            NRSP_LOGO,
            width=80,
            height=45
        )

    except:
        nrsp = ""

    logo_table = Table(
        [[govt, sphf, nrsp]],
        colWidths=[170,170,170]
    )

    logo_table.setStyle(
        TableStyle([
            ("ALIGN",(0,0),(0,0),"LEFT"),
            ("ALIGN",(1,0),(1,0),"CENTER"),
            ("ALIGN",(2,0),(2,0),"RIGHT"),
            ("VALIGN",(0,0),(-1,-1),"MIDDLE")
        ])
    )

    elements.append(logo_table)
    elements.append(Spacer(1,20))

    # ==========================
    # TITLE
    # ==========================

    elements.append(
        Paragraph(
            "HOUSE COMPLETION CERTIFICATE",
            title_style
        )
    )

    elements.append(
        Paragraph(
            "Sindh People's Housing for Flood Affectees (SPHF)",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1,15))

    # ==========================
    # CERTIFICATE TEXT
    # ==========================

    certificate_text = f"""
    This is to certify that <b>{beneficiary['Beneficiary Name']}</b>,
    Son / Daughter / Wife of
    <b>{beneficiary['Father/Husband Name']}</b>,
    bearing CNIC No.
    <b>{beneficiary['CNIC No.']}</b>,
    resident of
    <b>{beneficiary['Village']}</b>,
    Union Council
    <b>{beneficiary['UC']}</b>,
    Tehsil
    <b>{beneficiary['Tehsil']}</b>,
    District
    <b>{beneficiary['District']}</b>,
    has successfully completed the reconstruction of a flood resilient
    house under the Sindh People's Housing for Flood Affectees (SPHF)
    Project implemented by NRSP in collaboration with the Government
    of Balochistan.

    The construction has been completed in accordance with the approved
    technical standards and project guidelines.
    """

    elements.append(
        Paragraph(
            certificate_text,
            normal
        )
    )

    elements.append(Spacer(1,15))

    # ==========================
    # BENEFICIARY INFORMATION
    # ==========================

    info_data = [

        ["UUID", beneficiary["UUID"]],

        ["Beneficiary Name",
         beneficiary["Beneficiary Name"]],

        ["Father / Husband",
         beneficiary["Father/Husband Name"]],

        ["CNIC",
         beneficiary["CNIC No."]],

        ["Village",
         beneficiary["Village"]],

        ["UC",
         beneficiary["UC"]],

        ["Tehsil",
         beneficiary["Tehsil"]],

        ["District",
         beneficiary["District"]]

    ]

    info_table = Table(
        info_data,
        colWidths=[150,330]
    )

    info_table.setStyle(

        TableStyle([

            ("GRID",(0,0),(-1,-1),0.5,colors.black),

            ("BACKGROUND",(0,0),(0,-1),
             colors.HexColor("#EAF4EA")),

            ("FONTNAME",(0,0),(-1,-1),FONT),

            ("FONTSIZE",(0,0),(-1,-1),12),

            ("BOTTOMPADDING",(0,0),(-1,-1),8),

            ("TOPPADDING",(0,0),(-1,-1),8),

            ("VALIGN",(0,0),(-1,-1),"MIDDLE")

        ])

    )

    elements.append(info_table)

    elements.append(Spacer(1,15))

    # ==========================
    # SIGNATURES
    # ==========================

    sign_table = Table(
        [[
            "____________________\nBeneficiary",

            "____________________\nEngineer",

            "____________________\nMIS-M&E Officer",

            "____________________\nDistrict Manager"
        ]],
        colWidths=[120,120,120,120]
    )

    sign_table.setStyle(
        TableStyle([

            ("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("VALIGN",(0,0),(-1,-1),"BOTTOM"),
            ("TOPPADDING",(0,0),(-1,-1),12),
            ("BOTTOMPADDING",(0,0),(-1,-1),10),
            ("FONTNAME",(0,0),(-1,-1),FONT),
            ("FONTSIZE",(0,0),(-1,-1),12)

        ])
    )

    elements.append(sign_table)

    elements.append(Spacer(1,15))

    # ==========================
    # ISSUE DATE
    # ==========================

    issue_date = datetime.datetime.now().strftime("%d-%m-%Y")

    elements.append(
        Paragraph(
            f"<b>Date of Issue :</b> {issue_date}",
            normal
        )
    )

    elements.append(Spacer(1,20))

    # ==========================
    # FOOTER
    # ==========================

    elements.append(
        Paragraph(
            "<para align='center'><font size='10'>"
            "Generated from NRSP SPHF MIS Dashboard"
            "<br/>Designed & Developed by <b>Waseem Baloch</b>"
            "</font></para>",
            styles["Normal"]
        )
    )

    # ==========================
    # BUILD PDF
    # ==========================

    doc.build(elements)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf
    
df = load_data()

# =========================
# COLUMN VALIDATION
# =========================

required_columns = [
    "District",
    "Bank",

    "SPHF 1st Disbursement status Yes/No",
    "1st installment withdrawal Yes/No",

    "SPHF 2nd Disbursement status Yes/No",
    "2nd installment withdrawal Yes/No",

    "SPHF 3rd Disbursement status Yes/No",
    "3rd installment withdrawal Yes/No",

    "SPHF 4th Disbursement status Yes/No",
    "4th installment withdrawal Yes/No",

    "Plinth Verify Yes/No",
    "Lintel Verify Yes/No",
    "Roof Verify Yes/No",
    "Completion Yes/No",

    "Remarks",

    "UUID",
    "CNIC No.",
    "Beneficiary Name",
    "Father/Husband Name",
    "Mobile Number",
    "Gender",
    "Tehsil",
    "UC",
    "Village",
    "Account No.",
    "S. No."
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error("❌ Missing Columns Found in Google Sheet")
    st.write(missing_columns)
    st.stop()
    
# =========================
# HEADER WITH LOGOS
# =========================

st.markdown(
    """
    <style>
    .nrsp-banner [data-testid="stHorizontalBlock"] {
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="nrsp-banner">', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    st.image(NRSP_LOGO, width=105)

with col2:
    st.markdown(
        """
        <div class="nrsp-title">NRSP – SPHF Flood Reconstruction MIS</div>
        <div class="nrsp-subtitle">Government of Balochistan &nbsp;•&nbsp; SPHF Project &nbsp;•&nbsp; National Rural Support Programme</div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.image(SPHF_LOGO, width=105)

st.markdown('</div>', unsafe_allow_html=True)


# =========================
# HELPERS
# =========================

def is_yes(series):
    return (
        series.fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
        .eq("YES")
    )

def yes_count(series):
    return is_yes(series).sum()

def no_remarks(series):
    return (
        series.fillna("")
        .astype(str)
        .str.strip()
        .eq("")
    )
    

# =========================
# COLUMN NAMES
# =========================

DISTRICT = "District"
BANK = "Bank"

SPHF1 = "SPHF 1st Disbursement status Yes/No"
WD1 = "1st installment withdrawal Yes/No"

SPHF2 = "SPHF 2nd Disbursement status Yes/No"
WD2 = "2nd installment withdrawal Yes/No"

SPHF3 = "SPHF 3rd Disbursement status Yes/No"
WD3 = "3rd installment withdrawal Yes/No"

SPHF4 = "SPHF 4th Disbursement status Yes/No"
WD4 = "4th installment withdrawal Yes/No"

PLINTH = "Plinth Verify Yes/No"
LINTEL = "Lintel Verify Yes/No"
ROOF = "Roof Verify Yes/No"
COMP = "Completion Yes/No"
REMARKS = "Remarks"


# =========================
# FILTER
# =========================

districts = ["All"] + sorted(
    df[DISTRICT]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

st.sidebar.markdown("### 🏘️ Filters")

selected_district = st.sidebar.selectbox(
    "District Filter",
    districts
)

if selected_district != "All":
    df = df[df[DISTRICT].astype(str) == selected_district]


# =========================
# INSTALLMENT LOGIC
# =========================

d1 = yes_count(df[WD1])
p1 = (
    is_yes(df[SPHF1]) &
    ~is_yes(df[WD1]) &
    no_remarks(df[REMARKS])
).sum()

d2 = yes_count(df[WD2])
p2 = (
    is_yes(df[SPHF2]) &
    ~is_yes(df[WD2]) &
    no_remarks(df[REMARKS])
).sum()

d3 = yes_count(df[WD3])
p3 = (
    is_yes(df[SPHF3]) &
    ~is_yes(df[WD3]) &
    no_remarks(df[REMARKS])
).sum()

d4 = yes_count(df[WD4])
p4 = (
    is_yes(df[SPHF4]) &
    ~is_yes(df[WD4]) &
    no_remarks(df[REMARKS])
).sum()

total_done = d1 + d2 + d3 + d4
total_pending = p1 + p2 + p3 + p4

# =========================
# SPHF DISBURSEMENT OVERVIEW
# =========================

sp1 = yes_count(df[SPHF1])
sp2 = yes_count(df[SPHF2])
sp3 = yes_count(df[SPHF3])
sp4 = yes_count(df[SPHF4])

total_disbursed = sp1 + sp2 + sp3 + sp4

total_beneficiaries = len(df)
completion_verified = yes_count(df[COMP])
completion_pct = round(
    (completion_verified / total_beneficiaries) * 100, 1
) if total_beneficiaries > 0 else 0

st.markdown(
    f"""
    <div class="kpi-grid">
        <div class="kpi-card" style="background:linear-gradient(135deg,#0b6e4f,#063d1e);">
            <div class="kpi-icon">👨‍👩‍👧‍👦</div>
            <div class="kpi-value">{total_beneficiaries:,}</div>
            <div class="kpi-label">TOTAL BENEFICIARIES</div>
        </div>
        <div class="kpi-card" style="background:linear-gradient(135deg,#1565c0,#0d3b73);">
            <div class="kpi-icon">🏦</div>
            <div class="kpi-value">{total_disbursed:,}</div>
            <div class="kpi-label">TOTAL DISBURSEMENTS</div>
        </div>
        <div class="kpi-card" style="background:linear-gradient(135deg,#ef6c00,#a24800);">
            <div class="kpi-icon">⏳</div>
            <div class="kpi-value">{total_pending:,}</div>
            <div class="kpi-label">WITHDRAWALS PENDING</div>
        </div>
        <div class="kpi-card" style="background:linear-gradient(135deg,#8e24aa,#4a148c);">
            <div class="kpi-icon">🏆</div>
            <div class="kpi-value">{completion_pct}%</div>
            <div class="kpi-label">HOUSES COMPLETED</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

section_header("🏦 SPHF Disbursement Overview")

r1c1, r1c2, r1c3, r1c4, r1c5 = st.columns(5)

r1c1.metric("1st Disbursed", sp1)
r1c2.metric("2nd Disbursed", sp2)
r1c3.metric("3rd Disbursed", sp3)
r1c4.metric("4th Disbursed", sp4)
r1c5.metric("Total Disbursed", total_disbursed)

sp_df = pd.DataFrame({
    "Installment":["1st","2nd","3rd","4th"],
    "Disbursed":[sp1,sp2,sp3,sp4]
})

st.plotly_chart(
    px.bar(
        sp_df,
        x="Installment",
        y="Disbursed",
        title="SPHF Installment Disbursement",
        color="Installment",
        color_discrete_sequence=px.colors.qualitative.Bold,
        text="Disbursed"
    ),
    use_container_width=True
)

section_header("💰 Overall Trenches Withdrawal Summary")

r2c1, r2c2, r2c3 = st.columns(3)

r2c1.metric("Withdrawals Done", total_done)
r2c2.metric("Withdrawals Pending", total_pending)

pending_pct = round(
    (total_pending / (total_done + total_pending)) * 100, 2
) if (total_done + total_pending) > 0 else 0

r2c3.metric("Pending %", f"{pending_pct}%")

section_header("🏗️ Verification Progress")

r3c1, r3c2, r3c3, r3c4 = st.columns(4)

r3c1.metric("Plinth Verified", yes_count(df[PLINTH]))
r3c2.metric("Lintel Verified", yes_count(df[LINTEL]))
r3c3.metric("Roof Verified", yes_count(df[ROOF]))
r3c4.metric("Completion Verified", yes_count(df[COMP]))


# =========================
# INSTALLMENT SUMMARY
# =========================

section_header("📊 Installment Wise Withdrawal Summary")

inst_df = pd.DataFrame({
    "Installment": ["1st", "2nd", "3rd", "4th"],
    "Done": [d1, d2, d3, d4],
    "Pending": [p1, p2, p3, p4]
})

render_table(inst_df)

fig1 = px.bar(
    inst_df,
    x="Installment",
    y=["Done", "Pending"],
    barmode="group",
    title="Installment Wise Done vs Pending",
    color_discrete_sequence=["#0b6e4f", "#e67e22"]
)

st.plotly_chart(fig1, use_container_width=True)


# =========================
# BANK WISE INSTALLMENT REPORT
# =========================

section_header("🏦 Bank Wise Installment Withdrawal Report")

bank_rows = []

for bank, g in df.groupby(BANK):

    bd1 = yes_count(g[WD1])
    bp1 = (is_yes(g[SPHF1]) & ~is_yes(g[WD1])).sum()

    bd2 = yes_count(g[WD2])
    bp2 = (is_yes(g[SPHF2]) & ~is_yes(g[WD2])).sum()

    bd3 = yes_count(g[WD3])
    bp3 = (is_yes(g[SPHF3]) & ~is_yes(g[WD3])).sum()

    bd4 = yes_count(g[WD4])
    bp4 = (is_yes(g[SPHF4]) & ~is_yes(g[WD4])).sum()

    bank_rows.append({

        "Bank": bank,

        "1st Done": bd1,
        "1st Pending": bp1,

        "2nd Done": bd2,
        "2nd Pending": bp2,

        "3rd Done": bd3,
        "3rd Pending": bp3,

        "4th Done": bd4,
        "4th Pending": bp4,

        "Total Done": bd1+bd2+bd3+bd4,
        "Total Pending": bp1+bp2+bp3+bp4
    })

bank_detail_df = pd.DataFrame(bank_rows)

render_table(bank_detail_df)

# Download Button

csv_bank_detail = bank_detail_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Bank Wise Installment Report",
    csv_bank_detail,
    "Bank_Wise_Installment_Report.csv",
    "text/csv"
)

# =========================
# BANK WISE WITHDRAWAL PENDING
# =========================

section_header("⏳ Bank Wise Withdrawal Pending")

pending_rows = []

for bank, g in df.groupby(BANK):

    bp1 = (is_yes(g[SPHF1]) & ~is_yes(g[WD1])).sum()

    bp2 = (is_yes(g[SPHF2]) & ~is_yes(g[WD2])).sum()

    bp3 = (is_yes(g[SPHF3]) & ~is_yes(g[WD3])).sum()

    bp4 = (is_yes(g[SPHF4]) & ~is_yes(g[WD4])).sum()

    pending_rows.append({

        "Bank": bank,

        "1st Pending": bp1,
        "2nd Pending": bp2,
        "3rd Pending": bp3,
        "4th Pending": bp4,

        "Total Pending": bp1 + bp2 + bp3 + bp4

    })

bank_pending_df = pd.DataFrame(pending_rows)

render_table(bank_pending_df)

csv_pending = bank_pending_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Bank Wise Pending Report",
    csv_pending,
    "Bank_Wise_Pending_Report.csv",
    "text/csv"
)

# =========================
# DISTRICT VERIFICATION
# =========================

section_header("✅ District Wise Verification Done")

dist_done_rows = []

for district, g in df.groupby(DISTRICT):

    dist_done_rows.append({

        "District": district,

        "Plinth Done": yes_count(g[PLINTH]),
        "Lintel Done": yes_count(g[LINTEL]),
        "Roof Done": yes_count(g[ROOF]),
        "Completion Done": yes_count(g[COMP])

    })

dist_done_df = pd.DataFrame(dist_done_rows)

render_table(dist_done_df)

csv_done = dist_done_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download District Verification Done Report",
    csv_done,
    "District_Verification_Done.csv",
    "text/csv"
)

# =========================
# DISTRICT VERIFICATION PENDING
# =========================

section_header("⏳ District Wise Verification Pending")

dist_pending_rows = []

for district, g in df.groupby(DISTRICT):

    dist_pending_rows.append({

        "District": district,

        "Plinth Pending":
            len(g) - yes_count(g[PLINTH]),

        "Lintel Pending":
            len(g) - yes_count(g[LINTEL]),

        "Roof Pending":
            len(g) - yes_count(g[ROOF]),

        "Completion Pending":
            len(g) - yes_count(g[COMP])

    })

dist_pending_df = pd.DataFrame(dist_pending_rows)

render_table(dist_pending_df)

csv_pending = dist_pending_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download District Verification Pending Report",
    csv_pending,
    "District_Verification_Pending.csv",
    "text/csv"
)


# =========================
# PENDING WITHDRAWAL DOWNLOAD
# =========================

section_header("📥 Download Pending Withdrawal Beneficiary List")

selected_bank = st.selectbox(
    "🏦 Select Bank",
    sorted(df[BANK].dropna().unique()),
    key="pending_bank"
)

installment = st.selectbox(
    "💳 Select Installment",
    [
        "1st Installment",
        "2nd Installment",
        "3rd Installment",
        "4th Installment"
    ]
)

if installment == "1st Installment":

    pending_df = df[
    is_yes(df[SPHF1]) &
    ~is_yes(df[WD1]) &
    no_remarks(df[REMARKS]) &
    (df[BANK] == selected_bank)
]

elif installment == "2nd Installment":

    pending_df = df[
    is_yes(df[SPHF2]) &
    ~is_yes(df[WD2]) &
    no_remarks(df[REMARKS]) &
    (df[BANK] == selected_bank)
]

elif installment == "3rd Installment":

    pending_df = df[
    is_yes(df[SPHF3]) &
    ~is_yes(df[WD3]) &
    no_remarks(df[REMARKS]) &
    (df[BANK] == selected_bank)
]
    
else:

    pending_df = df[
    is_yes(df[SPHF4]) &
    ~is_yes(df[WD4]) &
    no_remarks(df[REMARKS]) &
    (df[BANK] == selected_bank)
]

st.info(
    f"Total Pending Beneficiaries: {len(pending_df)}"
)

# A to M Columns Only

download_cols = [
    "S. No.",
    "UUID",
    "Beneficiary Name",
    "Father/Husband Name",
    "Mobile Number",
    "CNIC No.",
    "District",
    "Tehsil",
    "UC",
    "Village",
    "Account No.",
    "Bank"
]

pending_download = pending_df[download_cols].copy()

# Village A-Z
pending_download = pending_download.sort_values(
    by="Village",
    ascending=True
)

pdf = create_pending_pdf(
    pending_download,
    selected_bank,
    f"{installment} Pending Withdrawal"
)

st.download_button(
    label="📄 Download PDF Report",
    data=pdf,
    file_name=f"{selected_bank}_{installment}_Pending_List.pdf",
    mime="application/pdf"
)

# =========================
# STAGE VERIFICATION PENDING DOWNLOAD
# =========================

section_header("🏗 Stage Verification Pending Download")

stage = st.selectbox(
    "Select Stage",
    [
        "Plinth",
        "Lintel",
        "Roof",
        "Completion"
    ]
)

bank_option = st.selectbox(
    "🏦 Select Bank",
    ["All"] + sorted(df[BANK].dropna().unique().tolist()),
    key="stage_bank"
)

district_option = st.selectbox(
    "📍 Select District",
    ["All"] + sorted(df[DISTRICT].dropna().unique().tolist()),
    key="stage_district"
)

stage_df = df.copy()

if bank_option != "All":
    stage_df = stage_df[
        stage_df[BANK] == bank_option
    ]

if district_option != "All":
    stage_df = stage_df[
        stage_df[DISTRICT] == district_option
    ]

# --------------------------
# PLINTH
# --------------------------

if stage == "Plinth":

    stage_df = stage_df[
        is_yes(stage_df[SPHF1]) &
        is_yes(stage_df[WD1]) &
        ~is_yes(stage_df[PLINTH])
    ]

# --------------------------
# LINTEL
# --------------------------

elif stage == "Lintel":

    stage_df = stage_df[
        is_yes(stage_df[SPHF2]) &
        is_yes(stage_df[WD2]) &
        ~is_yes(stage_df[LINTEL])
    ]

# --------------------------
# ROOF
# --------------------------

elif stage == "Roof":

    stage_df = stage_df[
        is_yes(stage_df[SPHF3]) &
        is_yes(stage_df[WD3]) &
        ~is_yes(stage_df[ROOF])
    ]

# --------------------------
# COMPLETION
# --------------------------

else:

    stage_df = stage_df[
        is_yes(stage_df[SPHF4]) &
        is_yes(stage_df[WD4]) &
        ~is_yes(stage_df[COMP])
    ]

# Village A-Z

stage_df = stage_df.sort_values(
    "Village"
)

st.success(
    f"Total {stage} Pending : {len(stage_df)}"
)

# =====================================
# STAGE VERIFICATION PDF DOWNLOAD
# =====================================

download_cols = [
    "S. No.",
    "UUID",
    "Beneficiary Name",
    "Father/Husband Name",
    "Mobile Number",
    "Gender",
    "CNIC No.",
    "District",
    "Tehsil",
    "UC",
    "Village"
]

stage_download = stage_df[download_cols].copy()
stage_download["Remarks"] = ""

# Village A-Z
stage_download = stage_download.sort_values(
    by="Village",
    ascending=True
)

pdf_stage = create_pending_pdf(
    stage_download,
    bank_option,
    f"{stage} Verification Pending"
)

st.download_button(
    label="📄 Download Stage Verification Pending PDF",
    data=pdf_stage,
    file_name=f"{stage}_Verification_Pending.pdf",
    mime="application/pdf"
)

# =========================
# REMARKS
# =========================

section_header("📝 AH Remarks Cases")

remarks_df = df[
    df[REMARKS]
    .fillna("")
    .astype(str)
    .str.strip()
    != ""
]

st.info(f"Total Remarks Cases: {len(remarks_df)}")

if remarks_df.empty:
    st.success("No Remarks Cases Found.")
else:
    st.dataframe(
        remarks_df,
        use_container_width=True
    )

    csv_remarks = remarks_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Remarks Report",
        csv_remarks,
        "AH_Remarks_Cases.csv",
        "text/csv"
    )

# =========================
# COMPLETION CERTIFICATES
# =========================

section_header("🏆 House Completion Certificates")

st.info(
    "Generate professional completion certificates for completed SPHF beneficiaries."
)

certificate_uuid = st.text_input(
    "Enter Beneficiary UUID",
    key="certificate_uuid"
).strip()

generate_certificate = st.button(
    "Generate Completion Certificate",
    key="generate_certificate"
)

if generate_certificate:

    if certificate_uuid == "":

        st.warning("Please enter Beneficiary UUID.")

    else:

        beneficiary = df[
            df["UUID"].astype(str).str.strip() == certificate_uuid
        ]

        if beneficiary.empty:

            st.error("❌ No beneficiary found for this UUID.")

        else:

            beneficiary = beneficiary.iloc[0]

            # Check Completion Status
            completion = str(
                beneficiary["Completion Yes/No"]
            ).strip().upper()

            if completion != "YES":

                st.warning(
                    "⚠️ This beneficiary has not completed the house yet. Certificate cannot be generated."
                )

            else:

                st.success(
                    f"Certificate Loaded Successfully for {beneficiary['Beneficiary Name']}"
                )                
                st.markdown("---")

                col1, col2, col3 = st.columns([1,1,1])

                with col1:
                    st.image(GOVT_LOGO, width=100)

                with col2:
                    st.image(SPHF_LOGO, width=100)

                with col3:
                    st.image(NRSP_LOGO, width=100)

                st.markdown(
                    "<h1 style='text-align:center;color:#006400;'>HOUSE COMPLETION CERTIFICATE</h1>",
                        unsafe_allow_html=True,
                )

                st.markdown(
                    "<h3 style='text-align:center;'>Sindh People's Housing for Flood Affectees (SPHF)</h3>",
                        unsafe_allow_html=True,
                )

                st.divider()

                st.write("### Beneficiary Information")

                st.table({
                    "Field": [
                        "UUID",
                        "Beneficiary Name",
                        "Father / Husband",
                        "CNIC",
                        "Village",
                        "UC",
                        "Tehsil",
                        "District"
                ],
                "Value": [
                    beneficiary["UUID"],
                    beneficiary["Beneficiary Name"],
                    beneficiary["Father/Husband Name"],
                    beneficiary["CNIC No."],
                    beneficiary["Village"],
                    beneficiary["UC"],
                    beneficiary["Tehsil"],
                    beneficiary["District"]
                ]
            })

                pdf_certificate = create_completion_certificate_pdf(
                    beneficiary
                )

                st.download_button(
                    label="📄 Download Official Completion Certificate",
                    data=pdf_certificate,
                    file_name=f"Completion_Certificate_{beneficiary['UUID']}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            
# =========================
# SEARCH
# =========================

section_header("🔍 Search Beneficiary")

search = st.text_input(
    "Enter UUID or CNIC"
).strip()

if search:

    result = df[
        df["UUID"].astype(str).str.contains(search, case=False, na=False)
        |
        df["CNIC No."].astype(str).str.contains(search, case=False, na=False)
    ]

    st.success(f"Total Records Found: {len(result)}")

    if result.empty:
        st.warning("No record found.")
    else:
        st.dataframe(
            result,
            use_container_width=True
        )

# =========================
# OVERALL PROJECT BENEFICIARIES (separate master sheet)
# =========================

OVERALL_SHEET_ID = "1NpWBcDN8pxcG2FPmYvwL73QizQE77gts"

@st.cache_data(ttl=60)
def load_overall_beneficiaries():

    url = f"https://docs.google.com/spreadsheets/d/{OVERALL_SHEET_ID}/export?format=csv"

    try:
        odf = pd.read_csv(url)
        odf.columns = odf.columns.str.strip()
        return odf

    except Exception as e:
        st.error(f"Overall Beneficiaries Sheet Load Error: {e}")
        return pd.DataFrame()

section_header("🌍 Overall Project Beneficiaries")

overall_df = load_overall_beneficiaries()

if overall_df.empty:

    st.warning(
        "⚠️ Overall Beneficiaries data could not be loaded. "
        "Please make sure the sheet is shared as \"Anyone with the link — Viewer\"."
    )

else:

    ocol1, ocol2 = st.columns([1, 3])

    with ocol1:
        st.metric("📋 Total Overall Beneficiaries", f"{len(overall_df):,}")

    with ocol2:
        st.info(
            "This is the complete master list of all project beneficiaries. "
            "Search below by UUID or CNIC Number to view a full beneficiary profile."
        )

    with st.form("overall_search_form"):

        sc1, sc2 = st.columns([4, 1])

        with sc1:
            overall_query = st.text_input(
                "🔎 Search by UUID or CNIC Number",
                placeholder="e.g. 42101-1234567-1  or  a UUID"
            ).strip()

        with sc2:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            overall_search_submit = st.form_submit_button("🔍 Search")

    if overall_search_submit:

        if overall_query == "":

            st.warning("Please enter a UUID or CNIC Number to search.")

        else:

            id_cols = [
                c for c in overall_df.columns
                if "uuid" in c.lower() or "cnic" in c.lower()
            ]

            if not id_cols:

                st.error("❌ No UUID/CNIC column found in the Overall Beneficiaries sheet.")

            else:

                match_mask = pd.Series(False, index=overall_df.index)

                for c in id_cols:
                    match_mask = match_mask | (
                        overall_df[c]
                        .astype(str)
                        .str.contains(overall_query, case=False, na=False)
                    )

                matches = overall_df[match_mask]

                if matches.empty:

                    st.error(
                        "❌ No beneficiary found with this UUID / CNIC in the Overall Project Database."
                    )

                else:

                    st.success(f"✅ {len(matches)} Record(s) Found")

                    for _, matched_row in matches.iterrows():
                        render_beneficiary_card(matched_row, overall_df.columns)

# =========================
# PROJECT STAFF
# =========================

section_header("👥 NRSP Project Staff")

staff_df = load_staff()
staff_df.columns = staff_df.columns.str.strip()

cols = st.columns(3)

for i, (_, row) in enumerate(staff_df.iterrows()):

    with cols[i % 3]:

        designation = str(row["Designation"]).replace("**", "").strip()

        st.markdown(
            f"""
            <div style="
                border:1px solid #e0e0e0;
                border-radius:16px;
                padding:18px;
                text-align:center;
                box-shadow:0px 6px 18px rgba(0,60,30,0.08);
                margin-bottom:20px;
                background: linear-gradient(160deg, #ffffff, #f3fbf6);
                border-top: 4px solid #0b6e4f;
            ">
            """,
            unsafe_allow_html=True
        )

        if (
            "Pic URL" in staff_df.columns
            and pd.notna(row["Pic URL"])
            and str(row["Pic URL"]).strip() != ""
        ):
            try:
                st.image(row["Pic URL"], width=150)
            except Exception:
                pass

        st.markdown(
            f"""
            <h4 style="color:#0b6e4f;margin-bottom:2px;">
                {row['Name']}
            </h4>

            <p style="
                color:#555;
                font-size:15px;
                font-weight:bold;
            ">
                {designation}
            </p>
            """,
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)
        
# =========================
# WATERMARK
# =========================

st.markdown(
    """
    <hr>
    <div style="
        text-align:center;
        color:#888888;
        font-size:13px;
        opacity:0.75;
        padding-top:10px;
        padding-bottom:10px;
    ">
        Designed &amp; Developed by <b>Waseem Baloch</b><br>
        MIS – M&amp;E Officer, NRSP SPHF Project
    </div>
    """,
    unsafe_allow_html=True
)
