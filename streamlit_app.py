import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import random
import time

# Page configuration
st.set_page_config(
    page_title="DiabetCare - Complete Wellness Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session state initialization
if 'water_intake' not in st.session_state:
    st.session_state.water_intake = 0
if 'exercise_done' not in st.session_state:
    st.session_state.exercise_done = False
if 'streak_days' not in st.session_state:
    st.session_state.streak_days = 0
if 'total_points' not in st.session_state:
    st.session_state.total_points = 0
if 'meditation_time' not in st.session_state:
    st.session_state.meditation_time = 0
if 'games_played' not in st.session_state:
    st.session_state.games_played = 0
if 'high_score' not in st.session_state:
    st.session_state.high_score = 0

# Enhanced CSS with game animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

    /* ── Global – large readable text for all ages ── */
    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif !important;
        font-size: 20px !important;
        color: #1a1a2e !important;
    }

    /* Sidebar bigger text */
    section[data-testid="stSidebar"] * {
        font-size: 18px !important;
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMetric label {
        font-size: 20px !important;
        font-weight: 700 !important;
    }

    /* All labels, inputs, sliders bigger */
    label, .stTextInput label, .stNumberInput label,
    .stSelectbox label, .stSlider label {
        font-size: 20px !important;
        font-weight: 700 !important;
        color: #1a1a2e !important;
    }
    input, select, textarea {
        font-size: 20px !important;
        padding: 12px !important;
    }

    /* Big bold buttons */
    .stButton > button {
        background: #1a56db !important;
        color: #ffffff !important;
        font-size: 20px !important;
        font-weight: 800 !important;
        padding: 18px 36px !important;
        border-radius: 16px !important;
        border: none !important;
        box-shadow: 0 6px 20px rgba(26,86,219,0.35) !important;
        transition: all 0.2s ease !important;
        width: 100%;
    }
    .stButton > button:hover {
        background: #1e40af !important;
        box-shadow: 0 8px 28px rgba(26,86,219,0.5) !important;
        transform: translateY(-2px) !important;
    }

    /* Main title */
    .main-title {
        font-size: 3.8rem !important;
        font-weight: 900;
        color: #1a1a2e !important;
        text-align: center;
        letter-spacing: -1px;
        margin-bottom: 0.3rem;
    }
    .main-title span { color: #1a56db; }

    /* Cards – white, strong border, big padding */
    .feature-card {
        background: #ffffff;
        padding: 28px 32px;
        border-radius: 20px;
        border-left: 8px solid #1a56db;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin: 16px 0;
        font-size: 19px;
        color: #1a1a2e;
    }
    .feature-card h2, .feature-card h3 { color: #1a1a2e; font-weight: 800; }

    .game-card {
        background: #1a56db;
        padding: 32px;
        border-radius: 20px;
        color: #ffffff;
        text-align: center;
        box-shadow: 0 6px 24px rgba(26,86,219,0.4);
        margin: 16px 0;
        font-size: 19px;
    }
    .game-card h3, .game-card h4 { color: #ffffff; font-weight: 800; }

    .meditation-card {
        background: #ecfdf5;
        border: 3px solid #059669;
        padding: 28px;
        border-radius: 20px;
        margin: 16px 0;
        font-size: 19px;
        color: #064e3b;
    }

    .info-box {
        background: #eff6ff;
        border-left: 8px solid #1a56db;
        padding: 24px 28px;
        border-radius: 16px;
        margin: 20px 0;
        font-size: 19px;
        color: #1e3a8a;
    }

    .warning-box {
        background: #fffbeb;
        border-left: 8px solid #d97706;
        padding: 24px 28px;
        border-radius: 16px;
        margin: 20px 0;
        font-size: 19px;
        color: #78350f;
    }

    .risk-card-high {
        background: #dc2626;
        color: #ffffff;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        font-size: 22px;
        font-weight: 700;
        box-shadow: 0 8px 30px rgba(220,38,38,0.4);
    }
    .risk-card-medium {
        background: #d97706;
        color: #ffffff;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        font-size: 22px;
        font-weight: 700;
        box-shadow: 0 8px 30px rgba(217,119,6,0.4);
    }
    .risk-card-low {
        background: #059669;
        color: #ffffff;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        font-size: 22px;
        font-weight: 700;
        box-shadow: 0 8px 30px rgba(5,150,105,0.4);
    }

    .breathing-circle {
        width: 220px;
        height: 220px;
        background: #1a56db;
        border-radius: 50%;
        margin: 30px auto;
        animation: breathe 4s ease-in-out infinite;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.6rem;
        font-weight: 800;
    }
    @keyframes breathe {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.28); }
    }

    .zen-quote {
        background: #fef3c7;
        border: 3px solid #d97706;
        padding: 28px;
        border-radius: 16px;
        text-align: center;
        font-size: 1.3rem;
        font-style: italic;
        color: #78350f;
        margin: 20px 0;
        font-weight: 600;
    }

    .music-player {
        background: #f0fdf4;
        border: 3px solid #059669;
        padding: 24px;
        border-radius: 16px;
        margin: 16px 0;
        font-size: 19px;
        color: #064e3b;
    }

    .timer-display {
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        color: #1a56db;
        margin: 20px 0;
    }

    /* Metrics larger */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        color: #1a1a2e !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 1.1rem !important;
        font-weight: 700 !important;
    }

    /* Headers */
    h1 { font-size: 2.5rem !important; font-weight: 900 !important; color: #1a1a2e !important; }
    h2 { font-size: 2rem !important; font-weight: 800 !important; color: #1a1a2e !important; }
    h3 { font-size: 1.6rem !important; font-weight: 700 !important; color: #1a1a2e !important; }
    p, li { font-size: 1.15rem !important; line-height: 1.9 !important; color: #1a1a2e !important; }

    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    possible_paths = [
        "diabetes.csv",
        r"C:\diabetes.csv",
        r"C:\DiabetesApp\diabetes.csv",
        r"C:\Users\sucheta maurya\Downloads\diabetes.csv"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                return pd.read_csv(path), None
            except Exception as e:
                return None, f"Error: {str(e)}"
    
    return None, "Put diabetes.csv in same folder as app"

def symptoms_to_clinical(thirst, fatigue, urination, healing, vision, tingling, family_history, glucose_known=None, bp_known=None):
    """Convert symptom answers to estimated clinical values"""
    # Glucose estimate from symptoms
    if glucose_known:
        glucose = glucose_known
    else:
        base = 90
        base += thirst * 15       # 0-3 scale
        base += fatigue * 10
        base += urination * 12
        base += vision * 18
        glucose = min(base, 280)

    # BP estimate
    if bp_known:
        bp = bp_known
    else:
        bp = 70 + (thirst + fatigue) * 5

    # Insulin resistance proxy
    insulin = 50 + (fatigue * 30) + (tingling * 40)

    # Family history boosts risk directly
    family_bonus = family_history * 2

    return glucose, bp, insulin, family_bonus

def predict_diabetes(glucose, bmi, age, pregnancies, bp, insulin, family_bonus=0):
    risk_score = 0
    factors = []
    recs = []
    
    if glucose >= 200:
        risk_score += 4
        factors.append("🔴 Critical glucose level")
        recs.append("⚠️ Immediate medical consultation")
    elif glucose >= 140:
        risk_score += 3
        factors.append("🟠 High glucose level")
        recs.append("📞 Consult endocrinologist")
    elif glucose >= 100:
        risk_score += 1
        factors.append("🟡 Elevated glucose")
    
    if bmi >= 35:
        risk_score += 3
        factors.append(f"🔴 Severe obesity (BMI {bmi:.1f})")
    elif bmi >= 30:
        risk_score += 2
        factors.append(f"🟠 Obesity (BMI {bmi:.1f})")
    elif bmi >= 25:
        risk_score += 1
        factors.append(f"🟡 Overweight (BMI {bmi:.1f})")
    
    if age >= 65:
        risk_score += 2
        factors.append("🔴 Advanced age")
    elif age >= 45:
        risk_score += 1
        factors.append("🟡 Increased age risk")
    
    if pregnancies >= 5:
        risk_score += 2
    if bp >= 90:
        risk_score += 1
        factors.append("🟠 High blood pressure")
    if insulin >= 200:
        risk_score += 2
        factors.append("🟠 High insulin resistance")

    if family_bonus > 0:
        risk_score += family_bonus
        factors.append("🔴 Family history of diabetes")

    if risk_score >= 8:
        level = "HIGH"
        prob = min(0.92, 0.62 + (risk_score - 8) * 0.05)
    elif risk_score >= 5:
        level = "MEDIUM"
        prob = 0.38 + (risk_score - 5) * 0.08
    else:
        level = "LOW"
        prob = max(0.05, 0.12 + risk_score * 0.05)
    
    return level, prob, factors, recs, risk_score

def generate_report(name, age, glucose, bmi, level, prob, factors, recs):
    report = f"""
╔══════════════════════════════════════════════════════╗
║        DIABETCARE HEALTH ASSESSMENT REPORT           ║
╚══════════════════════════════════════════════════════╝

Patient: {name}
Date: {datetime.now().strftime('%B %d, %Y, %I:%M %p')}
Report ID: DC-{datetime.now().strftime('%Y%m%d%H%M%S')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PATIENT INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Age: {age} years | Glucose: {glucose} mg/dL | BMI: {bmi}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RISK ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Risk Level: {level} | Probability: {prob:.1%}

RISK FACTORS:
"""
    for f in factors:
        report += f"- {f}\n"
    
    report += f"\nRECOMMENDATIONS:\n"
    for r in recs:
        report += f"- {r}\n"
    
    report += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ DISCLAIMER: Educational tool only. NOT medical advice.
Consult healthcare professionals for diagnosis/treatment.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated by DiabetCare AI © 2024
"""
    return report

def main():
    st.markdown('<h1 class="main-title">🏥 <span>Diabet</span>Care</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;font-size:1.4rem;font-weight:700;color:#1a56db;letter-spacing:1px;">Complete Diabetes Wellness Platform</p>', 
                unsafe_allow_html=True)
    
    df, error = load_data()
    
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.selectbox("", 
        ["🏠 Home", "🔮 Risk Assessment", "💪 Exercise", 
         "🎮 Relaxation Games", "🧘 Meditation & Calm", 
         "📊 Data Insights", "🎯 Tracker", "🛍️ Shop"],
        label_visibility="collapsed")
    
    if df is not None:
        st.sidebar.markdown("---")
        st.sidebar.success("✅ Dataset Loaded!")
        st.sidebar.metric("Records", len(df))
    
    st.sidebar.markdown("---")
    st.sidebar.metric("🏆 Points", st.session_state.total_points)
    st.sidebar.metric("🔥 Streak", f"{st.session_state.streak_days} days")
    
    if page == "🏠 Home":
        show_home(df)
    elif page == "🔮 Risk Assessment":
        show_prediction(df)
    elif page == "💪 Exercise":
        show_exercise()
    elif page == "🎮 Relaxation Games":
        show_games()
    elif page == "🧘 Meditation & Calm":
        show_meditation()
    elif page == "📊 Data Insights":
        show_data(df)
    elif page == "🎯 Tracker":
        show_tracker()
    else:
        show_shop()

def show_home(df):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="feature-card">
        <h2>🌟 Welcome to DiabetCare!</h2>
        <p style="font-size:1.2rem;">Your complete wellness companion for diabetes prevention and emotional well-being.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
        <h3>✨ Complete Features</h3>
        <ul style="font-size:1.1rem;line-height:2;">
            <li><strong>🔮 AI Risk Assessment:</strong> Advanced diabetes prediction</li>
            <li><strong>💪 Exercise Library:</strong> Video tutorials & workout plans</li>
            <li><strong>🎮 Relaxation Games:</strong> Stress-relief games for anger management</li>
            <li><strong>🧘 Meditation Hub:</strong> Guided meditation with soothing music</li>
            <li><strong>😌 Calm Timer:</strong> Breathing exercises with visual guides</li>
            <li><strong>🎯 Daily Tracker:</strong> Water, sleep, exercise tracking</li>
            <li><strong>🏆 Rewards System:</strong> Points, streaks, achievements</li>
            <li><strong>📥 Health Reports:</strong> Download detailed assessments</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="game-card">
        <h3>🎮 New!</h3>
        <h4>Stress Relief Games</h4>
        <p>Combat diabetes-related stress & anger with fun, calming games!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="meditation-card">
        <h3>🧘 Meditation Hub</h3>
        <p>Guided meditation, breathing exercises & soothing music</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="warning-box">
    <h2>⚠️ MEDICAL DISCLAIMER</h2>
    <p><strong>Educational tool only. NOT medical advice.</strong></p>
    <p>Always consult healthcare professionals for medical decisions.</p>
    </div>
    """, unsafe_allow_html=True)

def show_prediction(df):
    st.header("🔮 Diabetes Risk Assessment")

    st.markdown("""
    <div class="info-box">
    <h4>💡 No lab tests needed!</h4>
    <p>Answer simple questions about your daily experiences. If you have a glucometer, you can optionally enter your reading for higher accuracy.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("prediction_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 👤 Basic Info")
            name = st.text_input("Your Name")
            age = st.number_input("🎂 Age", 18, 120, 30)
            gender = st.selectbox("⚧ Gender", ["Male", "Female", "Other"])
            pregnancies = st.number_input("🤱 Pregnancies (females)", 0, 20, 0)
            weight = st.number_input("⚖️ Weight (kg)", 30.0, 200.0, 70.0, 0.5)
            height = st.number_input("📏 Height (cm)", 100.0, 220.0, 165.0, 0.5)
            bmi = round(weight / ((height / 100) ** 2), 1)
            st.info(f"📊 Your BMI: **{bmi}**")

        with col2:
            st.markdown("#### 🩺 Symptoms (Everyone Knows These!)")
            thirst = st.select_slider("💧 How often do you feel very thirsty?",
                options=[0, 1, 2, 3],
                format_func=lambda x: ["Never", "Sometimes", "Often", "Always"][x])
            fatigue = st.select_slider("😴 Do you feel tired/fatigued, especially after meals?",
                options=[0, 1, 2, 3],
                format_func=lambda x: ["Never", "Sometimes", "Often", "Always"][x])
            urination = st.select_slider("🚻 Frequent urination (more than usual)?",
                options=[0, 1, 2, 3],
                format_func=lambda x: ["Never", "Sometimes", "Often", "Always"][x])
            healing = st.select_slider("🩹 Do cuts/wounds heal slowly?",
                options=[0, 1, 2, 3],
                format_func=lambda x: ["Never", "Sometimes", "Often", "Always"][x])
            vision = st.select_slider("👁️ Blurry vision or eye strain?",
                options=[0, 1, 2, 3],
                format_func=lambda x: ["Never", "Sometimes", "Often", "Always"][x])
            tingling = st.select_slider("🖐️ Tingling/numbness in hands or feet?",
                options=[0, 1, 2, 3],
                format_func=lambda x: ["Never", "Sometimes", "Often", "Always"][x])
            family_history = st.selectbox("👨‍👩‍👧 Family history of diabetes?",
                ["No", "1 parent/sibling", "Both parents"])
            family_bonus = [0, 1, 2][["No", "1 parent/sibling", "Both parents"].index(family_history)]

        st.markdown("#### 🩸 Optional: Got a Glucometer? (Leave 0 if not)")
        col3, col4 = st.columns(2)
        with col3:
            glucose_known = st.number_input("Blood Glucose (mg/dL) — 0 = I don't have this", 0, 500, 0)
        with col4:
            bp_known = st.number_input("Blood Pressure (mmHg) — 0 = I don't have this", 0, 200, 0)

        submit = st.form_submit_button("🔍 ANALYZE MY RISK", use_container_width=True)

        if submit and name:
            glucose, bp, insulin, _ = symptoms_to_clinical(
                thirst, fatigue, urination, healing, vision, tingling, family_bonus,
                glucose_known if glucose_known > 0 else None,
                bp_known if bp_known > 0 else None
            )
            level, prob, factors, recs, score = predict_diabetes(
                glucose, bmi, age, pregnancies, bp, insulin, family_bonus)
            
            st.markdown("---")
            
            if level == "HIGH":
                st.markdown(f"""
                <div class="risk-card-high">
                    <h1>⚠️ HIGH RISK</h1>
                    <h2>{prob:.1%}</h2>
                    <p>Immediate medical consultation recommended</p>
                </div>
                """, unsafe_allow_html=True)
            elif level == "MEDIUM":
                st.markdown(f"""
                <div class="risk-card-medium">
                    <h1>⚡ MODERATE RISK</h1>
                    <h2>{prob:.1%}</h2>
                    <p>Lifestyle changes recommended</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="risk-card-low">
                    <h1>✅ LOW RISK</h1>
                    <h2>{prob:.1%}</h2>
                    <p>Keep up healthy habits!</p>
                </div>
                """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 🎯 Risk Factors")
                for f in factors if factors else ["No major risks!"]:
                    st.markdown(f"- {f}")
            with col2:
                st.markdown("### 💡 Recommendations")
                for r in recs if recs else ["Continue healthy lifestyle"]:
                    st.markdown(f"- {r}")
            
            st.progress(min(score/12, 1.0))
            st.write(f"**Risk Score: {score}/12**")
            
            report = generate_report(name, age, glucose if glucose_known > 0 else f"~{glucose} (estimated)", bmi, level, prob, factors, recs)
            st.download_button("📥 Download Report", report,
                             f"Report_{name}_{datetime.now().strftime('%Y%m%d')}.txt",
                             use_container_width=True)

def show_games():
    st.header("🎮 Stress Relief & Relaxation Games")
    
    st.markdown("""
    <div class="info-box">
    <h3>🎯 Why Games for Diabetes Patients?</h3>
    <p style="font-size:1.1rem;">
    Diabetes can cause stress, frustration, and anger due to:
    </p>
    <ul style="font-size:1.05rem;">
        <li>Blood sugar fluctuations affecting mood</li>
        <li>Constant health monitoring causing anxiety</li>
        <li>Dietary restrictions leading to frustration</li>
        <li>Lifestyle changes causing emotional stress</li>
    </ul>
    <p style="font-size:1.1rem;">
    <strong>These games help:</strong> Reduce stress, improve mood, distract from anxiety, 
    and provide a healthy emotional outlet!
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Memory Game", "🎨 Color Therapy", "🧩 Puzzle Challenge", "🎵 Music Rhythm"])
    
    with tab1:
        show_memory_game()
    
    with tab2:
        show_color_therapy()
    
    with tab3:
        show_puzzle_game()
    
    with tab4:
        show_rhythm_game()

def show_memory_game():
    st.subheader("🎯 Calm Memory Match")
    st.write("Find matching pairs to calm your mind!")
    
    if 'memory_cards' not in st.session_state:
        emojis = ['🌸', '🌺', '🌻', '🌷', '🌹', '🌼', '🍀', '🌿']
        cards = emojis * 2
        random.shuffle(cards)
        st.session_state.memory_cards = cards
        st.session_state.revealed = [False] * 16
        st.session_state.first_pick = None
        st.session_state.matches = 0
    
    cols = st.columns(4)
    for i, card in enumerate(st.session_state.memory_cards):
        col_idx = i % 4
        with cols[col_idx]:
            if st.session_state.revealed[i]:
                st.button(card, key=f"card_{i}", disabled=True, use_container_width=True)
            else:
                if st.button("❓", key=f"card_{i}", use_container_width=True):
                    if st.session_state.first_pick is None:
                        st.session_state.first_pick = i
                        st.session_state.revealed[i] = True
                    else:
                        st.session_state.revealed[i] = True
                        if st.session_state.memory_cards[i] == st.session_state.memory_cards[st.session_state.first_pick]:
                            st.session_state.matches += 1
                            st.session_state.total_points += 10
                            if st.session_state.matches == 8:
                                st.balloons()
                                st.success("🎉 You won! +50 points!")
                                st.session_state.total_points += 50
                        else:
                            time.sleep(0.5)
                            st.session_state.revealed[i] = False
                            st.session_state.revealed[st.session_state.first_pick] = False
                        st.session_state.first_pick = None
                    st.rerun()
    
    if st.button("🔄 New Game"):
        for key in ['memory_cards', 'revealed', 'first_pick', 'matches']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

def show_color_therapy():
    st.subheader("🎨 Color Therapy & Breathing")
    
    st.markdown("""
    <div class="breathing-circle">
        BREATHE
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### Click colors that make you feel calm:")
    
    colors = {
        "🟢 Green - Nature & Calm": "#4ade80",
        "🔵 Blue - Peace & Serenity": "#60a5fa",
        "🟣 Purple - Relaxation": "#a78bfa",
        "🟡 Yellow - Joy & Optimism": "#fbbf24",
        "🩷 Pink - Comfort & Love": "#f9a8d4"
    }
    
    cols = st.columns(5)
    for i, (name, color) in enumerate(colors.items()):
        with cols[i]:
            if st.button(name.split(" - ")[0], key=f"color_{i}", use_container_width=True):
                st.session_state.total_points += 5
                st.success(f"✨ {name.split(' - ')[1]}! +5 points")

def show_puzzle_game():
    st.subheader("🧩 Sliding Puzzle Challenge")
    st.write("Arrange numbers 1-8 in order. Great for focus!")
    
    if 'puzzle' not in st.session_state:
        st.session_state.puzzle = list(range(1, 9)) + [0]
        random.shuffle(st.session_state.puzzle)
    
    def can_move(idx):
        zero_idx = st.session_state.puzzle.index(0)
        return (abs(idx - zero_idx) == 1 and idx // 3 == zero_idx // 3) or abs(idx - zero_idx) == 3
    
    def move(idx):
        zero_idx = st.session_state.puzzle.index(0)
        st.session_state.puzzle[idx], st.session_state.puzzle[zero_idx] = 0, st.session_state.puzzle[idx]
    
    cols = st.columns(3)
    for i in range(9):
        col_idx = i % 3
        with cols[col_idx]:
            val = st.session_state.puzzle[i]
            if val == 0:
                st.button("  ", key=f"puzzle_{i}", disabled=True, use_container_width=True)
            else:
                if st.button(str(val), key=f"puzzle_{i}", disabled=not can_move(i), use_container_width=True):
                    move(i)
                    if st.session_state.puzzle == list(range(1, 9)) + [0]:
                        st.balloons()
                        st.success("🎉 Solved! +100 points!")
                        st.session_state.total_points += 100
                    st.rerun()
    
    if st.button("🔄 New Puzzle"):
        del st.session_state.puzzle
        st.rerun()

def show_rhythm_game():
    st.subheader("🎵 Calming Music Rhythm")
    st.write("Tap to the beat of soothing music!")
    
    if st.button("🎵 Start Music Beat", use_container_width=True):
        st.session_state.total_points += 10
        st.balloons()
        st.success("Perfect rhythm! +10 points")
    
    st.markdown("""
    <div class="music-player">
    <h4 style="text-align:center;">🎶 Calming Background Music</h4>
    <p style="text-align:center;">Listen while playing other games!</p>
    </div>
    """, unsafe_allow_html=True)

def show_meditation():
    st.header("🧘 Meditation & Calm Center")
    
    st.markdown("""
    <div class="zen-quote">
    "In the midst of movement and chaos, keep stillness inside of you." - Deepak Chopra
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🧘 Guided Meditation", "😌 Breathing Timer", "🎵 Soothing Music", "📺 Video Library"])
    
    with tab1:
        show_guided_meditation()
    
    with tab2:
        show_breathing_timer()
    
    with tab3:
        show_music_library()
    
    with tab4:
        show_video_library()

def show_guided_meditation():
    st.subheader("🧘 Guided Meditation Sessions")
    
    meditations = [
        ("🌅 Morning Calm (10 min)", "https://youtu.be/inpok4MKVLM", "Start your day peacefully"),
        ("🌙 Evening Relaxation (15 min)", "https://youtu.be/ZToicYcHIOU", "Wind down before sleep"),
        ("😌 Stress Relief (5 min)", "https://youtu.be/SEfs5TJZ6Nk", "Quick anxiety relief"),
        ("💪 Confidence Boost (10 min)", "https://youtu.be/86m4RC_ADEY", "Build self-esteem"),
        ("🧠 Mindfulness Practice (20 min)", "https://youtu.be/O-6f5wQXSu8", "Deep mindfulness")
    ]
    
    for title, link, desc in meditations:
        st.markdown(f"""
        <div class="meditation-card">
        <h4>{title}</h4>
        <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"[🎧 Start Meditation Session]({link})")
        with col2:
            if st.button("✅ Done", key=title):
                st.session_state.meditation_time += 10
                st.session_state.total_points += 20
                st.success("+20 points!")

def show_breathing_timer():
    st.subheader("😌 Guided Breathing Exercise")
    
    st.markdown("""
    <div class="info-box">
    <h4>🫁 Box Breathing Technique</h4>
    <p>Used by Navy SEALs for stress relief!</p>
    <ol style="font-size:1.1rem;">
        <li>Breathe IN for 4 seconds</li>
        <li>HOLD for 4 seconds</li>
        <li>Breathe OUT for 4 seconds</li>
        <li>HOLD for 4 seconds</li>
        <li>Repeat 4 times</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
    
    duration = st.selectbox("Choose Duration:", ["1 minute", "3 minutes", "5 minutes", "10 minutes"])
    
    if st.button("🎯 START BREATHING EXERCISE", use_container_width=True):
        with st.spinner("Get ready..."):
            time.sleep(2)
        
        st.markdown('<div class="breathing-circle">BREATHE IN</div>', unsafe_allow_html=True)
        time.sleep(2)
        st.markdown('<div class="breathing-circle">HOLD</div>', unsafe_allow_html=True)
        time.sleep(2)
        st.markdown('<div class="breathing-circle">BREATHE OUT</div>', unsafe_allow_html=True)
        time.sleep(2)
        
        st.balloons()
        st.success("✅ Great job! +15 points")
        st.session_state.total_points += 15

def show_music_library():
    st.subheader("🎵 Soothing Music Library")
    
    music = [
        ("🌊 Ocean Waves (1 Hour)", "https://youtu.be/WHPEKLQID4U", "Calming ocean sounds"),
        ("🌧️ Rain Sounds (2 Hours)", "https://youtu.be/q76bMs-NwRk", "Gentle rainfall"),
        ("🎹 Piano Relaxation (1 Hour)", "https://youtu.be/lTRiuFIWV54", "Peaceful piano"),
        ("🎻 Classical Calm (2 Hours)", "https://youtu.be/jgpJVI3tDbY", "Classical music"),
        ("🌿 Nature Sounds (3 Hours)", "https://youtu.be/eKFTSSKCzWA", "Forest ambience"),
        ("🎼 Meditation Music (30 min)", "https://youtu.be/bQyNLPdbbT8", "Deep meditation")
    ]
    
    for title, link, desc in music:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
            <div class="music-player">
            <h4>{title}</h4>
            <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"[🎧 Play]({link})")

def show_video_library():
    st.subheader("📺 Relaxation Video Library")
    
    videos = [
        ("Anger Management for Diabetes", "https://youtu.be/BnVRcdTfTMM", 
         "Managing diabetes-related frustration"),
        ("Diabetes & Emotional Health", "https://youtu.be/RrLfCsI40Lc",
         "Understanding emotional impact"),
        ("Quick Stress Relief Techniques", "https://youtu.be/S8ZPQY0mGOs",
         "5-minute stress relief"),
        ("Yoga for Diabetes", "https://youtu.be/8D1_HX3gVRk",
         "Gentle yoga practice"),
        ("Mindful Eating Guide", "https://youtu.be/Rv4jNh9Q6nY",
         "Reduce food stress")
    ]
    
    for title, link, desc in videos:
        st.markdown(f"""
        <div class="meditation-card">
        <h3>{title}</h3>
        <p style="font-size:1.1rem;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"[📺 Watch Full Video]({link})")
        st.markdown("---")

def show_exercise():
    st.header("💪 Exercise Recommendations")

    st.markdown("""
    <div class="info-box">
    <h4>🎯 Personalised for your age, condition & injuries</h4>
    <p>Tell us about yourself and we'll show only safe, suitable exercises for you.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        age_group = st.selectbox("👤 Your Age Group", [
            "👧 Child (5–12 yrs)",
            "🧑 Teen (13–17 yrs)",
            "🧑‍💼 Young Adult (18–35 yrs)",
            "🧑‍🦱 Adult (36–55 yrs)",
            "🧓 Senior (56–70 yrs)",
            "👴 Elderly (70+ yrs)"
        ])
    with col2:
        fitness = st.selectbox("💪 Fitness Level", ["Beginner", "Intermediate", "Active"])

    st.markdown("#### 🩹 Do you have any injuries or conditions?")
    col3, col4, col5 = st.columns(3)
    with col3:
        knee = st.checkbox("🦵 Knee problem / fracture")
        back = st.checkbox("🔙 Back pain / spine issue")
    with col4:
        shoulder = st.checkbox("💪 Shoulder / arm injury")
        heart = st.checkbox("❤️ Heart condition")
    with col5:
        foot = st.checkbox("🦶 Foot / ankle problem")
        post_surgery = st.checkbox("🏥 Recent surgery")

    injuries = {"knee": knee, "back": back, "shoulder": shoulder,
                "heart": heart, "foot": foot, "surgery": post_surgery}
    any_injury = any(injuries.values())

    if any_injury:
        st.markdown("""
        <div class="warning-box">
        <h4>⚠️ Precautions for your condition</h4>
        <ul style="font-size:1.1rem;line-height:2.2;">
        """ + 
        ("  <li>🦵 <strong>Knee:</strong> Avoid squats, lunges, running. Use chair support for all exercises.</li>" if knee else "") +
        ("  <li>🔙 <strong>Back:</strong> No forward bending, heavy lifting. Lie-down exercises only.</li>" if back else "") +
        ("  <li>💪 <strong>Shoulder:</strong> No overhead movements. Keep arms below shoulder height.</li>" if shoulder else "") +
        ("  <li>❤️ <strong>Heart:</strong> Keep intensity LOW. Stop if chest pain or breathlessness.</li>" if heart else "") +
        ("  <li>🦶 <strong>Foot/Ankle:</strong> Seated or water exercises only. No jumping.</li>" if foot else "") +
        ("  <li>🏥 <strong>Post-surgery:</strong> Only gentle stretching. Consult doctor before any exercise.</li>" if post_surgery else "") +
        """
        </ul>
        <p><strong>Always consult your doctor before starting. Stop immediately if pain increases.</strong></p>
        </div>
        """, unsafe_allow_html=True)

    # Exercise database by age group
    exercise_db = {
        "👧 Child (5–12 yrs)": {
            "description": "Fun, playful activities to keep blood sugar balanced",
            "exercises": [
                ("🏃 Running & Playing", "20–30 min", "Moderate", "~150 cal", "Play tag, run in park — keeps glucose in check", "https://www.youtube.com/watch?v=FHmYVqLFrqE", ["foot"]),
                ("🚴 Cycling", "20 min", "Low-Mod", "~100 cal", "Great for joints, fun for kids", "https://www.youtube.com/watch?v=8koQXUmPNKQ", ["knee", "surgery"]),
                ("🤸 Jumping Jacks", "10 min", "Moderate", "~80 cal", "Full body, boosts energy", "https://www.youtube.com/watch?v=CWpmIW6l-YA", ["knee", "foot", "heart"]),
                ("🧘 Kids Yoga", "15 min", "Low", "~50 cal", "Calm, flexible, great for focus", "https://www.youtube.com/watch?v=X655B4ISakg", []),
                ("💃 Dance & Movement", "20 min", "Moderate", "~120 cal", "Fun way to burn sugar", "https://www.youtube.com/watch?v=JpQpAkuyKIk", ["foot", "heart"]),
            ]
        },
        "🧑 Teen (13–17 yrs)": {
            "description": "Build strength, manage stress & control blood sugar",
            "exercises": [
                ("🏃 Jogging", "20–30 min", "Moderate", "~250 cal", "Best for blood sugar control", "https://www.youtube.com/watch?v=kVnyY17VS9Y", ["knee", "foot", "heart"]),
                ("💪 Bodyweight Workout", "25 min", "Moderate", "~200 cal", "Push-ups, squats, planks", "https://www.youtube.com/watch?v=vc1E5CfRfos", ["knee", "shoulder", "back", "surgery"]),
                ("🏊 Swimming", "30 min", "Moderate", "~300 cal", "Easiest on joints, full body", "https://www.youtube.com/watch?v=gh5mAtmeR3w", []),
                ("🧘 Teen Yoga", "20 min", "Low", "~100 cal", "Reduces stress hormones that raise blood sugar", "https://www.youtube.com/watch?v=gZPMGTG9-to", []),
                ("🚴 Cycling", "30 min", "Moderate", "~250 cal", "Great cardio, easy on knees", "https://www.youtube.com/watch?v=8koQXUmPNKQ", ["knee", "surgery"]),
            ]
        },
        "🧑‍💼 Young Adult (18–35 yrs)": {
            "description": "Peak metabolism — build habits that last a lifetime",
            "exercises": [
                ("🏃 Running", "30 min", "High", "~350 cal", "Best blood sugar management exercise", "https://www.youtube.com/watch?v=kVnyY17VS9Y", ["knee", "foot", "heart"]),
                ("🏋️ Strength Training", "40 min", "High", "~300 cal", "Builds muscle that absorbs glucose", "https://www.youtube.com/watch?v=vc1E5CfRfos", ["knee", "shoulder", "back", "surgery"]),
                ("🧘 Vinyasa Yoga", "30 min", "Moderate", "~200 cal", "Stress + sugar control together", "https://www.youtube.com/watch?v=9kOCY0KNByw", []),
                ("🏊 Swimming", "30 min", "Moderate", "~350 cal", "Full body, joint friendly", "https://www.youtube.com/watch?v=gh5mAtmeR3w", []),
                ("🚴 HIIT Cycling", "20 min", "High", "~300 cal", "Short but very effective for insulin sensitivity", "https://www.youtube.com/watch?v=mmq5zZfmIws", ["knee", "heart", "surgery"]),
            ]
        },
        "🧑‍🦱 Adult (36–55 yrs)": {
            "description": "Consistent moderate exercise — key age for prevention",
            "exercises": [
                ("🚶 Brisk Walking", "45 min", "Moderate", "~200 cal", "Most sustainable for blood sugar", "https://www.youtube.com/watch?v=njeZ29umqVE", []),
                ("🧘 Diabetes Yoga", "30 min", "Low-Mod", "~150 cal", "Designed for diabetics", "https://www.youtube.com/watch?v=v7AYKMP6rOE", []),
                ("🏊 Swimming", "30 min", "Moderate", "~300 cal", "Protects joints, high calorie burn", "https://www.youtube.com/watch?v=gh5mAtmeR3w", []),
                ("💪 Resistance Bands", "30 min", "Moderate", "~180 cal", "Safe strength training for this age", "https://www.youtube.com/watch?v=4VuBqUOFDZM", ["surgery"]),
                ("🚴 Stationary Cycling", "30 min", "Moderate", "~250 cal", "Low impact, high benefit", "https://www.youtube.com/watch?v=mmq5zZfmIws", ["knee", "foot"]),
            ]
        },
        "🧓 Senior (56–70 yrs)": {
            "description": "Safe, joint-friendly exercises for blood sugar & balance",
            "exercises": [
                ("🚶 Easy Walking", "30 min", "Low", "~130 cal", "Best daily habit for seniors", "https://www.youtube.com/watch?v=njeZ29umqVE", []),
                ("🧘 Chair Yoga", "20 min", "Low", "~80 cal", "Seated yoga — safe for everyone", "https://www.youtube.com/watch?v=qXNXGBgaWVk", []),
                ("🏊 Water Aerobics", "30 min", "Low-Mod", "~200 cal", "Zero joint stress, great resistance", "https://www.youtube.com/watch?v=R3s7H7gupC4", []),
                ("💪 Light Stretching", "15 min", "Low", "~50 cal", "Improves circulation & flexibility", "https://www.youtube.com/watch?v=L_xrDAtykMI", []),
                ("⚖️ Balance Exercises", "15 min", "Low", "~60 cal", "Prevents falls, improves stability", "https://www.youtube.com/watch?v=RQV3M2r9fKU", ["surgery"]),
            ]
        },
        "👴 Elderly (70+ yrs)": {
            "description": "Gentle daily movement — even 10 minutes helps significantly",
            "exercises": [
                ("🪑 Seated Chair Exercises", "15 min", "Low", "~50 cal", "Safe for all conditions", "https://www.youtube.com/watch?v=qXNXGBgaWVk", []),
                ("🚶 Short Gentle Walks", "15–20 min", "Low", "~70 cal", "After meals especially helpful for sugar", "https://www.youtube.com/watch?v=njeZ29umqVE", []),
                ("🧘 Gentle Stretching", "10 min", "Low", "~30 cal", "Morning routine to start day well", "https://www.youtube.com/watch?v=L_xrDAtykMI", []),
                ("🤲 Hand & Foot Exercises", "10 min", "Low", "~20 cal", "Improves circulation in extremities", "https://www.youtube.com/watch?v=tz8sGVXhMDE", []),
                ("🌬️ Breathing Exercises", "10 min", "Low", "~15 cal", "Reduces stress, improves oxygen", "https://www.youtube.com/watch?v=tEmt1Znux58", []),
            ]
        }
    }

    group_data = exercise_db[age_group]
    st.markdown(f"""
    <div class="feature-card">
    <h3>{age_group} — {group_data['description']}</h3>
    </div>
    """, unsafe_allow_html=True)

    shown = 0
    for name, dur, intensity, cal, desc, link, blocked_for in group_data["exercises"]:
        # Check if this exercise is blocked for user's injury
        is_blocked = any(injuries.get(inj, False) for inj in blocked_for)
        if is_blocked:
            st.markdown(f"""
            <div style="background:#fff1f1;border-left:8px solid #dc2626;padding:20px 24px;
            border-radius:16px;margin:12px 0;opacity:0.7;">
            <h3 style="color:#dc2626;">🚫 {name} — Not Recommended</h3>
            <p style="color:#7f1d1d;">This exercise may aggravate your current condition. Skip this one.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            shown += 1
            intensity_color = {"Low": "#059669", "Low-Mod": "#0891b2", "Moderate": "#d97706", "High": "#dc2626"}.get(intensity, "#1a56db")
            st.markdown(f"""
            <div class="feature-card">
            <h3>{name}</h3>
            <p>⏱️ <strong>{dur}</strong> &nbsp;|&nbsp; 
               💪 <strong style="color:{intensity_color};">{intensity}</strong> &nbsp;|&nbsp; 
               🔥 <strong>{cal}</strong></p>
            <p style="color:#374151;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)
            col_a, col_b = st.columns([3,1])
            with col_a:
                st.markdown(f"[🎥 Watch Exercise Video]({link})")
            with col_b:
                if st.button(f"✅ Done!", key=f"ex_{name}"):
                    st.session_state.total_points += 25
                    st.session_state.exercise_done = True
                    st.success("🎉 +25 points!")

    if shown == 0:
        st.markdown("""
        <div class="warning-box">
        <h3>⚠️ All exercises restricted due to your conditions</h3>
        <p>Please consult your doctor for a personalised physiotherapy plan. 
        In the meantime, try the <strong>🌬️ Breathing Exercises</strong> in the Meditation section — they are always safe.</p>
        </div>
        """, unsafe_allow_html=True)

def show_data(df):
    if df is None:
        st.error("Dataset not loaded")
        return
    
    st.header("📊 Dataset Analytics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total", len(df))
    with col2:
        st.metric("Diabetes", df['Outcome'].sum())
    with col3:
        st.metric("Healthy", (df['Outcome']==0).sum())
    with col4:
        rate = (df['Outcome'].sum()/len(df))*100
        st.metric("Rate", f"{rate:.1f}%")
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    df['Outcome'].value_counts().plot(kind='pie', ax=axes[0,0], 
        labels=['No Diabetes', 'Diabetes'], autopct='%1.1f%%',
        colors=['#6bcf7f', '#ff6b6b'])
    axes[0,0].set_title('Distribution')
    
    df[df['Outcome']==0]['Age'].hist(alpha=0.7, bins=20, ax=axes[0,1], 
        label='Healthy', color='#6bcf7f')
    df[df['Outcome']==1]['Age'].hist(alpha=0.7, bins=20, ax=axes[0,1],
        label='Diabetes', color='#ff6b6b')
    axes[0,1].set_title('Age')
    axes[0,1].legend()
    
    df[df['Outcome']==0]['Glucose'].hist(alpha=0.7, bins=20, ax=axes[1,0],
        label='Healthy', color='#6bcf7f')
    df[df['Outcome']==1]['Glucose'].hist(alpha=0.7, bins=20, ax=axes[1,0],
        label='Diabetes', color='#ff6b6b')
    axes[1,0].set_title('Glucose')
    axes[1,0].legend()
    
    df[df['Outcome']==0]['BMI'].hist(alpha=0.7, bins=20, ax=axes[1,1],
        label='Healthy', color='#6bcf7f')
    df[df['Outcome']==1]['BMI'].hist(alpha=0.7, bins=20, ax=axes[1,1],
        label='Diabetes', color='#ff6b6b')
    axes[1,1].set_title('BMI')
    axes[1,1].legend()
    
    plt.tight_layout()
    st.pyplot(fig)

def show_tracker():
    st.header("🎯 Daily Health Tracker")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<p style="font-size:3rem;text-align:center;">🔥 {st.session_state.streak_days}</p>', 
                   unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;'>Day Streak</p>", unsafe_allow_html=True)
    with col2:
        st.metric("💧 Water", f"{st.session_state.water_intake}/8")
    with col3:
        st.metric("🏆 Points", st.session_state.total_points)
    
    st.markdown("---")
    
    st.subheader("💧 Water Tracker")
    st.progress(min(st.session_state.water_intake/8, 1.0))
    
    if st.button("➕ Add Glass", use_container_width=True):
        if st.session_state.water_intake < 12:
            st.session_state.water_intake += 1
            st.session_state.total_points += 1
            st.success("+1 point!")
            st.rerun()

def show_shop():
    st.header("🛍️ Wellness Shop")
    
    st.markdown("""
    <div class="feature-card">
    <h3>🚀 Coming Soon</h3>
    <ul style="font-size:1.1rem;">
        <li>📱 Food Scanner & Nutrition Tracker</li>
        <li>🥗 AI Meal Planner</li>
        <li>👥 Community & Support Groups</li>
        <li>📊 Advanced Health Analytics</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
