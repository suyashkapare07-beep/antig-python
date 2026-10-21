# Student Placement Prediction System

> **BCA Final-Year Academic Project** — An interactive, machine learning–based placement prediction and student performance evaluation system built with Streamlit and scikit-learn.

---

## 🌟 Overview & Key Features

This project provides a **balanced, medium-level placement readiness assessment** tailored for college students, faculty evaluations, and viva presentations:

1. **Clean 3-Section Architecture**
   - **🏠 Home Page:** Project introduction, how placement prediction works, and clear call-to-action.
   - **📝 Predict Placement:** Streamlined student input form collecting 7 essential parameters without overwhelming the user.
   - **📊 Results Dashboard:** Consolidated results presenting predictions, key performance indicators, strengths/weaknesses, and personalised recommendations.

2. **Core Student Input Parameters**
   - **Academic Performance:** CGPA (0.0 to 10.0 scale)
   - **Aptitude Test Score:** Quantitative & logical reasoning score (0 to 100)
   - **Technical Skills Level:** Beginner, Intermediate, Proficient, or Advanced
   - **Communication Skills:** 5-point scale (Basic to Excellent)
   - **Internship Experience:** Yes / No
   - **Projects Completed:** Number of relevant academic or personal projects
   - **Active Backlogs:** Yes / No

3. **Machine Learning Placement Prediction**
   - Evaluates probability using a trained **Logistic Regression Pipeline** (StandardScaler + Classifier).
   - Classifies outcome into **Higher Placement Probability** or **Lower Placement Probability**.
   - Displays estimated placement probability percentage.
   - Includes transparent academic disclaimers (predictions are estimates, never guarantees).

4. **Student Performance Analysis & Strengths/Weaknesses**
   - 4 Key Performance Indicators (Academics, Aptitude, Technical Competence, Backlogs).
   - Visual performance breakdown chart across all key dimensions.
   - Automatic identification of student-specific strengths and areas needing improvement.

5. **Actionable Improvement Recommendations**
   - 3 to 5 targeted recommendations mapped directly to the student's input values.
   - Covers aptitude practice, technical problem-solving, project portfolio development, and communication skills.

---

## 🗂️ Project Structure

```
antig/
├── app.py                         # Streamlined 3-section Streamlit application
├── config.py                      # Model feature mappings and threshold settings
├── requirements.txt               # Project dependencies
├── README.md                      # Project documentation
├── models/
│   ├── model_pipeline.pkl         # Trained scikit-learn pipeline
│   └── metrics.json               # Model evaluation metrics (86.7% accuracy, 0.92 F1)
├── data/
│   ├── dataset.csv                # Student placement dataset
│   └── generate_dataset.py        # Dataset generation script
├── training/
│   └── train_model.py             # Model training & 5-fold evaluation script
├── modules/
│   ├── placement_predictor.py     # Model loading, validation, and inference
│   └── recommendation_engine.py   # Actionable advice and recommendation engine
└── tests/
    ├── test_prediction.py         # Unit tests for prediction logic
    ├── test_eligibility.py        # Unit tests for eligibility criteria
    └── test_resume_parser.py      # Unit tests for parser utilities
```

---

## ⚙️ Quick Start Guide

### 1. Set Up Environment
```bash
# Clone or download the project
cd antig

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. (Optional) Re-train the Machine Learning Model
The repository already includes the pre-trained pipeline in `models/model_pipeline.pkl`. If you wish to retrain:
```bash
python data/generate_dataset.py
python training/train_model.py
```

### 3. Launch the Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🤖 Machine Learning Model Summary

| Metric | Result |
|---|---|
| **Algorithm** | Logistic Regression with Standard Scaler |
| **Test Accuracy** | **86.7%** on held-out test data |
| **F1-Score** | **0.92** |
| **Validation** | 5-Fold Stratified Cross-Validation |
| **Key Influencing Factors** | CGPA, Aptitude Score, Technical Skills, Backlogs, Internships |
