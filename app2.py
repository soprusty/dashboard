import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Customer Demand & Fulfillment Analytics",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* ── GLOBAL ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.stApp {
    background: #f4f6f9;
}
.block-container {
    padding: 2rem 2.5rem 3rem 2.5rem !important;
    max-width: 1400px !important;
}

/* ── HEADER ── */
.dash-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 0 2rem 0;
    border-bottom: 1px solid #e0e5ef;
    margin-bottom: 2rem;
}
.dash-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: #0f1c35;
    letter-spacing: -0.3px;
}
.dash-title span {
    color: #2563eb;
}
.dash-subtitle {
    font-size: 0.82rem;
    color: #7a8aaa;
    margin-top: 3px;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.dash-badge {
    background: #eef3ff;
    border: 1px solid #c7d7fd;
    border-radius: 8px;
    padding: 8px 18px;
    font-size: 0.78rem;
    color: #2563eb;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}

/* ── SECTION LABELS ── */
.section-label {
    font-size: 0.72rem;
    font-weight: 600;
    color: #2563eb;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 1rem;
    font-family: 'DM Mono', monospace;
}

/* ── METRIC CARDS ── */
.metric-card {
    background: #ffffff;
    border: 1px solid #e5eaf4;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    height: 130px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 14px 14px 0 0;
}
.metric-card.blue::before   { background: linear-gradient(90deg, #2563eb, #60a5fa); }
.metric-card.teal::before   { background: linear-gradient(90deg, #0d9488, #2dd4bf); }
.metric-card.amber::before  { background: linear-gradient(90deg, #d97706, #fbbf24); }
.metric-card.rose::before   { background: linear-gradient(90deg, #e11d48, #fb7185); }
.metric-card.violet::before { background: linear-gradient(90deg, #7c3aed, #a78bfa); }
.metric-card.indigo::before { background: linear-gradient(90deg, #4338ca, #818cf8); }
.metric-card.green::before  { background: linear-gradient(90deg, #16a34a, #4ade80); }

.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(37,99,235,0.10);
}
.metric-label {
    font-size: 0.75rem;
    font-weight: 500;
    color: #7a8aaa;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.metric-value {
    font-size: 2.4rem;
    font-weight: 700;
    line-height: 1;
    font-family: 'DM Mono', monospace;
    letter-spacing: -1px;
}
.metric-value.blue   { color: #2563eb; }
.metric-value.teal   { color: #0d9488; }
.metric-value.amber  { color: #d97706; }
.metric-value.rose   { color: #e11d48; }
.metric-value.violet { color: #7c3aed; }
.metric-value.indigo { color: #4338ca; }
.metric-value.green  { color: #16a34a; }

.metric-icon {
    font-size: 1.4rem;
    opacity: 0.3;
    position: absolute;
    top: 1.2rem;
    right: 1.4rem;
}

/* ── DIVIDER ── */
.dash-divider {
    border: none;
    border-top: 1px solid #e0e5ef;
    margin: 2rem 0;
}

/* ── TABLES ── */
.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid #e5eaf4 !important;
}
[data-testid="stDataFrame"] > div {
    border-radius: 12px !important;
}

/* ── TABLE WRAPPER ── */
.table-card {
    background: #ffffff;
    border: 1px solid #e5eaf4;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.table-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.table-title::before {
    content: '';
    display: inline-block;
    width: 3px;
    height: 14px;
    background: #2563eb;
    border-radius: 2px;
}

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] {
    background: #ffffff !important;
    border: 1.5px dashed #c7d7fd !important;
    border-radius: 14px !important;
    padding: 1rem !important;
}
[data-testid="stFileUploader"] label {
    color: #7a8aaa !important;
}

/* ── SUCCESS / INFO ALERTS ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border: none !important;
    font-size: 0.82rem !important;
}

/* ── EXPANDER ── */
[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid #e5eaf4 !important;
    border-radius: 12px !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #f4f6f9; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

/* ── PERIOD TAG ── */
.period-tag {
    display: inline-block;
    background: #eef3ff;
    border: 1px solid #c7d7fd;
    color: #2563eb;
    font-size: 0.72rem;
    font-family: 'DM Mono', monospace;
    padding: 2px 10px;
    border-radius: 20px;
    letter-spacing: 0.5px;
    margin-left: 8px;
    vertical-align: middle;
}

/* ── URGENT BADGE ── */
.urgent-note {
    font-size: 0.72rem;
    color: #e11d48;
    margin-top: 6px;
    font-family: 'DM Mono', monospace;
}
</style>
""", unsafe_allow_html=True)


# ── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="dash-header">
  <div>
    
    <div class="dash-title">Customer Demand & Fulfillment Analytics</span></div>
    
  </div>
  <div class="dash-badge">⬤ &nbsp;Live Dashboard</div>
</div>
""", unsafe_allow_html=True)

# ── FILE UPLOADER ────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader("Upload Resource Extract (Excel)", type=['xlsx', 'xls'])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()

        df['Role Start Date']    = pd.to_datetime(df['Start Week'],    errors='coerce')
        df['Demand Raised Date'] = pd.to_datetime(df['Created Date'],  errors='coerce')

        current_period   = df['Period'].max()
        open_df          = df[df['Role Status'].astype(str).str.lower() == 'open']
        current_period_df = df[df['Period'] == current_period]

        st.markdown(f"""
        <div style="margin:0.5rem 0 2rem 0; font-size:0.82rem; color:#5a6a85;">
            Analysis complete &nbsp;·&nbsp; Active period: 
            <span class="period-tag">{current_period}</span>
        </div>
        """, unsafe_allow_html=True)

        # ── ROW 1 — DEMAND SUMMARY ────────────────────────────────────────
        st.markdown('<div class="section-label">Demand Summary</div>', unsafe_allow_html=True)
        r1c1, r1c2, r1c3 = st.columns(3)

        total_open   = len(open_df)
        total_gaps   = int(current_period_df['Gap'].sum())
        global_count = len(open_df[open_df['Global(Y/N)'].astype(str).str.lower() == 'y'])

        with r1c1:
            st.markdown(f"""
            <div class="metric-card blue">
                <div class="metric-icon">📋</div>
                <div class="metric-label">Total Open Demands</div>
                <div class="metric-value blue">{total_open}</div>
            </div>""", unsafe_allow_html=True)

        with r1c2:
            st.markdown(f"""
            <div class="metric-card rose">
                <div class="metric-icon">⚠️</div>
                <div class="metric-label">Gaps — {current_period}</div>
                <div class="metric-value rose">{total_gaps}</div>
            </div>""", unsafe_allow_html=True)

        with r1c3:
            st.markdown(f"""
            <div class="metric-card teal">
                <div class="metric-icon">🌐</div>
                <div class="metric-label">Open Roles (Global = Y)</div>
                <div class="metric-value teal">{global_count}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='margin:1.2rem 0'></div>", unsafe_allow_html=True)

        # ── ROW 2 — OPERATIONAL DETAIL ────────────────────────────────────
        st.markdown('<div class="section-label">Operational Detail</div>', unsafe_allow_html=True)
        r2c1, r2c2, r2c3, r2c4 = st.columns(4)

        otm_no  = len(open_df[open_df['OTM'].astype(str).str.lower() == 'no'])
        otm_yes = len(open_df[open_df['OTM'].astype(str).str.lower() == 'yes'])
        new_demands = len(current_period_df[
            current_period_df['New/Backfill'].astype(str).str.lower() == 'new'])
        urgent_new = len(current_period_df[
            (current_period_df['New/Backfill'].astype(str).str.lower() == 'new') &
            ((current_period_df['Start Week'] - current_period_df['Created Date']).dt.days <= 56)
        ])

        with r2c1:
            st.markdown(f"""
            <div class="metric-card amber">
                <div class="metric-icon">🔴</div>
                <div class="metric-label">Open Demands (OTM No)</div>
                <div class="metric-value amber">{otm_no}</div>
            </div>""", unsafe_allow_html=True)

        with r2c2:
            st.markdown(f"""
            <div class="metric-card green">
                <div class="metric-icon">🟢</div>
                <div class="metric-label">Open Demands (OTM Yes)</div>
                <div class="metric-value green">{otm_yes}</div>
            </div>""", unsafe_allow_html=True)

        with r2c3:
            st.markdown(f"""
            <div class="metric-card indigo">
                <div class="metric-icon">✨</div>
                <div class="metric-label">New Demands — {current_period}</div>
                <div class="metric-value indigo">{new_demands}</div>
            </div>""", unsafe_allow_html=True)

        with r2c4:
            st.markdown(f"""
            <div class="metric-card violet">
                <div class="metric-icon">🚨</div>
                <div class="metric-label">Urgent New (≤ 8 Weeks)</div>
                <div class="metric-value violet">{urgent_new}</div>
                <div class="urgent-note">⚡ Start date within 56 days</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)

        # ── ROW 3 — SKILL GAP ANALYSIS ────────────────────────────────────
        st.markdown('<div class="section-label">Skill Gap Analysis</div>', unsafe_allow_html=True)
        skill_gap_df = df[df['Gap'] == 1]

        if not skill_gap_df.empty:
            top_skills_gap = skill_gap_df['Request Key Skill'].value_counts().head(5).reset_index()
            top_skills_gap.columns = ['Mandatory Skill', 'Total Gap Count']
            top_skills_gap.index = top_skills_gap.index + 1

            st.markdown('<div class="table-card"><div class="table-title">Top 5 Mandatory Skill Gaps (Gap = 1)</div>', unsafe_allow_html=True)
            st.dataframe(
                top_skills_gap,
                hide_index=False,
                use_container_width=True,
                height=220,
                column_config={
                    "Mandatory Skill": st.column_config.TextColumn("Mandatory Skill", width="large"),
                    "Total Gap Count": st.column_config.ProgressColumn(
                        "Total Gap Count",
                        format="%d",
                        min_value=0,
                        max_value=int(top_skills_gap['Total Gap Count'].max()),
                    ),
                }
            )
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No records found with a Gap of 1.")

        st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)

        # ── ROW 4 — CLIENT & STATUS TABLES ───────────────────────────────
        st.markdown('<div class="section-label">Breakdown</div>', unsafe_allow_html=True)
        t_col1, t_col2 = st.columns(2)

        top_clients_data = open_df['Client'].value_counts().head(5).reset_index()
        top_clients_data.columns = ['Client Name', 'Open Demand Count']
        top_clients_data.index = top_clients_data.index + 1

        status_breakup = open_df['Project Status'].value_counts().reset_index()
        status_breakup.columns = ['Status Name', 'Total Count']
        status_breakup.index = status_breakup.index + 1

        with t_col1:
            st.markdown('<div class="table-card"><div class="table-title">Top 5 Client Accounts — Highest Open Demand</div>', unsafe_allow_html=True)
            st.dataframe(
                top_clients_data,
                hide_index=False,
                use_container_width=True,
                height=220,
                column_config={
                    "Client Name": st.column_config.TextColumn("Client Name", width="large"),
                    "Open Demand Count": st.column_config.ProgressColumn(
                        "Open Demand Count",
                        format="%d",
                        min_value=0,
                        max_value=int(top_clients_data['Open Demand Count'].max()),
                    ),
                }
            )
            st.markdown('</div>', unsafe_allow_html=True)

        with t_col2:
            st.markdown('<div class="table-card"><div class="table-title">Open Demand Breakup — Project Status</div>', unsafe_allow_html=True)
            st.dataframe(
                status_breakup,
                hide_index=False,
                use_container_width=True,
                height=220,
                column_config={
                    "Status Name": st.column_config.TextColumn("Status", width="large"),
                    "Total Count": st.column_config.ProgressColumn(
                        "Total Count",
                        format="%d",
                        min_value=0,
                        max_value=int(status_breakup['Total Count'].max()),
                    ),
                }
            )
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)

        # ── EXPANDER ─────────────────────────────────────────────────────
        with st.expander("🔎  View All Open Demand Records"):
            st.dataframe(open_df, use_container_width=True)

    except Exception as e:
        st.error(f"Error processing file: {e}")
        st.info("Verify that your Excel column names match exactly: Start Week, Created Date, Period, Role Status, Gap, Global(Y/N), OTM, New/Backfill, Request Key Skill, Client, Project Status")

else:
    # ── EMPTY STATE ──────────────────────────────────────────────────────
    st.markdown("""
    <div style="
        text-align: center;
        padding: 5rem 2rem;
        background: #ffffff;
        border: 1.5px dashed #c7d7fd;
        border-radius: 18px;
        margin-top: 1rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    ">
        <div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.4;">📂</div>
        <div style="font-size: 1rem; font-weight: 600; color: #1e293b; margin-bottom: 0.5rem;">
            No data loaded
        </div>
        <div style="font-size: 0.82rem; color: #7a8aaa;">
            Upload your resource extract Excel file above to populate the dashboard
        </div>
    </div>
    """, unsafe_allow_html=True)
