"""
AI Opportunity Identifier — Enterprise Process Assessment
===========================================================
Evaluates business processes for AI automation potential, recommends
implementation approaches, and estimates impact. Built for enterprise
IT teams identifying where AI can reduce manual effort and improve outcomes.

Built by Hammad Mirza | Portfolio Project for Honda Canada
"""

import streamlit as st
import plotly.graph_objects as go
import math

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Opportunity Identifier",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;600;700&display=swap');
    .main { background-color: #f8f9fc; }
    .header-banner {
        background: linear-gradient(135deg, #cc0000 0%, #8b0000 50%, #1a1a2e 100%);
        padding: 2.5rem 2rem; border-radius: 12px; margin-bottom: 1.5rem;
        color: white; text-align: center;
    }
    .header-banner h1 { font-family: 'Source Sans Pro', sans-serif; font-weight: 700; font-size: 2rem; margin-bottom: 0.3rem; color: white; }
    .header-banner p { font-family: 'Source Sans Pro', sans-serif; font-weight: 300; font-size: 1.05rem; opacity: 0.9; margin: 0; }
    .section-header {
        font-family: 'Source Sans Pro', sans-serif; font-weight: 700; font-size: 1.25rem;
        color: #1a1a2e; border-bottom: 3px solid #cc0000; padding-bottom: 0.4rem;
        margin-top: 1.5rem; margin-bottom: 1rem;
    }
    .result-card {
        background: white; border-radius: 10px; padding: 1.2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06); border-left: 4px solid #cc0000; margin-bottom: 0.8rem;
    }
    .result-card h4 { margin-top: 0; color: #1a1a2e; font-size: 1rem; }
    .risk-flag {
        background: #fff3f0; border-left: 4px solid #cc0000; padding: 0.6rem 1rem;
        border-radius: 0 8px 8px 0; margin-bottom: 0.4rem; font-size: 0.9rem;
    }
    .strength-flag {
        background: #f0faf4; border-left: 4px solid #27ae60; padding: 0.6rem 1rem;
        border-radius: 0 8px 8px 0; margin-bottom: 0.4rem; font-size: 0.9rem;
    }
    .phase-card {
        background: #f8f9fc; border: 1px solid #e0e0e0; border-left: 3px solid #cc0000;
        border-radius: 0 8px 8px 0; padding: 0.8rem 1rem; margin-bottom: 0.5rem;
    }
    .footer-note {
        text-align: center; color: #888; font-size: 0.8rem; margin-top: 2rem;
        padding-top: 1rem; border-top: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
    <h1>⚡ AI Opportunity Identifier</h1>
    <p>Enterprise Process Assessment — Identify where AI can reduce manual effort and improve outcomes</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
> **Purpose:** This tool evaluates enterprise business processes for AI automation potential.
> It classifies the AI opportunity type, recommends an implementation approach, estimates
> impact and ROI, assesses complexity, and generates a phased roadmap — enabling
> Product Owners and IT teams to make data-informed decisions about where to invest in AI.
""")

# ─────────────────────────────────────────────────────────────
# SCENARIOS
# ─────────────────────────────────────────────────────────────
SCENARIOS = {
    "— Select a scenario or enter your own below —": {},
    "Warranty Claims Triage": {
        "domain": "Warranty & Claims",
        "process_name": "Warranty Claims Triage & Adjudication",
        "description": "Dealers submit warranty claims through the portal. Each claim is manually reviewed by warranty operations staff for eligibility, parts verification, labour time accuracy, and policy compliance. Claims are individually adjudicated and approved or rejected.",
        "performer": "Manual by staff with some system support",
        "frequency": "Per transaction",
        "time_per": 25,
        "volume": 500,
        "pain_points": ["Time-consuming", "Inconsistent outcomes", "Error-prone", "Requires specialized knowledge"]
    },
    "Dealer Onboarding Documentation": {
        "domain": "Dealer Operations",
        "process_name": "New Dealer Onboarding & Compliance Review",
        "description": "When a new dealer joins the network, their documentation (business licenses, insurance, financial statements, facility certifications) is manually collected, reviewed, and verified against compliance requirements. Multiple departments are involved in the review chain.",
        "performer": "Fully manual with email/paper",
        "frequency": "Per transaction",
        "time_per": 480,
        "volume": 15,
        "pain_points": ["Time-consuming", "Error-prone", "Compliance-sensitive", "Requires specialized knowledge"]
    },
    "Parts Order Forecasting": {
        "domain": "Parts & Service",
        "process_name": "Dealer Parts Demand Forecasting",
        "description": "Regional parts managers manually review dealer order history, seasonal trends, and vehicle population data to forecast parts demand and set inventory allocation. Forecasts are compiled in spreadsheets and adjusted based on manager experience.",
        "performer": "Manual by staff with some system support",
        "frequency": "Weekly",
        "time_per": 180,
        "volume": 50,
        "pain_points": ["Time-consuming", "Inconsistent outcomes", "Requires specialized knowledge"]
    },
    "Customer Complaint Routing": {
        "domain": "Customer Experience",
        "process_name": "Customer Complaint Classification & Routing",
        "description": "Customer complaints received via phone, email, and web forms are manually read, categorized by type (vehicle quality, dealer service, warranty, safety), assessed for severity, and routed to the appropriate department. Urgent safety complaints must be escalated immediately.",
        "performer": "Manual by staff with some system support",
        "frequency": "Per transaction",
        "time_per": 15,
        "volume": 800,
        "pain_points": ["Time-consuming", "Inconsistent outcomes", "High staff turnover impact", "Compliance-sensitive"]
    },
    "F&I Document Verification": {
        "domain": "Sales & F&I",
        "process_name": "F&I Document Completeness Verification",
        "description": "When a vehicle deal is finalized, F&I documents (credit applications, loan agreements, insurance forms, trade-in valuations) are manually checked for completeness, accuracy, and regulatory compliance before funding release. Missing or incorrect documents delay funding and impact dealer cash flow.",
        "performer": "Manual by staff with some system support",
        "frequency": "Per transaction",
        "time_per": 20,
        "volume": 600,
        "pain_points": ["Time-consuming", "Error-prone", "Compliance-sensitive"]
    }
}

# ─────────────────────────────────────────────────────────────
# SIDEBAR — INPUT
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Process Assessment")

    scenario = st.selectbox("Quick-load a scenario", list(SCENARIOS.keys()))
    s = SCENARIOS.get(scenario, {})

    st.markdown("---")

    domain = st.selectbox("Business Domain", [
        "Dealer Operations", "Warranty & Claims", "Sales & F&I",
        "Parts & Service", "Finance & Reporting", "Customer Experience"
    ], index=["Dealer Operations", "Warranty & Claims", "Sales & F&I",
              "Parts & Service", "Finance & Reporting", "Customer Experience"
              ].index(s.get("domain", "Dealer Operations")))

    process_name = st.text_input("Process Name", value=s.get("process_name", ""))
    description = st.text_area("Current Process Description", value=s.get("description", ""), height=120)

    performer = st.selectbox("Who performs this today?", [
        "Fully manual with email/paper",
        "Manual by staff with some system support",
        "Semi-automated with manual checkpoints",
        "Mostly automated with exception handling"
    ], index=["Fully manual with email/paper",
              "Manual by staff with some system support",
              "Semi-automated with manual checkpoints",
              "Mostly automated with exception handling"
              ].index(s.get("performer", "Manual by staff with some system support")))

    frequency = st.selectbox("Frequency", [
        "Per transaction", "Daily", "Weekly", "Monthly"
    ], index=["Per transaction", "Daily", "Weekly", "Monthly"
              ].index(s.get("frequency", "Per transaction")))

    time_per = st.slider("Avg time per instance (minutes)", 5, 480, s.get("time_per", 30))
    volume = st.slider("Volume per month", 5, 5000, s.get("volume", 100))

    pain_points = st.multiselect(
        "Current Pain Points",
        ["Time-consuming", "Error-prone", "Inconsistent outcomes",
         "Requires specialized knowledge", "High staff turnover impact",
         "Compliance-sensitive"],
        default=s.get("pain_points", [])
    )

    st.markdown("---")
    st.markdown("### Methodology")
    st.caption("""
    Assessment scores are calculated from process characteristics:
    automation level, frequency, volume, time investment, and pain point
    severity. Classification follows enterprise AI adoption frameworks
    with human-in-the-loop governance as default.
    """)
    st.markdown("---")
    st.caption("Built by **Hammad Mirza**")
    st.caption("Portfolio Project — June 2026")

    assess = st.button("Run Assessment", type="primary", use_container_width=True)


# ─────────────────────────────────────────────────────────────
# ASSESSMENT LOGIC
# ─────────────────────────────────────────────────────────────
if not assess and not process_name:
    st.info("Configure a business process in the sidebar and click **Run Assessment** to evaluate AI potential.")
    st.stop()

if not process_name:
    st.warning("Please enter a process name.")
    st.stop()


# ── SCORING ──
def calculate_score(performer, frequency, time_per, volume, pain_points):
    score = 0

    # Automation level (0-25)
    performer_scores = {
        "Fully manual with email/paper": 25,
        "Manual by staff with some system support": 20,
        "Semi-automated with manual checkpoints": 12,
        "Mostly automated with exception handling": 5
    }
    score += performer_scores.get(performer, 10)

    # Frequency (0-15)
    freq_scores = {"Per transaction": 15, "Daily": 13, "Weekly": 8, "Monthly": 4}
    score += freq_scores.get(frequency, 8)

    # Volume (0-20)
    if volume >= 1000:
        score += 20
    elif volume >= 500:
        score += 17
    elif volume >= 200:
        score += 14
    elif volume >= 50:
        score += 10
    else:
        score += 5

    # Time per instance (0-20)
    if time_per >= 240:
        score += 20
    elif time_per >= 120:
        score += 17
    elif time_per >= 60:
        score += 14
    elif time_per >= 30:
        score += 11
    elif time_per >= 15:
        score += 8
    else:
        score += 4

    # Pain points (0-20)
    pain_weights = {
        "Time-consuming": 3,
        "Error-prone": 4,
        "Inconsistent outcomes": 4,
        "Requires specialized knowledge": 3,
        "High staff turnover impact": 3,
        "Compliance-sensitive": 3
    }
    pain_score = sum(pain_weights.get(p, 2) for p in pain_points)
    score += min(pain_score, 20)

    return min(score, 100)


def classify_opportunity(score, pain_points, performer):
    """Classify the AI opportunity type."""
    if score >= 75 and "Compliance-sensitive" not in pain_points:
        return "Full Automation", "Rules-based automation with exception routing. Process characteristics indicate high volume, repetitive work suitable for end-to-end automation with human oversight on exceptions only."
    elif score >= 60 or (score >= 50 and "Inconsistent outcomes" in pain_points):
        return "AI-Assisted Decision Support", "Copilot-style AI that analyzes inputs, recommends actions, and presents findings to a human reviewer. The human retains decision authority. Best for processes where judgment is needed but AI can accelerate the analysis."
    elif score >= 40:
        return "Intelligent Triage", "AI classifies and routes incoming items by complexity and risk. Low-complexity items are fast-tracked, complex items are routed to specialists. Reduces time spent on routine items while ensuring expert attention where needed."
    else:
        return "Monitor & Optimize", "Process characteristics suggest limited AI automation potential at this time. Recommend monitoring with analytics dashboards and exploring targeted optimizations before investing in AI. Consider reassessing if volume or complexity increases."


def get_ai_approach(classification, pain_points):
    """Recommend specific AI technology approach."""
    approaches = {
        "Full Automation": {
            "technology": "Rules Engine + RPA + ML Classification",
            "description": "Combine business rules for known patterns with ML for edge case handling. RPA handles system interactions (data entry, form filling, status updates). ML model classifies exceptions for human routing.",
            "copilot_fit": "Agent-based workflow — AI executes end-to-end with human oversight dashboard"
        },
        "AI-Assisted Decision Support": {
            "technology": "NLP + ML Classification + Copilot Interface",
            "description": "AI analyzes incoming data, extracts key information, compares against historical patterns, and presents a recommendation with confidence score. Human reviewer sees AI analysis alongside source data and makes the final call.",
            "copilot_fit": "Copilot-style assistant — AI prepares, human decides"
        },
        "Intelligent Triage": {
            "technology": "ML Classification + Priority Scoring",
            "description": "ML model trained on historical outcomes classifies incoming items by complexity (Low/Medium/High/Exception). Priority scoring determines queue order. Routing rules send items to the appropriate handler based on classification.",
            "copilot_fit": "Smart routing — AI classifies and prioritizes, humans process"
        },
        "Monitor & Optimize": {
            "technology": "Analytics Dashboard + Process Mining",
            "description": "Deploy process analytics to identify bottlenecks, measure cycle times, and surface optimization opportunities. Use this data to build the business case for future AI investment when the process reaches sufficient scale.",
            "copilot_fit": "Reporting assistant — AI surfaces insights, humans investigate"
        }
    }
    return approaches.get(classification, approaches["Monitor & Optimize"])


def estimate_impact(time_per, volume, classification):
    """Estimate hours saved and ROI."""
    annual_hours = (time_per * volume * 12) / 60

    reduction_rates = {
        "Full Automation": 0.70,
        "AI-Assisted Decision Support": 0.45,
        "Intelligent Triage": 0.35,
        "Monitor & Optimize": 0.10
    }
    reduction = reduction_rates.get(classification, 0.20)

    hours_saved = annual_hours * reduction
    avg_hourly_rate = 45
    cost_savings = hours_saved * avg_hourly_rate

    return annual_hours, hours_saved, cost_savings, reduction


def assess_complexity(performer, pain_points, volume):
    """Assess implementation complexity."""
    complexity_score = 0

    if performer == "Fully manual with email/paper":
        complexity_score += 3
    elif performer == "Manual by staff with some system support":
        complexity_score += 2

    if "Compliance-sensitive" in pain_points:
        complexity_score += 2
    if "Requires specialized knowledge" in pain_points:
        complexity_score += 1
    if volume >= 1000:
        complexity_score += 1

    if complexity_score >= 5:
        return "High", "Multiple integration points, compliance requirements, and significant change management effort. Requires dedicated project team and phased approach."
    elif complexity_score >= 3:
        return "Medium", "Moderate integration and change management requirements. Can be delivered by a cross-functional team within standard delivery timelines."
    else:
        return "Low", "Straightforward implementation with minimal integration complexity. Can leverage existing tools and infrastructure with focused configuration effort."


def generate_risks(pain_points, classification, performer):
    """Generate risk flags based on inputs."""
    risks = []

    if "Compliance-sensitive" in pain_points:
        risks.append("Compliance and regulatory review required before AI-assisted decisions are enabled. Legal, risk, and governance teams must approve the AI use case documentation.")
    if "High staff turnover impact" in pain_points:
        risks.append("High turnover means institutional knowledge may not be well-documented. AI training data quality depends on capturing expert decision patterns before knowledge is lost.")
    if "Inconsistent outcomes" in pain_points:
        risks.append("Inconsistent human outcomes mean AI training data may contain conflicting labels. A data quality audit and outcome standardization exercise should precede model development.")
    if "Error-prone" in pain_points:
        risks.append("Current error rates need baselining before AI deployment. Without a baseline, measuring AI accuracy improvement will not be possible.")
    if performer == "Fully manual with email/paper":
        risks.append("No existing digital workflow to integrate with. Requires digitization of the current process before AI can be applied. Consider process re-engineering alongside AI enablement.")
    if classification == "Full Automation":
        risks.append("Full automation requires robust exception handling and monitoring. Over-reliance on AI without maintaining human expertise creates fragility. Maintain mandatory human review rotation.")

    return risks


def generate_strengths(pain_points, score, volume, classification):
    """Generate strength indicators."""
    strengths = []

    if score >= 70:
        strengths.append("Strong AI automation candidate — process characteristics align well with proven AI patterns.")
    if volume >= 500:
        strengths.append("High volume provides excellent training data foundation for ML models.")
    if "Time-consuming" in pain_points:
        strengths.append("Significant time investment per instance means even moderate AI improvement yields substantial ROI.")
    if "Inconsistent outcomes" in pain_points and classification in ["AI-Assisted Decision Support", "Intelligent Triage"]:
        strengths.append("AI standardization can directly address outcome inconsistency — one of the strongest use cases for decision support AI.")
    if len(pain_points) >= 3:
        strengths.append("Multiple pain points create a compelling business case with measurable improvement across several dimensions.")

    return strengths


# ── RUN ASSESSMENT ──
score = calculate_score(performer, frequency, time_per, volume, pain_points)
classification, class_desc = classify_opportunity(score, pain_points, performer)
approach = get_ai_approach(classification, pain_points)
annual_hours, hours_saved, cost_savings, reduction = estimate_impact(time_per, volume, classification)
complexity, complexity_desc = assess_complexity(performer, pain_points, volume)
risks = generate_risks(pain_points, classification, performer)
strengths = generate_strengths(pain_points, score, volume, classification)

# ─────────────────────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Assessment Results</div>', unsafe_allow_html=True)

# Process context
st.caption(f"**{process_name}** · {domain} · {performer} · {frequency} · ~{time_per} min/instance · {volume}/month")

# Score + Classification
col1, col2 = st.columns([1, 1.5])

with col1:
    if score >= 70:
        gauge_color = "#27ae60"
    elif score >= 45:
        gauge_color = "#cc0000"
    else:
        gauge_color = "#f39c12"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "AI Opportunity Score", 'font': {'size': 16, 'family': 'Source Sans Pro'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': gauge_color},
            'bgcolor': "white",
            'steps': [
                {'range': [0, 40], 'color': '#f0f0f0'},
                {'range': [40, 65], 'color': '#fff3e0'},
                {'range': [65, 100], 'color': '#e8f5e9'}
            ],
            'threshold': {
                'line': {'color': gauge_color, 'width': 3},
                'thickness': 0.8, 'value': score
            }
        }
    ))
    fig.update_layout(height=250, margin=dict(l=30, r=30, t=50, b=10),
                      paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Source Sans Pro"))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown(f"""
    <div class="result-card">
        <h4>{classification}</h4>
        <p style="font-size: 0.9rem; color: #444; line-height: 1.6;">{class_desc}</p>
    </div>
    """, unsafe_allow_html=True)

# AI Approach
st.markdown('<div class="section-header">Recommended AI Approach</div>', unsafe_allow_html=True)

col_a1, col_a2 = st.columns(2)
with col_a1:
    st.markdown(f"""
    <div class="result-card">
        <h4>Technology</h4>
        <p style="font-size: 0.9rem; color: #444;">{approach['technology']}</p>
    </div>
    """, unsafe_allow_html=True)
with col_a2:
    st.markdown(f"""
    <div class="result-card">
        <h4>AI Interaction Model</h4>
        <p style="font-size: 0.9rem; color: #444;">{approach['copilot_fit']}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div class="result-card">
    <h4>How It Works</h4>
    <p style="font-size: 0.9rem; color: #444; line-height: 1.6;">{approach['description']}</p>
</div>
""", unsafe_allow_html=True)

# Impact Estimate
st.markdown('<div class="section-header">Impact Estimate</div>', unsafe_allow_html=True)

col_i1, col_i2, col_i3, col_i4 = st.columns(4)
with col_i1:
    st.metric("Current Annual Hours", f"{annual_hours:,.0f}")
with col_i2:
    st.metric("Estimated Hours Saved", f"{hours_saved:,.0f}", delta=f"{reduction*100:.0f}% reduction")
with col_i3:
    st.metric("Est. Annual Savings", f"${cost_savings:,.0f}", delta="at $45/hr avg")
with col_i4:
    if cost_savings > 200000:
        roi = "Quick Win (< 6 months)"
    elif cost_savings > 50000:
        roi = "Medium-Term (6-12 months)"
    else:
        roi = "Long-Term (12+ months)"
    st.metric("ROI Timeline", roi)

# Complexity
st.markdown('<div class="section-header">Implementation Complexity</div>', unsafe_allow_html=True)

complexity_color = {"Low": "#27ae60", "Medium": "#f39c12", "High": "#cc0000"}.get(complexity, "#888")
st.markdown(f"""
<div class="result-card" style="border-left-color: {complexity_color};">
    <h4>Complexity: {complexity}</h4>
    <p style="font-size: 0.9rem; color: #444;">{complexity_desc}</p>
</div>
""", unsafe_allow_html=True)

# Strengths
if strengths:
    st.markdown('<div class="section-header">Strengths & Accelerators</div>', unsafe_allow_html=True)
    for s in strengths:
        st.markdown(f'<div class="strength-flag">{s}</div>', unsafe_allow_html=True)

# Risks
if risks:
    st.markdown('<div class="section-header">Risk Flags & Considerations</div>', unsafe_allow_html=True)
    for r in risks:
        st.markdown(f'<div class="risk-flag">{r}</div>', unsafe_allow_html=True)

# Implementation Roadmap
st.markdown('<div class="section-header">Implementation Roadmap</div>', unsafe_allow_html=True)

if complexity == "Low":
    phases = [
        ("Phase 1 — Discovery & Requirements", "2-3 weeks", "Process assessment, data audit, stakeholder alignment, success criteria definition."),
        ("Phase 2 — Build & Configure", "3-4 weeks", "Configure AI model/rules, build user interface, integrate with existing systems."),
        ("Phase 3 — Validate & Test", "2-3 weeks", "Parallel run alongside current process, accuracy testing, user acceptance testing."),
        ("Phase 4 — Go-Live & Monitor", "2-3 weeks", "Controlled rollout, KPI monitoring, feedback collection, optimization."),
    ]
elif complexity == "High":
    phases = [
        ("Phase 1 — Discovery & Data Validation", "4-6 weeks", "Comprehensive process assessment, data quality audit, governance framework, legal and compliance review."),
        ("Phase 2 — Model Development & Integration", "6-8 weeks", "Develop AI models, configure business rules, build reviewer interface, system integration and API development."),
        ("Phase 3 — Parallel Run & Validation", "8-12 weeks", "Shadow mode deployment alongside manual process, daily accuracy comparison, fairness audit, model refinement."),
        ("Phase 4 — Controlled Go-Live", "4-6 weeks", "Phased rollout starting with low-risk segment, training, monitoring, exception handling optimization."),
        ("Phase 5 — Optimization & Scaling", "Ongoing", "Performance monitoring, model retraining, expansion to additional use cases, continuous improvement."),
    ]
else:
    phases = [
        ("Phase 1 — Discovery & Requirements", "3-4 weeks", "Process assessment, data audit, stakeholder alignment, success criteria definition, governance framework."),
        ("Phase 2 — Build & Configure", "4-6 weeks", "Develop AI model/rules, build user interface, integrate with existing systems, configure routing logic."),
        ("Phase 3 — Parallel Run & Validation", "4-6 weeks", "Shadow mode deployment, accuracy testing, user acceptance testing, model refinement."),
        ("Phase 4 — Go-Live & Monitor", "3-4 weeks", "Controlled rollout, training, KPI monitoring, feedback collection, optimization."),
    ]

for title, timeline, desc in phases:
    st.markdown(f"""
    <div class="phase-card">
        <strong>{title}</strong> <span style="color: #888; font-size: 0.85rem;">— {timeline}</span><br>
        <span style="font-size: 0.9rem; color: #444;">{desc}</span>
    </div>
    """, unsafe_allow_html=True)

total_low = sum(int(t.split("-")[0]) for _, t, _ in phases if t != "Ongoing")
total_high = sum(int(t.split("-")[1].split()[0]) for _, t, _ in phases if t != "Ongoing")
st.caption(f"Estimated total duration: **{total_low}-{total_high} weeks**")

# Governance Note
st.markdown('<div class="section-header">Governance & Responsible AI</div>', unsafe_allow_html=True)
st.markdown("""
<div class="result-card">
    <p style="font-size: 0.9rem; color: #444; line-height: 1.7;">
    All AI-enabled features should be governed with full audit trails, human-in-the-loop review during initial
    deployment, and regular model performance monitoring. AI recommendations must be transparent and explainable.
    Enterprise AI, data privacy, and security policies apply. Use case documentation should be maintained for
    governance review, including purpose, scope, data inputs, user impacts, and controls.
    </p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer-note">
    <strong>AI Opportunity Identifier</strong> · Enterprise Process Assessment · v1.0<br>
    Built by Hammad Mirza · Portfolio Project · June 2026<br>
    <em>This tool is a portfolio demonstration. All scenarios and estimates are illustrative.</em>
</div>
""", unsafe_allow_html=True)
