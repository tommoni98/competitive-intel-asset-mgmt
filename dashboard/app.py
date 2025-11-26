import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import os
from pathlib import Path

import pkgutil

st.write("plotly installed?", pkgutil.find_loader("plotly") is not None)

# ----------------------------------------------------
# PAGE CONFIG & CUSTOM STYLING
# ----------------------------------------------------
st.set_page_config(
    page_title="Competitive Intelligence – Asset Management",
    layout="wide",
    page_icon="🏦",
)

# FinTech / modern CSS override
st.markdown(
    """
    <style>
    /* Global */
    body {
        background: radial-gradient(circle at top, #020617 0, #020617 45%, #000 100%);
    }
    .main {
        background: linear-gradient(140deg, #020617 0%, #020617 40%, #020617 100%);
        color: #e5e7eb;
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    /* Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(15,23,42,0.95), rgba(15,23,42,0.8));
        border-radius: 18px;
        border: 1px solid rgba(148,163,184,0.4);
        padding: 0.9rem 1.1rem;
        box-shadow: 0 18px 45px rgba(15,23,42,0.85);
    }
    .metric-label {
        font-size: 0.8rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin-bottom: 0.15rem;
    }
    .metric-value {
        font-size: 1.35rem;
        font-weight: 600;
        color: #e5e7eb;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: #9ca3af;
    }
    /* Section titles */
    .section-title {
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }
    .section-subtitle {
        font-size: 0.9rem;
        color: #9ca3af;
        margin-bottom: 0.8rem;
    }
    /* Tag-like pills */
    .pill {
        display: inline-flex;
        padding: 0.15rem 0.6rem;
        border-radius: 999px;
        border: 1px solid rgba(148,163,184,0.65);
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-right: 0.3rem;
        color: #9ca3af;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------
# DATA DEFINITIONS (FROM REPORT)
# ----------------------------------------------------

# High-level AUM & tech scoring
companies = ["BlackRock", "State Street", "Invesco"]

overview_data = [
    {
        "Company": "BlackRock",
        "AUM_2024_Tn": 11.551,
        "ETF_AUM_Tn": 4.23,
        "Alternatives_AUM_Tn": 0.422,
        "Tech_Score": 9,
        "Fee_Level": "Low–Mid",
        "Model": "Scale + Tech (Aladdin)",
    },
    {
        "Company": "State Street",
        "AUM_2024_Tn": 4.715,
        "ETF_AUM_Tn": 1.578,
        "Alternatives_AUM_Tn": 0.200,
        "Tech_Score": 7,
        "Fee_Level": "Competitive",
        "Model": "Custody + Platform (Alpha)",
    },
    {
        "Company": "Invesco",
        "AUM_2024_Tn": 1.846,
        "ETF_AUM_Tn": 0.484,
        "Alternatives_AUM_Tn": 0.1285,
        "Tech_Score": 6,
        "Fee_Level": "Mid-range",
        "Model": "Independent Asset Manager",
    },
]
overview_df = pd.DataFrame(overview_data)

# Financials
financials_data = [
    {
        "Company": "BlackRock",
        "Revenue_Bn": 20.407,
        "Net_Income_Bn": 6.369,
        "Op_Margin_%": 37.1,
        "ROE_%": 13.4,
        "ROA_%": 4.6,
        "Total_Assets_Bn": 138.615,
        "Equity_Bn": 47.431,
    },
    {
        "Company": "State Street",
        "Revenue_Bn": 13.04,
        "Net_Income_Bn": 2.687,
        "Op_Margin_%": 26.1,
        "ROE_%": 10.6,
        "ROA_%": 0.76,
        "Total_Assets_Bn": 353.240,
        "Equity_Bn": 25.326,
    },
    {
        "Company": "Invesco",
        "Revenue_Bn": 6.067,
        "Net_Income_Bn": 0.538,
        "Op_Margin_%": 13.7,
        "ROE_%": 3.6,
        "ROA_%": 2.0,
        "Total_Assets_Bn": 27.0089,
        "Equity_Bn": 15.1241,
    },
]
financials_df = pd.DataFrame(financials_data)

# Product mix
product_mix_data = [
    {
        "Company": "BlackRock",
        "Equity_Tn": 6.3102,
        "Fixed_Income_Tn": 2.9057,
        "Multi_Asset_Tn": 0.9929,
        "Cash_Tn": 0.9207,
        "Alternatives_Tn": 0.4218,
    },
    {
        "Company": "State Street",
        "Equity_Tn": 3.007,
        "Fixed_Income_Tn": 0.616,
        "Multi_Asset_Tn": 0.374,
        "Cash_Tn": 0.518,
        "Alternatives_Tn": 0.200,
    },
    {
        "Company": "Invesco",
        "Equity_Tn": 0.2665,
        "Fixed_Income_Tn": 0.2811,
        "Multi_Asset_Tn": 0.0588,
        "Cash_Tn": 0.1894,
        "Alternatives_Tn": 0.1285,
    },
]
product_mix_df = pd.DataFrame(product_mix_data)

# Technology profiles
tech_profiles = {
    "BlackRock": {
        "Platform": "Aladdin + eFront + Preqin",
        "Positioning": "Enterprise investment OS / data platform",
        "Highlights": [
            "Used by internal teams and external clients",
            "AI copilots and private markets integration",
            "Key differentiator and revenue source",
        ],
    },
    "State Street": {
        "Platform": "State Street Alpha (incl. Charles River Development)",
        "Positioning": "Front-to-back institutional servicing platform",
        "Highlights": [
            "Integrates portfolio mgmt, trading, and servicing",
            "Deeply embedded with large institutions",
            "Supports complex multi-asset / alternatives",
        ],
    },
    "Invesco": {
        "Platform": "Embedded next-gen tech (no standalone platform)",
        "Positioning": "Tech-enabled global investment manager",
        "Highlights": [
            "Quant models and analytics in investment process",
            "Focus on efficiency and client experience",
            "No external platform like Aladdin/Alpha (yet)",
        ],
    },
}

# SWOT data
swot_data = [
    {
        "Company": "BlackRock",
        "Strengths": [
            "Largest global AUM (> $11.5T)",
            "Dominant ETF franchise (iShares)",
            "Aladdin technology and data moat",
            "Broad product spectrum (active + passive + alts)",
        ],
        "Weaknesses": [
            "High regulatory scrutiny and SIFI risk",
            "Integration risk from large acquisitions",
            "Fee pressure in core ETF business",
        ],
        "Opportunities": [
            "Private markets & infrastructure growth",
            "AI & data monetization via Aladdin + Preqin",
            "International and wealth channel expansion",
        ],
        "Threats": [
            "ETF fee wars with Vanguard & others",
            "Regulatory constraints on size and data",
            "Market downturn impacting AUM and fees",
        ],
    },
    {
        "Company": "State Street",
        "Strengths": [
            "Top-tier global custodian with $46T+ AUC/A",
            "Alpha platform drives front-to-back stickiness",
            "Deep institutional relationships",
        ],
        "Weaknesses": [
            "Lower margins vs pure asset managers",
            "High dependency on interest-rate-sensitive NII",
            "Limited retail presence",
        ],
        "Opportunities": [
            "Servicing of alternatives and private assets",
            "Wealth and data-driven services",
            "More Alpha mandates from large asset owners",
        ],
        "Threats": [
            "Regulatory burden as a G-SIB",
            "Custody fee pressure and competition",
            "Operational and cyber risk in complex stack",
        ],
    },
    {
        "Company": "Invesco",
        "Strengths": [
            "Independent global asset manager",
            "Strong ETF and QQQ franchise",
            "Diversified product and geography mix",
        ],
        "Weaknesses": [
            "Smaller scale vs mega-managers",
            "Exposure to fee and margin pressure",
            "Less differentiated technology platform",
        ],
        "Opportunities": [
            "APAC and ETF expansion",
            "Scaling private markets and global liquidity",
            "Cost efficiency and operating leverage",
        ],
        "Threats": [
            "Intense competition from BlackRock/Vanguard",
            "Market volatility impacting active flows",
            "Regulation and distribution changes",
        ],
    },
]

# Business model snippets
business_models = {
    "BlackRock": {
        "Model": "Global asset manager focused on Retail, iShares (ETFs) and Institutional",
        "Key_Pillars": [
            "Scale-driven AUM model",
            "Technology & data (Aladdin) as second growth engine",
            "Strategic push into private markets & infrastructure",
        ],
    },
    "State Street": {
        "Model": "Custody and investment servicing bank + asset manager (SSGA)",
        "Key_Pillars": [
            "Investment Servicing as foundation (custody, FX, lending)",
            "Alpha platform integrating front-to-back processes",
            "Institutional client depth and recurring relationships",
        ],
    },
    "Invesco": {
        "Model": "Independent global investment manager across active, passive, ETFs & alternatives",
        "Key_Pillars": [
            "Balanced retail and institutional footprint",
            "Scaling high-conviction franchises (e.g., QQQ)",
            "Embedding next-generation technology internally",
        ],
    },
}

# Risk heatmap (subjective scoring 1–5)
risk_categories = ["Regulatory", "Market", "Interest Rate", "Operational/Tech", "Fee Pressure"]
risk_matrix = pd.DataFrame(
    [
        [4, 4, 3, 4, 4],  # BlackRock
        [5, 3, 5, 4, 3],  # State Street
        [3, 4, 3, 3, 5],  # Invesco
    ],
    columns=risk_categories,
    index=companies,
)

# ----------------------------------------------------
# HELPER RENDER FUNCTIONS
# ----------------------------------------------------
def render_kpi_card(label, value, sublabel=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{sublabel}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_overview():
    st.markdown('<div class="section-title">Overview & Executive Snapshot</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">'
        "High-level view of scale, ETF exposure, alternatives and technology strength for BlackRock, State Street and Invesco."
        "</div>",
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    total_aum = overview_df["AUM_2024_Tn"].sum()
    total_etf = overview_df["ETF_AUM_Tn"].sum()
    avg_tech = overview_df["Tech_Score"].mean()
    alts_total = overview_df["Alternatives_AUM_Tn"].sum()

    with col1:
        render_kpi_card("Total AUM (2024)", f"{total_aum:.2f} Tn", "Across 3 managers")
    with col2:
        render_kpi_card("Total ETF AUM", f"{total_etf:.2f} Tn", "ETF platforms")
    with col3:
        render_kpi_card("Total Alternatives", f"{alts_total:.2f} Tn", "Private markets & alts")
    with col4:
        render_kpi_card("Avg Tech Strength", f"{avg_tech:.1f} / 10", "Tech & platform capability")

    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        fig_aum = px.bar(
            overview_df,
            x="Company",
            y="AUM_2024_Tn",
            title="Total AUM 2024",
            labels={"AUM_2024_Tn": "AUM ($ Trillions)"},
            text_auto=".2f",
        )
        fig_aum.update_layout(template="plotly_dark", height=360, margin=dict(t=50, b=40, l=40, r=20))
        st.plotly_chart(fig_aum, use_container_width=True)

    with c2:
        share_df = overview_df.copy()
        share_df["ETF_Share_%"] = (share_df["ETF_AUM_Tn"] / share_df["AUM_2024_Tn"]) * 100
        fig_etf = px.bar(
            share_df,
            x="Company",
            y="ETF_Share_%",
            title="ETF AUM as % of Total AUM",
            labels={"ETF_Share_%": "ETF Share of AUM (%)"},
            text_auto=".1f",
        )
        fig_etf.update_layout(template="plotly_dark", height=360, margin=dict(t=50, b=40, l=40, r=20))
        st.plotly_chart(fig_etf, use_container_width=True)

    st.markdown("### Narrative Highlights")
    st.write(
        "- **BlackRock**: Clear scale leader with > $11.5T AUM and the highest tech score, reflecting the "
        "strength of Aladdin and its expansion into private markets.\n"
        "- **State Street**: Smaller AUM as an asset manager but huge AUC/A as a servicer; strong ETF presence via SPDR and "
        "a robust Alpha platform.\n"
        "- **Invesco**: Large independent manager with meaningful ETF and alternatives exposure, but trailing in overall scale and tech score."
    )


def render_financials():
    st.markdown('<div class="section-title">Financial Performance</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">'
        "Comparing revenue, profitability and returns across the three competitors."
        "</div>",
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        top_rev = financials_df.loc[financials_df["Revenue_Bn"].idxmax()]
        render_kpi_card("Revenue Leader", f"{top_rev['Company']}", f"{top_rev['Revenue_Bn']:.1f} Bn")
    with c2:
        top_margin = financials_df.loc[financials_df["Op_Margin_%"].idxmax()]
        render_kpi_card("Highest Operating Margin", f"{top_margin['Company']}", f"{top_margin['Op_Margin_%']:.1f}%")
    with c3:
        top_roe = financials_df.loc[financials_df["ROE_%"].idxmax()]
        render_kpi_card("ROE Leader", f"{top_roe['Company']}", f"{top_roe['ROE_%']:.1f}%")

    st.markdown("---")

    col_a, col_b = st.columns(2)
    with col_a:
        fig_rev = px.bar(
            financials_df,
            x="Company",
            y="Revenue_Bn",
            title="Total Revenue (2024, $Bn)",
            text_auto=".1f",
        )
        fig_rev.update_layout(template="plotly_dark", height=360, margin=dict(t=50, b=40, l=40, r=20))
        st.plotly_chart(fig_rev, use_container_width=True)

        fig_margin = px.bar(
            financials_df,
            x="Company",
            y="Op_Margin_%",
            title="Operating Margin (%)",
            text_auto=".1f",
        )
        fig_margin.update_layout(template="plotly_dark", height=360, margin=dict(t=50, b=40, l=40, r=20))
        st.plotly_chart(fig_margin, use_container_width=True)

    with col_b:
        fig_roe = px.scatter(
            financials_df,
            x="ROE_%",
            y="ROA_%",
            size="Revenue_Bn",
            color="Company",
            hover_name="Company",
            title="ROE vs ROA (Bubble size = Revenue)",
        )
        fig_roe.update_layout(template="plotly_dark", height=360, margin=dict(t=50, b=40, l=40, r=20))
        st.plotly_chart(fig_roe, use_container_width=True)

        fig_ni = px.bar(
            financials_df,
            x="Company",
            y="Net_Income_Bn",
            title="Net Income (2024, $Bn)",
            text_auto=".2f",
        )
        fig_ni.update_layout(template="plotly_dark", height=360, margin=dict(t=50, b=40, l=40, r=20))
        st.plotly_chart(fig_ni, use_container_width=True)

    st.markdown("### Interpretation")
    st.write(
        "- **BlackRock** generates the highest revenue and net income by a wide margin and sustains the best operating margin.\n"
        "- **State Street** delivers solid profitability within a lower-margin servicing model, with ROE close to BlackRock’s.\n"
        "- **Invesco** exhibits materially lower margins and returns, highlighting the impact of fee pressure and scale constraints."
    )


def render_business_model():
    st.markdown('<div class="section-title">Business Model & Strategic Positioning</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">'
        "Comparing how each firm creates value through its core model and strategic pillars."
        "</div>",
        unsafe_allow_html=True,
    )

    company_choice = st.selectbox("Select a company to explore its business model:", companies, index=0)

    model_info = business_models[company_choice]

    st.markdown(f"#### {company_choice} – Model Overview")
    st.write(model_info["Model"])

    st.markdown("#### Strategic Pillars")
    for p in model_info["Key_Pillars"]:
        st.write(f"- {p}")

    st.markdown("---")
    st.markdown("#### Strategic Positioning Map – Price vs Innovation")

    # Build a small positioning scatter using tech score + a fee proxy
    fee_map = {"Low–Mid": 3, "Competitive": 4, "Mid-range": 5}
    position_df = overview_df.copy()
    position_df["Fee_Level_Score"] = position_df["Fee_Level"].replace(fee_map)

    fig_pos = px.scatter(
        position_df,
        x="Fee_Level_Score",
        y="Tech_Score",
        text="Company",
        labels={
            "Fee_Level_Score": "Relative Fee Level (Higher = More Expensive)",
            "Tech_Score": "Technology / Platform Strength (1–10)",
        },
        title="Competitive Positioning: Fees vs Technology",
    )
    fig_pos.update_traces(textposition="top center")
    fig_pos.update_layout(
        template="plotly_dark",
        xaxis=dict(tickvals=[3, 4, 5], ticktext=["Low–Mid", "Competitive", "Mid-range"]),
        height=420,
        margin=dict(t=60, b=40, l=40, r=40),
    )
    st.plotly_chart(fig_pos, use_container_width=True)

    st.write(
        "- **Top-left quadrant (low fee, high tech)** is the most attractive: BlackRock is closest given its scale and Aladdin.\n"
        "- **State Street** leans more toward institutional, competitively priced servicing with strong platform capability.\n"
        "- **Invesco** sits in the middle on fees and somewhat lower on tech, relying on its product franchises rather than a flagship platform."
    )


def render_product_mix():
    st.markdown('<div class="section-title">Product & AUM Mix</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">'
        "Breakdown of AUM across equity, fixed income, multi-asset, cash and alternatives."
        "</div>",
        unsafe_allow_html=True,
    )

    # Stacked bar by asset class
    melted = product_mix_df.melt(id_vars="Company", var_name="Asset_Class", value_name="AUM_Tn")
    asset_class_map = {
        "Equity_Tn": "Equity",
        "Fixed_Income_Tn": "Fixed Income",
        "Multi_Asset_Tn": "Multi-Asset",
        "Cash_Tn": "Cash / Money Market",
        "Alternatives_Tn": "Alternatives",
    }
    melted["Asset_Class"] = melted["Asset_Class"].replace(asset_class_map)

    fig_stack = px.bar(
        melted,
        x="Company",
        y="AUM_Tn",
        color="Asset_Class",
        title="AUM by Asset Class (2024, $Trillions)",
    )
    fig_stack.update_layout(template="plotly_dark", height=420, margin=dict(t=60, b=40, l=40, r=40))
    st.plotly_chart(fig_stack, use_container_width=True)

    st.markdown("### Product Mix Table")
    st.dataframe(product_mix_df.set_index("Company"), use_container_width=True)

    st.markdown("### Product Mix Observations")
    st.write(
        "- **BlackRock**: Heavily equity-weighted, with substantial fixed income and a meaningful but smaller alternatives book.\n"
        "- **State Street**: Strong equity and cash presence consistent with its institutional index and ETF heritage.\n"
        "- **Invesco**: Smaller in absolute terms but diversified across equity, fixed income, cash and growing alternatives."
    )


def render_technology():
    st.markdown('<div class="section-title">Technology & Platform Edge</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">'
        "Assessing Aladdin, Alpha and Invesco’s embedded tech capabilities."
        "</div>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1.2, 1])
    with col1:
        fig_tech = px.bar(
            overview_df,
            x="Company",
            y="Tech_Score",
            title="Technology / Platform Strength (1–10)",
            text_auto=".0f",
        )
        fig_tech.update_layout(template="plotly_dark", height=400, margin=dict(t=60, b=40, l=40, r=40))
        st.plotly_chart(fig_tech, use_container_width=True)

    with col2:
        st.markdown("#### Platform Summary")
        for comp in companies:
            st.markdown(f"**{comp}**")
            st.write(f"- Platform: {tech_profiles[comp]['Platform']}")
            st.write(f"- Positioning: {tech_profiles[comp]['Positioning']}")
            st.write("")

    st.markdown("---")
    st.markdown("#### Platform Highlights by Firm")

    tech_company = st.selectbox("Select company to view platform details:", companies, index=0)
    profile = tech_profiles[tech_company]

    st.markdown(f"**{tech_company} – {profile['Platform']}**")
    for h in profile["Highlights"]:
        st.write(f"- {h}")


def render_risk():
    st.markdown('<div class="section-title">Risk & Regulatory Profile</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">'
        "Heatmap of key risk exposures: regulatory, market, interest rate, operational/tech and fee pressure."
        "</div>",
        unsafe_allow_html=True,
    )

    fig = go.Figure(
        data=go.Heatmap(
            z=risk_matrix.values,
            x=risk_matrix.columns,
            y=risk_matrix.index,
            colorscale="Viridis",
            colorbar=dict(title="Risk Level (1–5)"),
        )
    )
    fig.update_layout(
        template="plotly_dark",
        height=420,
        margin=dict(t=60, b=40, l=60, r=40),
        title="Relative Risk Exposure Heatmap",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Narrative Interpretation")
    st.write(
        "- **State Street** shows the highest regulatory and interest rate risk due to its G-SIB status and NII dependence.\n"
        "- **BlackRock** faces elevated regulatory and operational/tech risk given its scale and centrality of Aladdin.\n"
        "- **Invesco** is most exposed to fee pressure and market risk, reflecting its traditional asset management model and smaller scale."
    )


def render_swot():
    st.markdown('<div class="section-title">SWOT Explorer</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">'
        "Interactive view of strengths, weaknesses, opportunities and threats for each firm."
        "</div>",
        unsafe_allow_html=True,
    )

    comp_choice = st.selectbox("Select a company:", companies, index=0)
    selected = next(item for item in swot_data if item["Company"] == comp_choice)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### ✅ Strengths")
        for s_item in selected["Strengths"]:
            st.write(f"- {s_item}")
        st.markdown("#### ⚠️ Weaknesses")
        for w_item in selected["Weaknesses"]:
            st.write(f"- {w_item}")

    with col2:
        st.markdown("#### 🎯 Opportunities")
        for o_item in selected["Opportunities"]:
            st.write(f"- {o_item}")
        st.markdown("#### ⚡ Threats")
        for t_item in selected["Threats"]:
            st.write(f"- {t_item}")


def render_outlook():
    st.markdown('<div class="section-title">Forward Outlook & Strategic Implications</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">'
        "How industry trends, technology and private markets shape the next phase of competition."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("### Major Industry Themes")
    st.write(
        "- **Private markets & alternatives** are the main growth engine.\n"
        "- **Integrated technology and data platforms** are becoming the core competitive moat.\n"
        "- **Fee compression and margin pressure** continue to challenge traditional managers.\n"
        "- **Regulation and operational resilience** are critical constraints for systemically important firms."
    )

    st.markdown("### Firm-by-Firm Outlook")
    st.markdown("**BlackRock**")
    st.write(
        "- Best positioned to dominate in private markets and technology, provided it manages integration risk.\n"
        "- Likely to keep expanding Aladdin’s ecosystem and data capabilities."
    )

    st.markdown("**State Street**")
    st.write(
        "- Expected to reinforce its role as institutional infrastructure through Alpha and alternative servicing.\n"
        "- Profitability will hinge on balancing regulatory capital, NII and servicing fees."
    )

    st.markdown("**Invesco**")
    st.write(
        "- Must execute on efficiency, scale its winning franchises (e.g., QQQ, ETFs) and continue upgrading tech.\n"
        "- Success depends on differentiating as an independent, diversified manager in a scale-driven world."
    )

    st.markdown("---")
    st.markdown("### High-Level Strategic Recommendations")
    st.write(
        "- **Double down on technology**: treating platforms and data as profit centers, not cost centers.\n"
        "- **Align product strategy with secular flows**: particularly towards private markets, ETFs, and solutions.\n"
        "- **Strengthen operating leverage**: through automation, simplification and global operating models.\n"
        "- **Build resilience**: ensuring regulatory, risk and cyber capabilities keep up with business complexity."
    )


def render_downloads():
    st.markdown('<div class="section-title">Downloads & Artefacts</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">'
        "Download the PDF versions of the full report and executive summary used in this analysis."
        "</div>",
        unsafe_allow_html=True,
    )

    # app.py is in /dashboard → go up to repo root → into /report
    base_dir = Path(__file__).resolve().parent          # .../dashboard
    repo_root = base_dir.parent                         # .../
    report_dir = repo_root / "report"

    full_report_path = report_dir / "Competitive Intelligence Analysis.pdf"
    exec_summary_path = report_dir / "Executive Summary.pdf"

    col1, col2 = st.columns(2)

    # Full report download
    with col1:
        st.markdown("#### 📄 Full Competitive Intelligence Report")
        if full_report_path.exists():
            with full_report_path.open("rb") as f:
                full_bytes = f.read()
            st.download_button(
                label="Download Full Report (PDF)",
                data=full_bytes,
                file_name="Competitive Intelligence Analysis.pdf",
                mime="application/pdf",
            )
        else:
            st.warning(
                "Full report PDF not found.\n\n"
                "Expected at: `report/Competitive Intelligence Analysis.pdf`"
            )

    # Executive summary download
    with col2:
        st.markdown("#### 📄 Executive Summary")
        if exec_summary_path.exists():
            with exec_summary_path.open("rb") as f:
                summary_bytes = f.read()
            st.download_button(
                label="Download Executive Summary (PDF)",
                data=summary_bytes,
                file_name="Executive Summary.pdf",
                mime="application/pdf",
            )
        else:
            st.warning(
                "Executive summary PDF not found.\n\n"
                "Expected at: `report/Executive Summary.pdf`"
            )

    st.markdown("---")
    st.markdown("#### 🔗 GitHub Repository")
    st.write(
        "View the full project, code and documentation on GitHub. "
        "Update this text with your actual repo URL, for example:\n\n"
        "`https://github.com/tommoni98/competitive-intel-asset-mgmt`"
    )




# ----------------------------------------------------
# SIDEBAR NAVIGATION
# ----------------------------------------------------
st.sidebar.markdown("### 🏦 CI: Asset Management")
st.sidebar.markdown(
    "<span class='pill'>BlackRock</span> <span class='pill'>State Street</span> <span class='pill'>Invesco</span>",
    unsafe_allow_html=True,
)
page = st.sidebar.radio(
    "Navigate",
    [
        "Overview",
        "Financials",
        "Business Model",
        "Product Mix",
        "Technology",
        "Risk & Regulation",
        "SWOT",
        "Outlook",
        "Downloads",
    ],
)

# ----------------------------------------------------
# MAIN RENDER LOGIC
# ----------------------------------------------------
st.markdown(
    """
    <h1 style="margin-bottom:0.1rem;">Competitive Intelligence Dashboard</h1>
    <p style="color:#9ca3af;font-size:0.92rem;margin-bottom:0.5rem;">
    Strategic analysis of BlackRock, State Street and Invesco based on 2024 10-Ks and Annual Reports.
    </p>
    """,
    unsafe_allow_html=True,
)

if page == "Overview":
    render_overview()
elif page == "Financials":
    render_financials()
elif page == "Business Model":
    render_business_model()
elif page == "Product Mix":
    render_product_mix()
elif page == "Technology":
    render_technology()
elif page == "Risk & Regulation":
    render_risk()
elif page == "SWOT":
    render_swot()
elif page == "Outlook":
    render_outlook()
elif page == "Downloads":
    render_downloads()
