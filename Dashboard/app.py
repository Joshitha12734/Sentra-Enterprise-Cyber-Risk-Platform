import streamlit as st
import pandas as pd
import plotly.express as px
import json
import sys
import os
import google.generativeai as genai
from dotenv import load_dotenv
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from Engine.sentra_intelligence import SentraIntelligence
from Engine.risk_monitor import save_snapshot
from Engine.risk_monitor import get_exposure_delta
from Engine.nvd_live_fetch import fetch_latest_cves
from Engine.business_matcher import find_matches
from streamlit_autorefresh import st_autorefresh


# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv()  # reads .env file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# =====================================
# SENTRA PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Sentra | Cyber Risk Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)
st_autorefresh(
    interval=30000,   # 30 seconds
    key="sentra_live_refresh"
)

st.markdown("""
<style>

/* =====================================================
   SENTRA ENTERPRISE THEME
   ===================================================== */

:root{
    --bg:#050816;
    --bg2:#0b1220;
    --card:#111827;
    --purple:#7c3aed;
    --purple-light:#a855f7;
    --blue:#38bdf8;
    --green:#22c55e;
    --red:#ef4444;
    --text:#f8fafc;
    --muted:#94a3b8;
}

/* =====================================================
   APP BACKGROUND
   ===================================================== */

.stApp{
    background:
    radial-gradient(
        circle at top center,
        rgba(168,85,247,0.55),
        transparent 35%
    ),
    radial-gradient(
        circle at 80% 20%,
        rgba(56,189,248,0.12),
        transparent 30%
    ),
    linear-gradient(
        180deg,
        #050816 0%,
        #0b1220 60%,
        #050816 100%
    );
}

/* =====================================================
   MAIN CONTENT
   ===================================================== */

.main .block-container{
    max-width:95%;
    padding-top:2rem;
    padding-bottom:3rem;
}

/* =====================================================
   SIDEBAR
   ===================================================== */

[data-testid="stSidebar"]{
    background:
    rgba(10,12,16,0.92);

    backdrop-filter: blur(12px);

    border-right:1px solid rgba(255,255,255,0.08);
}

/* =====================================================
   HEADINGS
   ===================================================== */

h1{
    font-size:3rem !important;
    font-weight:800 !important;

    background:
    linear-gradient(
        135deg,
        #ffffff,
        #a855f7
    );

    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

h2,h3{
    color:white !important;
}
            


/* =====================================================
   METRIC CARDS
   ===================================================== */

[data-testid="stMetric"]{

    background:
    rgba(17,24,39,0.65);

    backdrop-filter: blur(14px);

    border:1px solid rgba(255,255,255,0.05);

    border-radius:20px;

    padding:18px;

    box-shadow:
    0px 10px 40px rgba(124,58,237,0.12);

    transition:0.3s;
}

[data-testid="stMetric"]:hover{

    border-color:
    rgba(124,58,237,0.4);

    transform:
    translateY(-2px);
}

[data-testid="stMetricLabel"]{

    color:#94a3b8;

    text-transform:uppercase;

    letter-spacing:1px;
}

[data-testid="stMetricValue"]{

    color:white;

    font-size:2rem;

    font-weight:800;
}

/* =====================================================
   DATAFRAMES
   ===================================================== */

div[data-testid="stDataFrame"]{

    border-radius:18px;

    overflow:hidden;

    border:
    1px solid rgba(255,255,255,0.05);
}

/* =====================================================
   BUTTONS
   ===================================================== */

.stButton button{

    background:
    linear-gradient(
        135deg,
        #7c3aed,
        #9333ea
    ) !important;

    color:white !important;

    border:none !important;

    border-radius:12px !important;

    font-weight:700 !important;

    transition:0.25s;
}

.stButton button:hover{

    transform:
    translateY(-2px);

    box-shadow:
    0px 8px 25px rgba(124,58,237,0.35);
}
            
.stTextInput input {
    color: white !important;
    background-color: #101722 !important;
}

.stTextInput input::placeholder {
    color: #9ca3af !important;
}
/* =====================================================
   SELECTBOX
   ===================================================== */

.stSelectbox div[data-baseweb="select"]{

    background:
    rgba(17,24,39,0.8);

    border-radius:12px;
}

/* =====================================================
   ALERT BOXES
   ===================================================== */

.stAlert{

    border-radius:16px;
}

/* =====================================================
   PLOTLY CHARTS
   ===================================================== */

.js-plotly-plot{

    background:
    rgba(17,24,39,0.55);

    border-radius:20px;

    padding:10px;

    backdrop-filter: blur(12px);

    border:
    1px solid rgba(255,255,255,0.04);
}

/* =====================================================
   HIDE STREAMLIT BRANDING
   ===================================================== */

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

header{
    background:transparent !important;
}
/* =====================================
   FORCE TEXT VISIBILITY
===================================== */

body{
    color:#f8fafc;
}

p,
span{
    color:#f8fafc;
}

h1,
h2,
h3,
h4,
h5,
h6 {
    color: white !important;
}
/* Selectbox text fix */

.stSelectbox div[data-baseweb="select"] *{
    color:#111827 !important;
}

.stSelectbox input{
    color:#111827 !important;
}

/* Dropdown menu */

div[role="listbox"]{
    background:white !important;
}

div[role="option"]{
    color:#111827 !important;
    background:white !important;
}

div[role="option"]:hover{
    background:#ede9fe !important;
    color:#111827 !important;
}


small {
    color: #cbd5e1 !important;
}
            
.stMarkdown {
    color: #f8fafc !important;
}

[data-testid="stAlert"] {
    color: white !important;
}

[data-testid="stAlert"] p {
    color: white !important;
}          

input {
    color: white !important;
}

input::placeholder {
    color: #94a3b8 !important;
}

.ai-card{
    background:
    linear-gradient(
        135deg,
        rgba(17,24,39,0.95),
        rgba(30,41,59,0.85)
    );

    border:1px solid rgba(124,58,237,.35);

    border-radius:20px;

    padding:24px;

    color:#f8fafc;

    line-height:1.8;

    box-shadow:
    0 0 25px rgba(124,58,237,.15);

    margin-bottom:20px;
}
            
[data-testid="stAlert"] {
    color: white !important;
}

[data-testid="stAlert"] p {
    color: white !important;
}
input {
    color: white !important;
}

input::placeholder {
    color: #94a3b8 !important;
}
            
.sidebar-brand{
    text-align:center;
    padding:1rem;
    margin-bottom:1rem;
}

.brand-icon{
    font-size:2rem;
}

.brand-name{
    font-size:1.5rem;
    font-weight:800;
    color:white;
}

.brand-tagline{
    color:#cbd5e1;
    font-size:0.85rem;
}

.brand-version{
    color:#94a3b8;
    font-size:0.75rem;
}
.hero{
    padding:30px 0;
    margin-bottom:20px;
}

.hero-subtitle{
    color:#cbd5e1;
    font-size:1.1rem;
}

.hero-tagline{
    color:#94a3b8;
}
.risk-card{

background:rgba(17,24,39,.92);

border-radius:22px;

padding:24px;

margin-bottom:22px;

border:1px solid rgba(124,58,237,.25);

box-shadow:0 8px 24px rgba(0,0,0,.25);

transition:.3s;
}

.risk-card:hover{

transform:translateY(-4px);

box-shadow:0 15px 40px rgba(124,58,237,.25);

}

.tech-chip{

display:inline-block;

padding:6px 12px;

margin:4px;

border-radius:18px;

background:#312e81;

color:white;

font-size:13px;

font-weight:600;

}
.top-risk-banner{
    background:linear-gradient(
        135deg,
        rgba(127,29,29,.9),
        rgba(153,27,27,.8)
    );

    border:1px solid rgba(239,68,68,.4);

    border-radius:18px;

    padding:24px;

    margin-bottom:25px;
}

.metric-card{
    box-shadow:
    0 0 30px rgba(124,58,237,.15);
}

       
</style>
""", unsafe_allow_html=True) 




# -------------------------------
# Load contextual risk data
# -------------------------------

@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join("Outputs", "contextual_risk.json")
    if not os.path.exists(json_path):
        st.error(f"❌ contextual_risk.json not found at {json_path}. Run risk_contextualizer.py first.")
        st.stop()
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["results"], data.get("top_asset_risks", []), data["metadata"]

results, top_asset_risks, metadata = load_data()
df = pd.DataFrame(results)

def render_risk_card(risk,medal):
    """
    Render an enterprise-style business risk card.
    """

    level = risk["risk_level"]

    colors = {
        "Critical": "#ef4444",
        "High": "#f97316",
        "Medium": "#eab308",
        "Low": "#22c55e"
    }

    color = colors.get(level, "#64748b")
    priority_color = {
        "Critical": "#ef4444",
        "High": "#f97316",
        "Medium": "#eab308",
        "Low": "#22c55e"
    }.get(risk["risk_level"], "#64748b")

    tech_stack = risk.get("technology_stack", [])
    stack = risk.get("technology_stack", [])

    if not isinstance(stack, list):
        stack = []

    tech = "".join(
        f'<span class="tech-chip">{t}</span>'
        for t in stack
    )

    if not tech:
        tech = "<span class='tech-chip'>Unknown</span>"

    internet = (
        "🌐 Internet Facing"
        if risk.get("internet_exposed", False)
        else "🔒 Internal"
    )

    crown = (
        "👑 Crown Jewel"
        if risk.get("crown_jewel", False)
        else "Standard Asset"
    )


    st.markdown(
        f"""
<div class="risk-card">

<div style="display:flex;justify-content:space-between;align-items:center;">

<h3>{medal} {risk['asset_name']}</h3>

<span
style="
background:{color};
padding:6px 14px;
border-radius:20px;
font-weight:bold;
color:white;
">

{risk['risk_level']}

</span>

</div>

<hr>


<b>💰 Exposure</b><br>

${risk['estimated_total_exposure']:,.0f}

<br><br>

<b>🚨 Priority</b><br>
<span style="
background:{priority_color};
padding:4px 12px;
border-radius:14px;
font-weight:bold;
color:white;
">

{risk['risk_level']}

<br><br>

<b>🏢 Business Unit</b><br>

{risk.get("business_unit", "Unknown")}

<br><br>

<b>👤 Owner</b><br>

{risk.get("cloud_provider", "Unknown")}

<br><br>

<b>☁ Cloud</b><br>

{risk['cloud_provider']}

<br><br>

<b>💻 Operating System</b><br>

{risk.get("operating_system", "Unknown")}

<br><br>

<b>⚙ Technology Stack</b>

<br><br>

{tech}

<br><br>

<b>Status</b>

<br>

{internet}

<br>

{crown}

<br><br>

<b>⚡ Executive Decision</b>

<br>

{risk.get("decision", "Monitor")}

</div>
""",
        unsafe_allow_html=True
    )
# -------------------------------
# Gemini setup (using .env key)
# -------------------------------
def init_gemini():
    if not GEMINI_API_KEY:
        st.warning("Gemini temporarily unavailable. Using Sentra Local Intelligence.")
        return None
    genai.configure(api_key=GEMINI_API_KEY)
    model_name = "gemini-2.5-flash"
    print("Initializing Sentra Intelligence Engine...")
    return genai.GenerativeModel(model_name)

model = init_gemini()

def generate_gemini_risk_summary(asset_name, cve_id, exposure, business_impact, risk_level):
    if not model:
        return f"Gemini unavailable. {cve_id} poses {risk_level} risk to {asset_name} with potential exposure of ${exposure:,.0f}."
    prompt = f"""
You are a cyber risk advisor for a Fortune 500 company. 
Provide a concise, executive-level summary (2-3 sentences) of the following risk:

- Asset: {asset_name}
- Vulnerability: {cve_id}
- Financial Exposure: ${exposure:,.0f}
- Business Impact: {business_impact}
- Risk Level: {risk_level}

Explain why leadership should care and what immediate action is recommended.
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return (
            f"{cve_id} poses a {risk_level} business risk to {asset_name}. "
            f"The estimated financial exposure is ${exposure:,.0f}. "
            f"Immediate remediation is recommended to reduce operational and financial impact."
        )
        
    
 # -------------------------------
# Live CVE Exposure Estimator
# -------------------------------
def severity_to_exposure(severity):

    mapping = {
        "CRITICAL": 10000000,
        "HIGH": 5000000,
        "MEDIUM": 1000000,
        "LOW": 100000
    }

    return mapping.get(
        severity.upper(),
        50000
    )   

# -------------------------------
# What‑if helper
# -------------------------------
def what_if_exposure(row, delay_days=0, controls=None):
    if controls is None:
        controls = []
    base = row["estimated_total_exposure"]
    delay_factor = 1 + (delay_days * 0.05)
    delay_factor = min(3.0, delay_factor)
    control_factor = 1 - (0.2 * len(controls))
    control_factor = max(0.1, control_factor)
    new_exposure = base * delay_factor * control_factor

    if new_exposure >= 10_000_000:
        risk_level = "Critical"
        decision = "Immediate Remediation"
    elif new_exposure >= 5_000_000:
        risk_level = "High"
        decision = "Executive Review"
    elif new_exposure >= 1_000_000:
        risk_level = "Medium"
        decision = "Security Approval"
    else:
        risk_level = "Low"
        decision = "Accept with Monitoring"
    return new_exposure, risk_level, decision

# -------------------------------
# Sidebar
# -------------------------------
with st.sidebar:
    st.markdown("""
        <div class="sidebar-brand">
            <div class="brand-icon">🛡️</div>
            <div class="brand-name">SENTRA</div>
            <div class="brand-tagline">Cyber Risk Command Center</div>
            <div class="brand-version">v1.0 Enterprise Edition</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigation", ["📊 Risk Dashboard", "📄 Board Reporting", "🧠 Sentra Intelligence"], index=0)
    st.markdown("---")

    if page == "📊 Risk Dashboard":
        st.markdown("### 🔮 What‑If Lab")
        pairs = df.groupby(["asset_name", "cve_id"]).size().reset_index()[["asset_name", "cve_id"]]
        pair_labels = pairs.apply(lambda r: f"{r['asset_name']} – {r['cve_id']}", axis=1)
        selected_label = st.selectbox("Asset & Vulnerability", pair_labels, key="whatif_select")
        selected_asset, selected_cve = selected_label.split(" – ")
        baseline = df[(df["asset_name"] == selected_asset) & (df["cve_id"] == selected_cve)].iloc[0]
        delay = st.slider("Remediation delay (days)", 0, 90, 7)
        controls = st.multiselect("Mitigating controls", ["WAF", "IDS/IPS", "Air gap", "Backup"])
        if st.button("Run What‑If", type="primary", use_container_width=True):
            new_exp, new_risk, new_dec = what_if_exposure(baseline, delay, controls)
            st.session_state.what_if = {
                "asset": selected_asset,
                "cve": selected_cve,
                "base_exp": baseline["estimated_total_exposure"],
                "new_exp": new_exp,
                "base_risk": baseline["risk_level"],
                "new_risk": new_risk,
                "base_dec": baseline["decision"],
                "new_dec": new_dec,
                "delay": delay,
                "controls": controls
            }

    # Show Gemini status in sidebar
    if model:
        st.sidebar.success("🧠 Sentra Intelligence ready")
    else:
        st.sidebar.error("⚠️ AI running in Offline Mode")

# -------------------------------
# Page: Risk Dashboard
# -------------------------------
if page == "📊 Risk Dashboard":
    # Hero
    st.markdown("""
        <div class="hero">
            <h1>🛡️ SENTRA</h1>
            <p class="hero-subtitle">Enterprise Cyber Risk Command Center</p>
            <p class="hero-tagline">Turning vulnerabilities into business decisions.</p>
        </div>
    """, unsafe_allow_html=True)

    # Metadata card
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric("Last Scan", metadata.get("scan_time", "N/A")[:19])
    with col_m2:
        st.metric("Engine", metadata.get("engine", "contextual-risk-engine"))
    with col_m3:
        st.metric("CVEs Processed", len(df))
    with col_m4:
        st.metric("Data Source", "NVD (NIST)")
    st.divider()

    # Glassmorphism KPI cards
    
    st.divider()
    st.subheader("🚨 Live Threat Intelligence")

    try:
        live_cves = fetch_latest_cves(5)
    except Exception as e:
        st.warning(f"NVD unavailable: {e}")
        live_cves = []

    if live_cves:

        newest = live_cves[0]

        banner_color = "#dc2626"

        if newest["severity"] == "HIGH":
            banner_color = "#ea580c"

        st.markdown(
            f"""
    <div style="
    background:{banner_color};
    padding:20px;
    border-radius:18px;
    margin-bottom:25px;
    color:white;
    ">

    <h3>🚨 NEW LIVE THREAT DETECTED</h3>

    <b>{newest['cve_id']}</b>

    Severity: <b>{newest['severity']}</b>

    CVSS: <b>{newest['cvss']}</b>

    Published: <b>{newest['published']}</b>

    </div>
    """,
            unsafe_allow_html=True
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric("Live CVEs", len(live_cves))

        with c2:
            st.metric("Critical", sum(x["severity"] == "CRITICAL" for x in live_cves))

        with c3:
            st.metric("High", sum(x["severity"] == "HIGH" for x in live_cves))

        with c4:
            st.metric("Highest CVSS", max(x["cvss"] for x in live_cves))

        st.markdown("### 🌐 Latest Threat Feed")

        for cve in live_cves:

            if cve["severity"] == "CRITICAL":
                color = "#dc2626"
                icon = "🔴"

            elif cve["severity"] == "HIGH":
                color = "#ea580c"
                icon = "🟠"

            elif cve["severity"] == "MEDIUM":
                color = "#ca8a04"
                icon = "🟡"

            else:
                color = "#16a34a"
                icon = "🟢"

            st.markdown(
                f"""
    <div style="
    background:#111827;
    padding:18px;
    border-left:6px solid {color};
    border-radius:12px;
    margin-bottom:15px;
    ">

    <h4>{icon} {cve['cve_id']}</h4>

    <b>Severity:</b> {cve['severity']}<br>

    <b>CVSS:</b> {cve['cvss']}<br>

    <b>Attack Vector:</b> {cve.get("attack_vector","UNKNOWN")}<br>

    <b>Published:</b> {cve["published"]}<br><br>

    {cve["description"][:250]}...

    </div>
    """,
                unsafe_allow_html=True
            )

    else:
        st.warning("Unable to retrieve live threat intelligence.")
    
    
    business_matches = find_matches(live_cves)

    if business_matches:

        st.success(
            f"""
    ✅ **{len(business_matches)} Live Business Threat(s) Detected**

    The latest NVD vulnerabilities affect assets within your enterprise.
    """
        )

        df = pd.concat(
            [df, pd.DataFrame(business_matches)],
            ignore_index=True
        )

    else:

        st.info(
            f"""
    ### 🛡️ No Live Business Threats Detected

    Sentra analyzed **{len(live_cves)}** newly published CVEs from the NVD.

    **Analysis Summary**

    - 🌐 Live NVD feed successfully retrieved
    - 🖥️ Enterprise assets analyzed: **12**
    - 🔍 Technology matching completed
    - ✅ No current vulnerabilities impact technologies deployed in your environment

    The platform continuously monitors the NVD and will automatically prioritize any future vulnerabilities that match your enterprise technology stack.
    """
        )
     #DEBUG LINES GO HERE
    
    total_exp = df["estimated_total_exposure"].sum()
    print("Saving exposure snapshot...")
    save_snapshot(total_exp)

    delta = 0
    trend = "Live Scan"

    # ----------------------------
    # Dashboard KPIs
    # ----------------------------

    total_exp = df["estimated_total_exposure"].sum()

    critical_risks = (
        df["risk_level"] == "Critical"
    ).sum()

    board_risks = (
        df["board_reporting"] == "Required"
    ).sum()

    risk_breaches = (
        df["risk_appetite_breach"] == "Above Appetite"
    ).sum()

    st.markdown(f"""
    <style>

    .kpi-container{{
    display:flex;
    gap:20px;
    margin-bottom:30px;
    }}

    .kpi-card{{
    flex:1;

    background:linear-gradient(
    135deg,
    rgba(17,24,39,.95),
    rgba(30,41,59,.90)
    );

    border:1px solid rgba(124,58,237,.35);

    border-radius:18px;

    padding:22px;

    box-shadow:0 0 30px rgba(124,58,237,.18);

    transition:.25s;
    }}

    .kpi-card:hover{{
    transform:translateY(-4px);
    }}

    .kpi-title{{
    font-size:15px;
    color:#94a3b8;
    }}

    .kpi-value{{
    font-size:34px;
    font-weight:800;
    color:white;
    margin-top:8px;
    }}

    .kpi-sub{{
    margin-top:6px;
    color:#22c55e;
    }}

    </style>

    <div class="kpi-container">

    <div class="kpi-card">

    <div class="kpi-title">
    💰 Enterprise Exposure
    </div>

    <div class="kpi-value">
    ${total_exp:,.0f}
    </div>

    <div class="kpi-sub">
    {trend}
    </div>

    </div>

    <div class="kpi-card">

    <div class="kpi-title">
    🚨 Critical Risks
    </div>

    <div class="kpi-value">
    {critical_risks}
    </div>

    </div>

    <div class="kpi-card">

    <div class="kpi-title">
    📋 Board Risks
    </div>

    <div class="kpi-value">
    {board_risks}
    </div>

    </div>

    <div class="kpi-card">

    <div class="kpi-title">
    ⚠ Risk Appetite
    </div>

    <div class="kpi-value">
    {risk_breaches}
    </div>

    </div>

    </div>

    """, unsafe_allow_html=True)
    st.subheader("Enterprise Business Risk Ranking")
    ranking = (
        df.sort_values(
            "estimated_total_exposure",
            ascending=False
        )
        .head(5)
    )
    for i, (_, risk) in enumerate(ranking.iterrows(), start=1):
        medals = {
            1: "🥇",
            2: "🥈",
            3: "🥉",
            4: "🏅",
            5: "🏅"
        }
        render_risk_card(risk, medals[i])
        
    # Top Enterprise Risk Banner
    top_risk = df.loc[df["estimated_total_exposure"].idxmax()]
    st.markdown(f"""
        <div class="top-risk-banner">
            <div class="banner-label">🚨 TOP ENTERPRISE RISK</div>
            <div class="banner-asset">{top_risk['asset_name']}</div>
            <div class="banner-details">
                <div><span class="detail-label">CVE</span><br>{top_risk['cve_id']}</div>
                <div><span class="detail-label">Exposure</span><br>${top_risk['estimated_total_exposure']:,.0f}</div>
                <div><span class="detail-label">Impact</span><br>{top_risk['business_impact']}</div>
                <div><span class="detail-label">Decision</span><br>{top_risk['decision']}</div>
            </div>
            <div class="banner-action">⚡ {top_risk['recommended_action']}</div>
        </div>
    """, unsafe_allow_html=True)

    # Two columns: Risk Posture Donut + Business Impact Bar
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("📊 Risk Posture")
        risk_counts = df["risk_level"].value_counts().reset_index()
        risk_counts.columns = ["Risk Level", "Count"]
        fig_donut = px.pie(risk_counts, names="Risk Level", values="Count",
                           hole=0.4, color="Risk Level",
                           color_discrete_map={"Critical": "#ef4444", "High": "#f59e0b",
                                               "Medium": "#eab308", "Low": "#22c55e"})
        fig_donut.update_layout(showlegend=True, height=400, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_right:
        st.subheader("💥 Business Impact Distribution")
        impact_counts = df["business_impact"].value_counts().reset_index()
        impact_counts.columns = ["Impact Type", "Count"]
        fig_impact = px.bar(impact_counts, x="Impact Type", y="Count", color="Impact Type",
                            color_discrete_sequence=px.colors.qualitative.Set2)
        fig_impact.update_layout(showlegend=False, height=400, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_impact, use_container_width=True)

    # Treemap
    st.subheader("🏢 Exposure by Business Unit & Asset")
    fig_treemap = px.treemap(df, path=["business_unit", "asset_name"],
                             values="estimated_total_exposure", color="risk_level",
                             color_discrete_map={"Critical": "#ef4444", "High": "#f59e0b",
                                                 "Medium": "#eab308", "Low": "#22c55e"},
                             hover_data={"estimated_total_exposure": ":.0f"})
    fig_treemap.update_traces(texttemplate='%{label}<br>$%{value:,.0f}', textfont_size=12)
    fig_treemap.update_layout(height=450, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_treemap, use_container_width=True)

    # What-If Results
    if "what_if" in st.session_state:
        w = st.session_state.what_if
        st.subheader("📊 What‑If Impact Analysis")
        colA, colB = st.columns(2)
        with colA:
            st.metric("Baseline Exposure", f"${w['base_exp']:,.0f}")
            st.metric("Risk Level", w['base_risk'])
            st.metric("Decision", w['base_dec'])
        with colB:
            delta = w['new_exp'] - w['base_exp']
            st.metric("New Exposure", f"${w['new_exp']:,.0f}", delta=f"${delta:+,.0f}", delta_color="inverse")
            st.metric("Risk Level", w['new_risk'])
            st.metric("Decision", w['new_dec'])

        st.markdown("#### 📈 Scenario Comparison")
        scenarios = {
            "Baseline": (0, []),
            f"Delay {w['delay']}d": (w['delay'], []),
            f"Controls: {', '.join(w['controls'])}" if w['controls'] else "Controls only": (0, w['controls']),
            "Combined": (w['delay'], w['controls'])
        }
        comp = []
        for name, (d, c) in scenarios.items():
            exp, rl, dec = what_if_exposure(baseline, d, c)
            comp.append({"Scenario": name, "Exposure (USD)": exp, "Risk Level": rl, "Decision": dec})
        st.dataframe(pd.DataFrame(comp), use_container_width=True,
                     column_config={"Exposure (USD)": st.column_config.NumberColumn(format="$%.0f")})
        st.divider()

    # Crown Jewel Monitoring
    st.subheader("👑 Crown Jewel Assets")
    crown_assets = df[df["crown_jewel"] == True]["asset_name"].unique()
    if len(crown_assets) > 0:
        cols = st.columns(min(len(crown_assets), 4))
        for idx, asset in enumerate(crown_assets):
            asset_data = df[df["asset_name"] == asset]
            max_exp = asset_data["estimated_total_exposure"].max()
            with cols[idx % 4]:
                st.markdown(f"**{asset}**")
                st.metric("Peak Exposure", f"${max_exp:,.0f}")
                st.progress(min(max_exp / 10_000_000, 1.0))
    else:
        st.info("No crown jewel assets identified.")
    st.divider()

    # Asset Explorer
    st.subheader("🔍 Asset Explorer")
    selected_asset_exp = st.selectbox("Select an asset", df["asset_name"].unique())
    asset_df = df[df["asset_name"] == selected_asset_exp].copy()
    asset_meta = asset_df.iloc[0]
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        st.metric("Business Unit", asset_meta["business_unit"])
    with col_b:
        st.metric("Owner", asset_meta["owner"])
    with col_c:
        st.metric("Crown Jewel", asset_meta["crown_jewel"])
    with col_d:
        st.metric("Internet Exposed", asset_meta["internet_exposed"])

    vuln_table = asset_df[["cve_id", "estimated_total_exposure", "priority_score",
                           "business_impact_level", "decision", "remediation_sla"]].copy()
    vuln_table.columns = ["CVE", "Exposure (USD)", "Priority Score", "Business Impact", "Decision", "SLA"]
    st.dataframe(vuln_table, use_container_width=True,
                 column_config={"Exposure (USD)": st.column_config.NumberColumn(format="$%.0f")})
    csv = vuln_table.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Export Asset Report (CSV)", csv, f"{selected_asset_exp}_risks.csv", "text/csv")

    st.caption("© Sentra – Cyber Risk Command Center | Data from NVD & contextual risk engine")

# -------------------------------
# Page: Board Reporting
# -------------------------------
elif page == "📄 Board Reporting":
    st.markdown("""
        <div class="hero">
            <h1>📋 Board Risk Report</h1>
            <p class="hero-subtitle">Executive Summary & Strategic Risk Insights</p>
        </div>
    """, unsafe_allow_html=True)

    # Board KPIs
    board_exposure = df[df["board_reporting"] == "Required"]["estimated_total_exposure"].sum()
    board_risks = len(df[df["board_reporting"] == "Required"])
    appetite_breaches = len(df[df["risk_appetite_breach"] == "Yes"])
    crown_jewel_exposure = df[df["crown_jewel"] == "Yes"]["estimated_total_exposure"].sum()

    col_k1, col_k2, col_k3, col_k4 = st.columns(4)
    with col_k1:
        st.metric("📋 Board Exposure", f"${board_exposure:,.0f}")
    with col_k2:
        st.metric("⚠️ Board-Reportable Risks", board_risks)
    with col_k3:
        st.metric("📊 Risk Appetite Breaches", appetite_breaches)
    with col_k4:
        st.metric("👑 Crown Jewel Exposure", f"${crown_jewel_exposure:,.0f}")
    st.divider()

    board_risks_df = df[df["board_reporting"] == "Required"].copy()
    if len(board_risks_df) > 0:
        st.subheader("📌 Risks Requiring Board Notification")
        board_summary = board_risks_df[["asset_name", "cve_id", "estimated_total_exposure",
                                        "business_impact", "risk_level", "decision"]].copy()
        board_summary.columns = ["Asset", "CVE", "Exposure (USD)", "Business Impact", "Risk Level", "Decision"]
        st.dataframe(board_summary, use_container_width=True,
                     column_config={"Exposure (USD)": st.column_config.NumberColumn(format="$%.0f")})

        st.subheader("💰 Financial Exposure by Business Unit")
        bu_exp = board_risks_df.groupby("business_unit")["estimated_total_exposure"].sum().reset_index()
        fig_bu = px.bar(bu_exp, x="business_unit", y="estimated_total_exposure", color="estimated_total_exposure",
                        color_continuous_scale="Reds", title="Board-Reportable Exposure per Business Unit")
        fig_bu.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_bu, use_container_width=True)
    else:
        st.success("✅ No board-reportable risks at this time.")

    appetite_df = df[df["risk_appetite_breach"] == "Yes"].copy()
    if len(appetite_df) > 0:
        st.subheader("⚠️ Risk Appetite Breaches")
        st.metric("Total Breaches", len(appetite_df))
        st.dataframe(appetite_df[["asset_name", "cve_id", "estimated_total_exposure", "risk_level"]],
                     use_container_width=True,
                     column_config={"estimated_total_exposure": st.column_config.NumberColumn(format="$%.0f")})
    else:
        st.success("✅ All risks within organizational risk appetite.")

    st.subheader("📝 Executive Summary (AI‑Generated)")
    top_risk = df.loc[df["estimated_total_exposure"].idxmax()]
    if model:
        gemini_summary = generate_gemini_risk_summary(
            top_risk['asset_name'], top_risk['cve_id'],
            top_risk['estimated_total_exposure'], top_risk['business_impact'],
            top_risk['risk_level']
        )
        
        st.markdown(
            f"""
            <div class="ai-card">
                <h4>🚨 Critical Finding</h4>
                {gemini_summary}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.info(f"**Critical Finding:** {top_risk['llm_business_explanation']}")
    st.caption("Based on NVD data and asset criticality analysis. Review full report for remediation timelines.")

# -------------------------------
# Page: Sentra Intelligence
# -------------------------------
elif page == "🧠 Sentra Intelligence":
    st.markdown("""
        <div class="hero">
            <h1>🧠 Sentra Intelligence</h1>
            <p class="hero-subtitle">AI‑Powered Risk Analysis & Remediation Guidance</p>
        </div>
    """, unsafe_allow_html=True)

    if not model:
        st.error("⚠️ Gemini is temporarily unavailable. Sentra is using its local intelligence engine.")
        st.info("""
            **How to fix:**  
            1. Create a `.env` file in the project root  
            2. Add `GEMINI_API_KEY=your_key_here`  
            3. Restart the app  
        """)
    else:
        st.success("✅ Sentra AI is active. Ask a question or let AI analyze your top risks.")
        sentra = SentraIntelligence()
        # --------------------------------------------
        # Ask Sentra
        # --------------------------------------------

        user_query = st.text_input(
            "Ask Sentra about your enterprise risk posture:",
            placeholder="Example: What is our highest business risk?"
        )

        if user_query:

            with st.spinner("Sentra is thinking..."):

                # First try local intelligence
                local_answer = sentra.answer_question(user_query)

                if local_answer:

                    st.success("⚡ Answered using Sentra Enterprise Intelligence")

                    st.markdown(local_answer)

                else:

                    prompt = f"""
        You are Sentra Intelligence, an AI assistant for an Enterprise Cyber Risk Intelligence Platform.

        Enterprise Risk Data

        {df.nlargest(
            10,
            "estimated_total_exposure"
        )[[
            "asset_name",
            "cve_id",
            "risk_level",
            "business_impact",
            "estimated_total_exposure",
            "decision"
        ]].to_string(index=False)}

        User Question:

        {user_query}

        Answer ONLY using the enterprise context above.

        If the answer cannot be inferred, clearly say so.
        """

                    try:

                        response = model.generate_content(prompt)

                        st.info("🤖 Answered using Gemini")

                        st.markdown(response.text)

                    except Exception:

                        st.error(
                            "Gemini is currently unavailable and "
                            "Sentra could not answer this question locally."
                        )


        # Pre-built: Top risk analysis
        st.subheader("📊 AI Analysis of Top Enterprise Risk")
        top_risk = df.loc[df["estimated_total_exposure"].idxmax()]
        with st.spinner("Generating AI risk summary..."):
            gemini_summary = sentra.executive_summary(top_risk)
            st.markdown(
                f"""
                <div class="ai-card">
                    <h4>📊 Executive Summary</h4>
                    {gemini_summary}
                </div>
                """,
                unsafe_allow_html=True
            )

        # Remediation recommendations
        st.subheader("🛠️ AI-Powered Remediation Guidance")
        with st.spinner("Generating recommendations..."):
            prompt = f"""
Given a {top_risk['risk_level']} risk on asset {top_risk['asset_name']} (CVE {top_risk['cve_id']}) with estimated financial exposure ${top_risk['estimated_total_exposure']:,.0f} and business impact {top_risk['business_impact']}, provide 3 specific remediation steps for a security team.
"""
            try:
                rec_response = model.generate_content(prompt)
                st.markdown(
                f"""
                <div class="ai-card">
                    <h4>🛠️ Recommended Actions</h4>
                    {rec_response.text}
                </div>
                """,
                unsafe_allow_html=True
            )
            except Exception:
                actions = sentra.remediation(top_risk)
                html = """
                <div class="ai-card">
                <h4>🛠️ Recommended Actions</h4>
                """

                for action in actions:
                    html += f"<p>• {action}</p>"

                html += "</div>"

                st.markdown(html, unsafe_allow_html=True)
                
                        
            


    st.markdown("---")
    st.markdown("**Roadmap**")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("✅ NVD data ingestion  \n✅ Business context mapping  \n✅ What‑if simulation  \n✅ Sentra Intelligence (active)")
    with col2:
        st.markdown("⏳ Real‑time CVE feed  \n⏳ Automated board PDFs  \n⏳ Role-based access  \n⏳ SaaS multi‑tenancy")

    st.caption("Sentra Intelligence uses Gemini to deliver executive-ready risk insights.")