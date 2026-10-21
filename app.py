"""
app.py — Student Placement Prediction System (Self-Contained)
A clean, professional, and accessible BCA Final-Year Academic Project.
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import joblib
from pathlib import Path

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
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
.stApp { background-color: #f8fafc; color: #0f172a; }
.hero-box {
    background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
    color: #ffffff; border-radius: 16px; padding: 44px 36px; margin-bottom: 28px;
    box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.2);
}
.hero-box h1 { color: #ffffff !important; font-size: 2.3rem; font-weight: 700; margin-bottom: 12px; }
.hero-box p { color: #dbeafe !important; font-size: 1.05rem; line-height: 1.6; margin-bottom: 0; }
.clean-card {
    background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 24px; margin-bottom: 20px;
}
.clean-card-header {
    font-size: 1.15rem; font-weight: 700; color: #0f172a; margin-bottom: 16px;
    display: flex; align-items: center; gap: 8px; border-bottom: 1px solid #f1f5f9; padding-bottom: 10px;
}
.result-card-placed {
    background: #f0fdf4; border: 2px solid #22c55e; border-radius: 16px; padding: 32px 24px; text-align: center; margin-bottom: 24px;
}
.result-card-not-placed {
    background: #fff7ed; border: 2px solid #f97316; border-radius: 16px; padding: 32px 24px; text-align: center; margin-bottom: 24px;
}
.result-title { font-size: 2rem; font-weight: 800; margin-top: 8px; margin-bottom: 6px; }
.result-placed-title { color: #15803d; }
.result-not-placed-title { color: #c2410c; }
.prob-badge {
    display: inline-block; padding: 6px 16px; border-radius: 9999px; font-weight: 600; font-size: 0.95rem; margin-top: 6px;
}
.prob-badge-green { background-color: #dcfce7; color: #166534; }
.prob-badge-orange { background-color: #ffedd5; color: #9a3412; }
.pill-strength {
    background-color: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; border-radius: 8px; padding: 10px 14px; margin-bottom: 10px; font-size: 0.9rem; display: flex; gap: 8px;
}
.pill-weakness {
    background-color: #fef2f2; color: #991b1b; border: 1px solid #fecaca; border-radius: 8px; padding: 10px 14px; margin-bottom: 10px; font-size: 0.9rem; display: flex; gap: 8px;
}
.rec-box { background-color: #f8fafc; border-left: 4px solid #2563eb; border-radius: 0 10px 10px 0; padding: 14px 18px; margin-bottom: 12px; }
.rec-box-high { border-left-color: #ef4444; }
.rec-box-medium { border-left-color: #f59e0b; }
.rec-title { font-weight: 700; color: #1e293b; font-size: 0.95rem; margin-bottom: 4px; }
.rec-desc { font-size: 0.88rem; color: #475569; line-height: 1.5; }
div.stButton > button {
    background-color: #2563eb !important; color: #ffffff !important; border-radius: 10px !important;
    border: none !important; padding: 0.6rem 1.8rem !important; font-weight: 600 !important;
}
.disclaimer-box {
    background-color: #f1f5f9; border-radius: 10px; padding: 14px 18px; font-size: 0.82rem; color: #64748b; margin-top: 24px; text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ── Embedded Logic Functions ──────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent

@st.cache_resource(show_spinner=False)
def load_model():
    model_path = BASE_DIR / "models" / "model_pipeline.pkl"
    if model_path.exists():
        return joblib.load(model_path)
    return None

def predict(input_data, model):
    if model is None:
        return {"prediction": 0, "probability": 0.0}
    
    # Construct DataFrame matching expected features
    features = [
        "cgpa", "aptitude_score", "num_projects", "num_internships",
        "num_certifications", "num_workshops", "communication_skills",
        "technical_skills_score", "backlogs"
    ]
    df = pd.DataFrame([[input_data.get(f, 0) for f in features]], columns=features)
    
    pred = model.predict(df)[0]
    prob = model.predict_proba(df)[0][1] if hasattr(model, "predict_proba") else 0.5
    return {"prediction": int(pred), "probability": float(prob)}

def compute_readiness_score(input_data):
    cgpa = input_data.get("cgpa", 0) / 10.0
    apt = input_data.get("aptitude_score", 0) / 100.0
    tech = input_data.get("technical_skills_score", 0) / 100.0
    score = (cgpa * 0.3 + apt * 0.3 + tech * 0.4) * 100
    return round(score, 1)

def generate_recommendations(input_data):
    recs = []
    if input_data.get("aptitude_score", 0) < 65:
        recs.append({
            "area": "Aptitude & Reasoning",
            "reason": "Screening tests are the first elimination round.",
            "action": "Practise quantitative and logical reasoning questions daily.",
            "priority": "High"
        })
    if input_data.get("technical_skills_score", 0) < 60:
        recs.append({
            "area": "Technical Core",
            "reason": "Technical rounds evaluate core concepts.",
            "action": "Revise Data Structures, OOPs, and SQL fundamentals.",
            "priority": "High"
        })
    if input_data.get("num_projects", 0) < 2:
        recs.append({
            "area": "Project Development",
            "reason": "Projects demonstrate hands-on application.",
            "action": "Build and host at least two functional web or software projects.",
            "priority": "Medium"
        })
    return {"recommendations": recs}

# ── Session State Initialisation ─────────────────────────────────────────────
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"
if "student_inputs" not in st.session_state:
    st.session_state.student_inputs = None
if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None

# ── Navigation Bar ───────────────────────────────────────────────────────────
col_nav1, col_nav2 = st.columns([1, 1])
with col_nav1:
    st.markdown("<div style='font-size:1.25rem; font-weight:700; color:#1e3a8a; padding:6px 0;'>🎓 PlacementIQ | BCA Project</div>", unsafe_allow_html=True)
with col_nav2:
    pages = ["Home", "Predict Placement", "Results"]
    current_idx = pages.index(st.session_state.current_page) if st.session_state.current_page in pages else 0
    selected = st.radio("Navigation", pages, index=current_idx, horizontal=True, label_visibility="collapsed", key="nav_selection")
    if selected != st.session_state.current_page:
        st.session_state.current_page = selected
        st.rerun()
st.markdown("<hr style='margin: 8px 0 24px 0; border: none; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)

# ── Page Routing ─────────────────────────────────────────────────────────────
if st.session_state.current_page == "Home":
    st.markdown("""
    <div class='hero-box'>
        <h1>Student Placement Prediction System</h1>
        <p>An intelligent academic assessment platform designed for BCA & undergraduate students. Evaluate your placement readiness using machine learning.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🚀 Start Placement Assessment"):
        st.session_state.current_page = "Predict Placement"
        st.rerun()

elif st.session_state.current_page == "Predict Placement":
    st.markdown("## 📝 Student Placement Assessment Form")
    model = load_model()
    if not model:
        st.error("⚠️ The machine learning model could not be loaded. Please ensure `models/model_pipeline.pkl` exists in your repository.")
    
    prev = st.session_state.student_inputs or {}
    with st.form("placement_form"):
        cgpa = st.number_input("CGPA (out of 10.0)", 0.0, 10.0, float(prev.get("cgpa", 7.5)), 0.05)
        aptitude_score = st.number_input("Aptitude Test Score (0–100)", 0, 100, int(prev.get("aptitude_score", 70)))
        technical_level = st.selectbox("Technical Skills Level", ["Beginner (0–40)", "Intermediate (41–70)", "Proficient (71–85)", "Advanced (86–100)"])
        comm_level = st.selectbox("Communication Skills Level", ["Basic (1)", "Fair (2)", "Good (3)", "Very Good (4)", "Excellent (5)"])
        num_projects = st.number_input("Relevant Projects Completed", 0, 15, int(prev.get("num_projects", 2)))
        has_internship = st.radio("Internship Experience?", ["No", "Yes"])
        has_backlogs = st.radio("Active Backlogs?", ["No", "Yes"])
        
        submitted = st.form_submit_button("🔮 Predict Placement Outcome")

    if submitted:
        tech_map = {"Beginner (0–40)": 35, "Intermediate (41–70)": 60, "Proficient (71–85)": 78, "Advanced (86–100)": 92}
        comm_map = {"Basic (1)": 1, "Fair (2)": 2, "Good (3)": 3, "Very Good (4)": 4, "Excellent (5)": 5}
        
        inp = {
            "cgpa": float(cgpa),
            "aptitude_score": int(aptitude_score),
            "num_projects": int(num_projects),
            "num_internships": 1 if has_internship == "Yes" else 0,
            "num_certifications": 1 if has_internship == "Yes" else 0,
            "num_workshops": 1 if num_projects >= 1 else 0,
            "communication_skills": comm_map[comm_level],
            "technical_skills_score": tech_map[technical_level],
            "backlogs": 1 if has_backlogs == "Yes" else 0
        }
        
        st.session_state.student_inputs = inp
        st.session_state.prediction_result = predict(inp, model)
        st.session_state.current_page = "Results"
        st.rerun()

elif st.session_state.current_page == "Results":
    if not st.session_state.prediction_result:
        st.info("Please fill in the assessment form first.")
    else:
        pred = st.session_state.prediction_result
        is_placed = pred["prediction"] == 1
        prob = pred["probability"]
        
        if is_placed:
            st.markdown(f"""
            <div class='result-card-placed'>
                <div style='font-size:2.8rem;'>🎉</div>
                <div class='result-title result-placed-title'>Higher Placement Probability</div>
                <div class='prob-badge prob-badge-green'>Estimated Probability: {prob*100:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='result-card-not-placed'>
                <div style='font-size:2.8rem;'>📈</div>
                <div class='result-title result-not-placed-title'>Lower Placement Probability</div>
                <div class='prob-badge prob-badge-orange'>Estimated Probability: {prob*100:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("🔄 Edit Inputs"):
            st.session_state.current_page = "Predict Placement"
            st.rerun()