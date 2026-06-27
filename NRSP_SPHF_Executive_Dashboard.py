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
from reportlab.lib.pagesizes import landscape, A4

st.set_page_config(
    page_title="NRSP SPHF MIS Dashboard",
    layout="wide",
    page_icon="🏠"
)

# =========================
# LOGIN SYSTEM
# =========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("🔐 NRSP SPHF MIS Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == "nrspmis" and password == "nrsp098":

            st.session_state.logged_in = True
            st.rerun()

        else:
            st.error("Invalid Username or Password")

    st.stop()

# =========================
# LOAD DATA
# =========================

@st.cache_data(ttl=60)
def load_data():
    

    SHEET_ID = "1DefXTvqGRyq8lW7fF9Ud7ePhmi9W_Le-gYeRcImG26c"
    GID = "2141693356"

    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

    df = pd.read_csv(url)

    return df

STAFF_GID = "224345141"

@st.cache_data
def load_staff():

    SHEET_ID = "1DefXTvqGRyq8lW7fF9Ud7ePhmi9W_Le-gYeRcImG26c"

    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={STAFF_GID}"

    df = pd.read_csv(url)

    # Header names clean karo
    df.columns = df.columns.str.strip()

    return df

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

    logo1 = Image(
        "NRSP_Logo.png",
        width=90,
        height=40
    )

    logo2 = Image(
        "SPHF_Logo.png",
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

    table_data = [list(df_report.columns)]
    table_data += df_report.values.tolist()

    table = Table(
        table_data,
        repeatRows=1
    )

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("ALIGN", (0, 0), (-1, -1), "CENTER")
        ])
    )

    elements.append(table)
    elements.append(Spacer(1, 20))

    # =========================
    # FOOTER
    # =========================

    footer = Paragraph(
    """
    <para align='center'>
    Designed & Developed by Waseem Baloch
    </para>
    """,
    styles["Normal"]
)

    elements.append(footer)

    doc.build(elements)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf
    
df = load_data()

# =========================
# HEADER WITH LOGOS
# =========================

col1, col2, col3 = st.columns([1,3,1])

with col1:
    st.image("NRSP_Logo.png", width=120)

with col2:
    st.markdown(
        """
        <h1 style='text-align:center;color:#006400;'>
        NRSP - SPHF Flood Reconstruction MIS
        </h1>
        <div style='text-align:center;font-size:18px;'>
        Govt: Of Balochistan | SPHF Project | NRSP
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.image("SPHF_Logo.png", width=120)

st.markdown("---")


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
# EXECUTIVE CARDS
# =========================

sp1 = yes_count(df[SPHF1])
sp2 = yes_count(df[SPHF2])
sp3 = yes_count(df[SPHF3])
sp4 = yes_count(df[SPHF4])

total_disbursed = sp1 + sp2 + sp3 + sp4

st.subheader("🏦 SPHF Disbursement Summary")

r1c1, r1c2, r1c3, r1c4, r1c5 = st.columns(5)

r1c1.metric("1st Disbursed", sp1)
r1c2.metric("2nd Disbursed", sp2)
r1c3.metric("3rd Disbursed", sp3)
r1c4.metric("4th Disbursed", sp4)
r1c5.metric("Total Disbursed", total_disbursed)

st.divider()

st.subheader("💳 Withdrawal Summary")

r2c1, r2c2, r2c3 = st.columns(3)

r2c1.metric("Withdrawals Done", total_done)
r2c2.metric("Withdrawals Pending", total_pending)

pending_pct = round(
    (total_pending / (total_done + total_pending)) * 100, 2
) if (total_done + total_pending) > 0 else 0

r2c3.metric("Pending %", f"{pending_pct}%")

st.divider()

st.subheader("🏗️ Verification Progress")

r3c1, r3c2, r3c3, r3c4 = st.columns(4)

r3c1.metric("Plinth Verified", yes_count(df[PLINTH]))
r3c2.metric("Lintel Verified", yes_count(df[LINTEL]))
r3c3.metric("Roof Verified", yes_count(df[ROOF]))
r3c4.metric("Completion Verified", yes_count(df[COMP]))

# =========================
# SPHF DISBURSEMENT
# =========================

sp1 = yes_count(df[SPHF1])
sp2 = yes_count(df[SPHF2])
sp3 = yes_count(df[SPHF3])
sp4 = yes_count(df[SPHF4])

st.subheader("🏦 SPHF Disbursement Dashboard")

a,b,c,d = st.columns(4)

a.metric("1st Disbursed", sp1)
b.metric("2nd Disbursed", sp2)
c.metric("3rd Disbursed", sp3)
d.metric("4th Disbursed", sp4)

sp_df = pd.DataFrame({
    "Installment":["1st","2nd","3rd","4th"],
    "Disbursed":[sp1,sp2,sp3,sp4]
})

st.plotly_chart(
    px.bar(
        sp_df,
        x="Installment",
        y="Disbursed",
        title="SPHF Installment Disbursement"
    ),
    use_container_width=True
)


# =========================
# INSTALLMENT SUMMARY
# =========================

st.subheader("Installment Wise Withdrawal Summary")

inst_df = pd.DataFrame({
    "Installment": ["1st", "2nd", "3rd", "4th"],
    "Done": [d1, d2, d3, d4],
    "Pending": [p1, p2, p3, p4]
})

st.dataframe(inst_df, use_container_width=True)

fig1 = px.bar(
    inst_df,
    x="Installment",
    y=["Done", "Pending"],
    barmode="group",
    title="Installment Wise Done vs Pending"
)

st.plotly_chart(fig1, use_container_width=True)


# =========================
# BANK WISE INSTALLMENT REPORT
# =========================

st.subheader("🏦 Bank Wise Installment Withdrawal Report")

bank_rows = []

for bank, g in df.groupby(BANK):

    d1 = yes_count(g[WD1])
    p1 = (is_yes(g[SPHF1]) & ~is_yes(g[WD1])).sum()

    d2 = yes_count(g[WD2])
    p2 = (is_yes(g[SPHF2]) & ~is_yes(g[WD2])).sum()

    d3 = yes_count(g[WD3])
    p3 = (is_yes(g[SPHF3]) & ~is_yes(g[WD3])).sum()

    d4 = yes_count(g[WD4])
    p4 = (is_yes(g[SPHF4]) & ~is_yes(g[WD4])).sum()

    bank_rows.append({

        "Bank": bank,

        "1st Done": d1,
        "1st Pending": p1,

        "2nd Done": d2,
        "2nd Pending": p2,

        "3rd Done": d3,
        "3rd Pending": p3,

        "4th Done": d4,
        "4th Pending": p4,

        "Total Done": d1+d2+d3+d4,
        "Total Pending": p1+p2+p3+p4
    })

bank_detail_df = pd.DataFrame(bank_rows)

st.dataframe(
    bank_detail_df,
    use_container_width=True
)

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

st.subheader("⏳ Bank Wise Withdrawal Pending")

pending_rows = []

for bank, g in df.groupby(BANK):

    p1 = (is_yes(g[SPHF1]) & ~is_yes(g[WD1])).sum()

    p2 = (is_yes(g[SPHF2]) & ~is_yes(g[WD2])).sum()

    p3 = (is_yes(g[SPHF3]) & ~is_yes(g[WD3])).sum()

    p4 = (is_yes(g[SPHF4]) & ~is_yes(g[WD4])).sum()

    pending_rows.append({

        "Bank": bank,

        "1st Pending": p1,
        "2nd Pending": p2,
        "3rd Pending": p3,
        "4th Pending": p4,

        "Total Pending": p1 + p2 + p3 + p4

    })

bank_pending_df = pd.DataFrame(pending_rows)

st.dataframe(
    bank_pending_df,
    use_container_width=True
)

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

st.subheader("✅ District Wise Verification Done")

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

st.dataframe(
    dist_done_df,
    use_container_width=True
)

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

st.subheader("⏳ District Wise Verification Pending")

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

st.dataframe(
    dist_pending_df,
    use_container_width=True
)

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

st.subheader("📥 Download Pending Withdrawal Beneficiary List")

selected_bank = st.selectbox(
    "🏦 Select Bank",
    sorted(df[BANK].dropna().unique())
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
    "Gender",
    "CNIC No.",
    "District",
    "Tehsil",
    "UC",
    "Village",
    "Account No.",
    "Bank"
]

pending_download = pending_df[download_cols]

pdf_file = create_pending_pdf(
    pending_download,
    selected_bank,
    installment
)

st.download_button(
    label="📄 Download PDF Report",
    data=pdf_file,
    file_name=f"{selected_bank}_{installment}_Pending_List.pdf",
    mime="application/pdf"
)


# =========================
# STAGE VERIFICATION PENDING DOWNLOAD
# =========================

st.subheader("🏗 Stage Verification Pending Download")

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
    ["All"] + sorted(df[BANK].dropna().unique().tolist())
)

district_option = st.selectbox(
    "📍 Select District",
    ["All"] + sorted(df[DISTRICT].dropna().unique().tolist())
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
    "Village",
    "Account No.",
    "Bank",
    "Remarks"
]

stage_download = stage_df[download_cols].copy()

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

st.subheader("📝 AH Remarks Cases")

remarks_df = df[
    df[REMARKS]
    .fillna("")
    .astype(str)
    .str.strip()
    != ""
]


# =========================
# SEARCH
# =========================

st.subheader("Search by UUID / CNIC")

search = st.text_input(
    "Enter UUID or CNIC"
)

if search:

    result = df[
        df.astype(str)
        .apply(
            lambda col: col.str.contains(
                search,
                case=False,
                na=False
            )
        )
        .any(axis=1)
    ]

    st.dataframe(
        result,
        use_container_width=True
    )

# =========================
# PROJECT STAFF
# =========================

st.subheader("👥 NRSP Project Staff")

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
                border-radius:15px;
                padding:15px;
                text-align:center;
                box-shadow:0px 2px 10px rgba(0,0,0,0.08);
                margin-bottom:20px;
                background-color:white;
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
            except:
                pass

        st.markdown(
            f"""
            <h4 style="color:#006400;">
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
        opacity:0.6;
        padding-top:20px;
        padding-bottom:10px;
    ">
        Designed & Developed by Waseem Baloch
    </div>
    """,
    unsafe_allow_html=True
)
