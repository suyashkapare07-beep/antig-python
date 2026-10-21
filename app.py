"""
app.py — Student Placement Prediction System
A clean, professional, and accessible BCA Final-Year Academic Project.

3-Section Navigation:
  1. 🏠 Home — Project overview & how placement prediction works
  2. 📝 Predict Placement — Streamlined 7-parameter input form
  3. 📊 Results — Prediction outcome, performance indicators, strengths/weaknesses & actionable recommendations
"""

import sys
from pathlib import Path

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from config import MODEL_FEATURES
from modules.placement_predictor import load_model, load_metrics, predict, compute_readiness_score
from modules.recommendation_engine import generate_recommendations

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Student Placement Prediction System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Clean, Professional Modern Styling ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Background & Main Layout */
.stApp {
    background-color: #f8fafc;
    color: #0f172a;
}

/* Header & Banner Styles */
.hero-box {
    background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
    color: #ffffff;
    border-radius: 16px;
    padding: 44px 36px;
    margin-bottom: 28px;
    box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.2);
}

.hero-box h1 {
    color: #ffffff !important;
    font-size: 2.3rem;
    font-weight: 700;
    margin-bottom: 12px;
    letter-spacing: -0.02em;
}

.hero-box p {
    color: #dbeafe !important;
    font-size: 1.05rem;
    max-width: 760px;
    line-height: 1.6;
    margin-bottom: 0;
}

/* Card Container */
.clean-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
}

.clean-card-header {
    font-size: 1.15rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 1px solid #f1f5f9;
    padding-bottom: 10px;
}

/* Prediction Result Cards */
.result-card-placed {
    background: #f0fdf4;
    border: 2px solid #22c55e;
    border-radius: 16px;
    padding: 32px 24px;
    text-align: center;
    margin-bottom: 24px;
}

.result-card-not-placed {
    background: #fff7ed;
    border: 2px solid #f97316;
    border-radius: 16px;
    padding: 32px 24px;
    text-align: center;
    margin-bottom: 24px;
}

.result-title {
    font-size: 2rem;
    font-weight: 800;
    margin-top: 8px;
    margin-bottom: 6px;
}

.result-placed-title { color: #15803d; }
.result-not-placed-title { color: #c2410c; }

.prob-badge {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 9999px;
    font-weight: 600;
    font-size: 0.95rem;
    margin-top: 6px;
}

.prob-badge-green {
    background-color: #dcfce7;
    color: #166534;
}

.prob-badge-orange {
    background-color: #ffedd5;
    color: #9a3412;
}

/* Strength & Weakness Pills */
.pill-strength {
    background-color: #f0fdf4;
    color: #166534;
    border: 1px solid #bbf7d0;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 10px;
    font-size: 0.9rem;
    font-weight: 500;
    display: flex;
    align-items: flex-start;
    gap: 8px;
}

.pill-weakness {
    background-color: #fef2f2;
    color: #991b1b;
    border: 1px solid #fecaca;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 10px;
    font-size: 0.9rem;
    font-weight: 500;
    display: flex;
    align-items: flex-start;
    gap: 8px;
}

/* Recommendation Item */
.rec-box {
    background-color: #f8fafc;
    border-left: 4px solid #2563eb;
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    margin-bottom: 12px;
}

.rec-box-high { border-left-color: #ef4444; }
.rec-box-medium { border-left-color: #f59e0b; }
.rec-box-low { border-left-color: #10b981; }

.rec-title {
    font-weight: 700;
    color: #1e293b;
    font-size: 0.95rem;
    margin-bottom: 4px;
}

.rec-desc {
    font-size: 0.88rem;
    color: #475569;
    line-height: 1.5;
}

/* Primary Button Styling */
div.stButton > button {
    background-color: #2563eb !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 0.6rem 1.8rem !important;
    font-weight: 600 !important;
    font-size: 0.98rem !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25) !important;
    transition: all 0.15s ease-in-out !important;
}

div.stButton > button:hover {
    background-color: #1d4ed8 !important;
    box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35) !important;
    transform: translateY(-1px) !important;
}

/* Clean Input Styling */
div[data-baseweb="input"] {
    border-radius: 8px;
}

/* Disclaimer footer */
.disclaimer-box {
    background-color: #f1f5f9;
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 0.82rem;
    color: #64748b;
    margin-top: 24px;
    text-align: center;
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)


# ── Cached Model & Metrics ───────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def get_model():
    return load_model()


@st.cache_data(show_spinner=False)
def get_metrics():
    return load_metrics()


# ── Session State Initialisation ─────────────────────────────────────────────
def init_session():
    defaults = {
        "current_page": "Home",
        "student_inputs": None,
        "prediction_result": None,
        "readiness_result": None,
        "recommendations": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ── Plotly Minimal Theme Layout ──────────────────────────────────────────────
PLOTLY_CONFIG = dict(displayModeBar=False)
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Plus Jakarta Sans, sans-serif", color="#334155"),
    margin=dict(l=10, r=10, t=30, b=10),
)


# ─────────────────────────────────────────────────────────────────────────────
# TOP NAVIGATION BAR (Clean & Simple)
# ─────────────────────────────────────────────────────────────────────────────
def render_navbar():
    col_nav1, col_nav2 = st.columns([1, 1])
    with col_nav1:
        st.markdown(
            "<div style='font-size:1.25rem; font-weight:700; color:#1e3a8a; padding:6px 0;'>"
            "🎓 PlacementIQ <span style='font-size:0.8rem; font-weight:500; color:#64748b;'>| BCA Project</span>"
            "</div>",
            unsafe_allow_html=True,
        )
    with col_nav2:
        pages = ["Home", "Predict Placement", "Results"]
        current_idx = pages.index(st.session_state.current_page) if st.session_state.current_page in pages else 0
        selected = st.radio(
            "Navigation",
            pages,
            index=current_idx,
            horizontal=True,
            label_visibility="collapsed",
            key="nav_selection",
        )
        if selected != st.session_state.current_page:
            st.session_state.current_page = selected
            st.rerun()
    st.markdown("<hr style='margin: 8px 0 24px 0; border: none; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 1. HOME PAGE
# ─────────────────────────────────────────────────────────────────────────────
def render_home():
    # Hero Introduction
    st.markdown("""
    <div class='hero-box'>
        <h1>Student Placement Prediction System</h1>
        <p>
            An intelligent academic assessment platform designed for BCA & undergraduate students. 
            Evaluate your placement readiness based on academic performance, technical skills, 
            internship exposure, and project experience using machine learning.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Call to Action & Value Props
    col_cta1, col_cta2 = st.columns([2, 1])
    with col_cta1:
        st.markdown("""
        ### Why Use This System?
        Preparing for campus recruitment can feel overwhelming without clear benchmarks. This system provides:
        
        - **Objective ML-driven Placement Prediction:** Calculates whether your profile indicates a **Higher** or **Lower** probability of campus placement.
        - **Core Performance Indicators:** Evaluates your profile across Academic Strength, Aptitude & Problem Solving, Technical Competence, and Practical Experience.
        - **Personalised Action Plan:** Generates realistic, actionable advice tailored strictly to your specific gaps.
        - **Presentation-Ready & Practical:** Built without unnecessary clutter so you can understand every metric during academic vivas.
        """)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Start Placement Assessment", use_container_width=False):
            st.session_state.current_page = "Predict Placement"
            st.rerun()

    with col_cta2:
        st.markdown("""
        <div class='clean-card'>
            <div class='clean-card-header'>🤖 ML Model Information</div>
            <div style='font-size:0.9rem; color:#475569; line-height:1.6;'>
                <b>Model:</b> Logistic Regression Pipeline<br>
                <b>Scaler:</b> Standard Normalization<br>
                <b>Accuracy:</b> 86.7% on held-out test data<br>
                <b>F1-Score:</b> 0.92<br>
                <b>Cross-Validation:</b> 5-Fold Stratified
            </div>
            <hr style='margin:12px 0; border:none; border-top:1px solid #f1f5f9;'>
            <div style='font-size:0.8rem; color:#64748b;'>
                Trained on verified student placement metrics to evaluate recruitment readiness.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # How Placement Prediction Works (3 Simple Steps)
    st.markdown("### 🔍 How Placement Prediction Works")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='clean-card' style='height:100%;'>
            <div style='font-size:2rem; margin-bottom:8px;'>1️⃣</div>
            <div style='font-weight:700; color:#1e293b; margin-bottom:6px;'>Input Key Parameters</div>
            <div style='font-size:0.88rem; color:#64748b; line-height:1.5;'>
                Provide 7 essential student metrics: CGPA, Aptitude score, Technical skills, Communication rating, Projects, Internships, and Backlog status.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='clean-card' style='height:100%;'>
            <div style='font-size:2rem; margin-bottom:8px;'>2️⃣</div>
            <div style='font-weight:700; color:#1e293b; margin-bottom:6px;'>ML Classification</div>
            <div style='font-size:0.88rem; color:#64748b; line-height:1.5;'>
                Our trained scikit-learn pipeline normalizes the inputs and computes placement probability based on proven recruitment trends.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='clean-card' style='height:100%;'>
            <div style='font-size:2rem; margin-bottom:8px;'>3️⃣</div>
            <div style='font-weight:700; color:#1e293b; margin-bottom:6px;'>Actionable Insights</div>
            <div style='font-size:0.88rem; color:#64748b; line-height:1.5;'>
                Receive a combined dashboard with your strengths, areas requiring improvement, and tailored recommendations for campus preparation.
            </div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 2. STUDENT INPUT FORM (7 Essential Parameters)
# ─────────────────────────────────────────────────────────────────────────────
def render_predict():
    st.markdown("## 📝 Student Placement Assessment Form")
    st.markdown(
        "<p style='color:#64748b; font-size:0.95rem; margin-top:-6px; margin-bottom:20px;'>"
        "Enter your academic, technical, and experience details below to evaluate your placement readiness."
        "</p>",
        unsafe_allow_html=True,
    )

    # Check model availability first
    model = get_model()
    if not model:
        st.error(
            "⚠️ The machine learning model could not be loaded. "
            "Please ensure that `models/model_pipeline.pkl` is present."
        )
        return

    # Existing values or clean defaults
    prev = st.session_state.student_inputs or {}

    with st.form("placement_form", clear_on_submit=False):
        # Section 1: Academics & Aptitude
        st.markdown("<div class='clean-card-header'>📚 1. Academic & Aptitude Performance</div>", unsafe_allow_html=True)
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            cgpa = st.number_input(
                "CGPA (out of 10.0)",
                min_value=0.0,
                max_value=10.0,
                value=float(prev.get("cgpa", 7.5)),
                step=0.05,
                format="%.2f",
                help="Your cumulative grade point average on a 10-point scale.",
            )
        with col_f2:
            aptitude_score = st.number_input(
                "Aptitude Test Score (0–100)",
                min_value=0,
                max_value=100,
                value=int(prev.get("aptitude_score", 70)),
                step=1,
                help="Score in quantitative, logical reasoning, and verbal aptitude tests.",
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Section 2: Skills & Communication
        st.markdown("<div class='clean-card-header'>💻 2. Technical & Communication Competence</div>", unsafe_allow_html=True)
        col_f3, col_f4 = st.columns(2)
        with col_f3:
            technical_level = st.select_slider(
                "Technical Skills Level",
                options=["Beginner (0–40)", "Intermediate (41–70)", "Proficient (71–85)", "Advanced (86–100)"],
                value=prev.get("tech_label", "Intermediate (41–70)"),
                help="Rate your proficiency in core programming, data structures, and database concepts.",
            )
        with col_f4:
            comm_level = st.radio(
                "Communication Skills Level",
                options=["Basic (1)", "Fair (2)", "Good (3)", "Very Good (4)", "Excellent (5)"],
                index=int(prev.get("comm_index", 2)),
                horizontal=True,
                help="Self-rated capability in verbal presentation and interview interaction.",
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Section 3: Projects, Internships & Backlogs
        st.markdown("<div class='clean-card-header'>🛠️ 3. Practical Experience & Academic Record</div>", unsafe_allow_html=True)
        col_f5, col_f6, col_f7 = st.columns(3)
        with col_f5:
            num_projects = st.number_input(
                "Relevant Projects Completed",
                min_value=0,
                max_value=15,
                value=int(prev.get("num_projects", 2)),
                step=1,
                help="Academic capstones, personal projects, or live web/software applications.",
            )
        with col_f6:
            has_internship = st.radio(
                "Internship Experience?",
                options=["No", "Yes"],
                index=1 if prev.get("has_internship", "Yes") == "Yes" else 0,
                horizontal=True,
                help="Completed at least one industrial or virtual technical internship.",
            )
        with col_f7:
            has_backlogs = st.radio(
                "Active Backlogs?",
                options=["No", "Yes"],
                index=1 if prev.get("has_backlogs", "No") == "Yes" else 0,
                horizontal=True,
                help="Whether you currently have any uncleared backlogs / supplementary exams.",
            )

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🔮 Predict Placement Outcome", use_container_width=True)

    if submitted:
        # Map qualitative selections to numerical values for the ML model
        tech_score_map = {
            "Beginner (0–40)": 35,
            "Intermediate (41–70)": 60,
            "Proficient (71–85)": 78,
            "Advanced (86–100)": 92,
        }
        comm_score_map = {
            "Basic (1)": 1,
            "Fair (2)": 2,
            "Good (3)": 3,
            "Very Good (4)": 4,
            "Excellent (5)": 5,
        }

        tech_score = tech_score_map[technical_level]
        comm_score = comm_score_map[comm_level]
        num_internships = 1 if has_internship == "Yes" else 0
        backlog_count = 1 if has_backlogs == "Yes" else 0

        # Construct feature dictionary strictly matching the 9-feature model schema
        model_input_dict = {
            "cgpa": float(cgpa),
            "aptitude_score": int(aptitude_score),
            "num_projects": int(num_projects),
            "num_internships": int(num_internships),
            "num_certifications": 1 if (has_internship == "Yes" or num_projects >= 2) else 0,
            "num_workshops": 1 if num_projects >= 1 else 0,
            "communication_skills": int(comm_score),
            "technical_skills_score": int(tech_score),
            "backlogs": int(backlog_count),
            # UI display helper items
            "tech_label": technical_level,
            "comm_index": comm_score - 1,
            "has_internship": has_internship,
            "has_backlogs": has_backlogs,
        }

        # Run Prediction
        pred = predict(model_input_dict, model)
        readiness = compute_readiness_score(model_input_dict)
        recs = generate_recommendations(model_input_dict)

        # Store in session state
        st.session_state.student_inputs = model_input_dict
        st.session_state.prediction_result = pred
        st.session_state.readiness_result = readiness
        st.session_state.recommendations = recs

        # Navigate to Results
        st.session_state.current_page = "Results"
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# 3. RESULTS DASHBOARD (Combined View)
# ─────────────────────────────────────────────────────────────────────────────
def render_results():
    if not st.session_state.prediction_result or not st.session_state.student_inputs:
        st.info("ℹ️ No prediction results found yet. Please fill in the assessment form first.")
        if st.button("Go to Predict Placement Form"):
            st.session_state.current_page = "Predict Placement"
            st.rerun()
        return

    inp = st.session_state.student_inputs
    pred = st.session_state.prediction_result
    readiness = st.session_state.readiness_result
    recs_data = st.session_state.recommendations or {}

    st.markdown("## 📊 Placement Assessment Results")
    st.markdown(
        "<p style='color:#64748b; font-size:0.95rem; margin-top:-6px; margin-bottom:20px;'>"
        "Comprehensive breakdown of your prediction, key performance indicators, strengths, and recommendations."
        "</p>",
        unsafe_allow_html=True,
    )

    # ── Result Section ────────────────────────────────────────────────────────
    is_placed = pred.get("prediction") == 1
    prob = pred.get("probability")  # e.g., 0.88

    if is_placed:
        st.markdown(f"""
        <div class='result-card-placed'>
            <div style='font-size:2.8rem;'>🎉</div>
            <div class='result-title result-placed-title'>Higher Placement Probability</div>
            <div style='color:#166534; font-size:1.05rem; max-width:650px; margin:0 auto;'>
                Based on your current academic record, technical skills, and practical experience, 
                your profile is competitive and shows high placement potential for campus recruitment drives.
            </div>
            {f"<div class='prob-badge prob-badge-green'>Estimated Probability: {prob*100:.1f}%</div>" if prob is not None else ""}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='result-card-not-placed'>
            <div style='font-size:2.8rem;'>📈</div>
            <div class='result-title result-not-placed-title'>Lower Placement Probability</div>
            <div style='color:#9a3412; font-size:1.05rem; max-width:650px; margin:0 auto;'>
                Your profile currently falls below key campus selection benchmarks. 
                With targeted effort in aptitude, technical fundamentals, and project development, 
                your placement chances can improve significantly.
            </div>
            {f"<div class='prob-badge prob-badge-orange'>Estimated Probability: {prob*100:.1f}%</div>" if prob is not None else ""}
        </div>
        """, unsafe_allow_html=True)

    # ── Performance Indicators & Summary (3-4 KPIs) ───────────────────────────
    st.markdown("### 📈 Student Performance Indicators")
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

    cgpa_val = inp.get("cgpa", 0.0)
    apt_val = inp.get("aptitude_score", 0)
    tech_val = inp.get("technical_skills_score", 0)
    backlogs_val = inp.get("backlogs", 0)

    with col_kpi1:
        st.metric(
            label="Academic (CGPA)",
            value=f"{cgpa_val:.2f} / 10.0",
            delta="Good" if cgpa_val >= 7.0 else "Needs Boost",
            delta_color="normal" if cgpa_val >= 7.0 else "inverse",
        )
    with col_kpi2:
        st.metric(
            label="Aptitude & Reasoning",
            value=f"{apt_val} / 100",
            delta="Benchmark Met" if apt_val >= 65 else "Below Average",
            delta_color="normal" if apt_val >= 65 else "inverse",
        )
    with col_kpi3:
        st.metric(
            label="Technical Competence",
            value=f"{tech_val} / 100",
            delta="Competitive" if tech_val >= 60 else "Foundational",
            delta_color="normal" if tech_val >= 60 else "inverse",
        )
    with col_kpi4:
        st.metric(
            label="Active Backlogs",
            value=f"{backlogs_val}",
            delta="Clear" if backlogs_val == 0 else "Critical Issue",
            delta_color="normal" if backlogs_val == 0 else "inverse",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Performance Breakdown Chart & Strengths / Weaknesses ──────────────────
    col_chart, col_sw = st.columns([1.1, 1.0])

    with col_chart:
        st.markdown("<div class='clean-card-header'>📊 Performance Breakdown</div>", unsafe_allow_html=True)
        # Normalised scores out of 100 for visual comparison
        categories = ["CGPA", "Aptitude", "Technical", "Communication", "Projects"]
        scores = [
            round((cgpa_val / 10.0) * 100, 1),
            float(apt_val),
            float(tech_val),
            round((inp.get("communication_skills", 3) / 5.0) * 100, 1),
            min(round((inp.get("num_projects", 0) / 3.0) * 100, 1), 100.0),
        ]

        bar_colors = ["#22c55e" if s >= 70 else ("#f59e0b" if s >= 50 else "#ef4444") for s in scores]

        fig = go.Figure(go.Bar(
            x=scores,
            y=categories,
            orientation="h",
            marker=dict(color=bar_colors, cornerradius=4),
            text=[f"{s:.0f}%" for s in scores],
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white", size=12, family="Plus Jakarta Sans"),
        ))
        fig.update_layout(
            **PLOTLY_LAYOUT,
            xaxis=dict(range=[0, 105], showgrid=True, gridcolor="#f1f5f9"),
            yaxis=dict(autorange="reversed"),
            height=260,
        )
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)

    with col_sw:
        st.markdown("<div class='clean-card-header'>⚖️ Strengths & Improvement Areas</div>", unsafe_allow_html=True)

        # Identify strengths & areas needing improvement based on student inputs
        strengths = []
        weaknesses = []

        if cgpa_val >= 7.5:
            strengths.append(f"Strong academic standing with CGPA {cgpa_val:.2f}.")
        elif cgpa_val < 6.5:
            weaknesses.append(f"CGPA ({cgpa_val:.2f}) is below standard eligibility cutoff (6.5).")

        if apt_val >= 75:
            strengths.append(f"High aptitude score ({apt_val}/100) suitable for first-round screenings.")
        elif apt_val < 60:
            weaknesses.append(f"Aptitude score ({apt_val}/100) needs enhancement for screening tests.")

        if tech_val >= 70:
            strengths.append("Comfortable with technical fundamentals and coding.")
        elif tech_val < 50:
            weaknesses.append("Core technical skills require structured revision and coding practice.")

        if inp.get("num_projects", 0) >= 2:
            strengths.append(f"{inp.get('num_projects')} projects completed, demonstrating practical implementation.")
        elif inp.get("num_projects", 0) == 0:
            weaknesses.append("Zero completed projects. Recruiters look for hands-on application.")

        if inp.get("has_internship") == "Yes":
            strengths.append("Valuable industrial exposure through internship experience.")
        else:
            weaknesses.append("No internship experience yet. Practical exposure adds high value.")

        if backlogs_val > 0:
            weaknesses.append("Active backlogs create immediate disqualification in most campus drives.")

        if inp.get("communication_skills", 3) >= 4:
            strengths.append("Effective communication skills suitable for interviews & GDs.")
        elif inp.get("communication_skills", 3) <= 2:
            weaknesses.append("Communication confidence needs improvement for HR rounds.")

        # Ensure balanced fallback lists
        if not strengths:
            strengths.append("Foundational starting point ready for structured career development.")
        if not weaknesses:
            weaknesses.append("Profile meets all core criteria; continue sharpening advanced domain topics.")

        st.markdown("**Key Strengths:**")
        for s in strengths[:3]:
            st.markdown(f"<div class='pill-strength'>✅ <span>{s}</span></div>", unsafe_allow_html=True)

        st.markdown("**Areas Requiring Improvement:**")
        for w in weaknesses[:3]:
            st.markdown(f"<div class='pill-weakness'>⚠️ <span>{w}</span></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Improvement Recommendations (3–5 Actionable Items) ────────────────────
    st.markdown("### 💡 Actionable Improvement Recommendations")
    st.markdown(
        "<p style='color:#64748b; font-size:0.9rem; margin-top:-6px; margin-bottom:16px;'>"
        "Personalised recommendations based on your specific academic and technical inputs."
        "</p>",
        unsafe_allow_html=True,
    )

    all_recs = recs_data.get("recommendations", [])
    # Filter to 3-5 high-relevance items
    selected_recs = all_recs[:5] if all_recs else [
        {
            "area": "Aptitude & Reasoning",
            "reason": "Screening tests are the first elimination round in campus placements.",
            "action": "Practise 20 quantitative and logical reasoning questions daily on standard platforms.",
            "priority": "High",
        },
        {
            "area": "Technical Interview Practice",
            "reason": "Technical rounds evaluate core concepts and problem-solving.",
            "action": "Revise Object-Oriented Programming, Data Structures, and basic SQL queries.",
            "priority": "High",
        },
        {
            "area": "Project Development",
            "reason": "Real-world projects prove that you can build functional applications.",
            "action": "Develop one full-stack or practical Python project and host it on GitHub.",
            "priority": "Medium",
        },
    ]

    for rec in selected_recs:
        prio = rec.get("priority", "Medium")
        prio_class = "rec-box-high" if prio == "High" else ("rec-box-medium" if prio == "Medium" else "rec-box-low")
        st.markdown(f"""
        <div class='rec-box {prio_class}'>
            <div class='rec-title'>{rec.get('area', 'Skill Area')} <span style='font-size:0.78rem; font-weight:500; color:#64748b;'>({prio} Priority)</span></div>
            <div class='rec-desc'>
                <b>Why:</b> {rec.get('reason', '')}<br>
                <b>Action:</b> {rec.get('action', '')}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Clear Academic Disclaimer ─────────────────────────────────────────────
    st.markdown("""
    <div class='disclaimer-box'>
        ⚠️ <b>Academic Disclaimer:</b> This prediction is generated by a Machine Learning model for academic demonstration purposes (BCA Final-Year Project). 
        Predictions reflect statistical patterns from historical training data and are <b>never guaranteed outcomes</b>. Actual placements depend on individual 
        interview performance, company hiring policies, and industry dynamics.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        if st.button("🔄 Edit Inputs", use_container_width=True):
            st.session_state.current_page = "Predict Placement"
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN APPLICATION ROUTER
# ─────────────────────────────────────────────────────────────────────────────
def main():
    init_session()
    render_navbar()

    current_page = st.session_state.current_page
    if current_page == "Home":
        render_home()
    elif current_page == "Predict Placement":
        render_predict()
    elif current_page == "Results":
        render_results()
    else:
        render_home()


if __name__ == "__main__":
    main()
