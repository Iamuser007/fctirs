import streamlit as st
import json
import time
from datetime import datetime, timedelta
import random

# Page config
st.set_page_config(
    page_title="FCT-IRS CBT Mock Exam",
    page_icon="📊",
    layout="wide"
)

# Enhanced CSS with animations and sleek design
st.markdown("""
<style>
    /* Base styling */
    body, .stApp, .css-18e3th9 {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        color: #000000;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Smooth animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    /* Main title styling */
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin: 2rem 0;
        background: linear-gradient(45deg, #000000, #333333, #000000);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shimmer 3s linear infinite, fadeIn 0.8s ease-out;
        letter-spacing: -1px;
    }
    
    .subtitle {
        font-size: 1.3rem;
        text-align: center;
        color: #333333;
        margin-bottom: 2rem;
        animation: fadeIn 1s ease-out 0.3s both;
        font-weight: 500;
    }
    
    /* Card styling with hover effects */
    .stats-box, .timer-box {
        padding: 1.2rem;
        border-radius: 16px;
        background: #ffffff;
        border: 2px solid #000000;
        text-align: center;
        font-size: 1.3rem;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: slideIn 0.6s ease-out;
    }
    
    .stats-box:hover, .timer-box:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border-color: #333333;
    }
    
    .timer-green {
        border-color: #10B981 !important;
        background: linear-gradient(135deg, #ffffff 0%, #F0FDF4 100%) !important;
    }
    
    .timer-yellow {
        border-color: #F59E0B !important;
        background: linear-gradient(135deg, #ffffff 0%, #FEFCE8 100%) !important;
    }
    
    .timer-red {
        border-color: #EF4444 !important;
        background: linear-gradient(135deg, #ffffff 0%, #FEF2F2 100%) !important;
    }
    
    .question-number {
        font-size: 1.1rem;
        color: #666666;
        margin-bottom: 1.5rem;
        font-weight: 600;
        animation: fadeIn 0.5s ease-out;
        letter-spacing: 0.5px;
    }
    
    .question-text {
        font-size: 1.8rem;
        font-weight: 600;
        margin: 2rem 0;
        padding: 2rem;
        background: #ffffff;
        border-left: 6px solid #000000;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        animation: fadeIn 0.6s ease-out;
        transition: all 0.3s ease;
    }
    
    .question-text:hover {
        box-shadow: 0 6px 30px rgba(0,0,0,0.12);
        transform: translateX(5px);
    }
    
    /* Button styling with advanced animations */
    .stButton>button {
        background: linear-gradient(135deg, #ffffff 0%, #f5f5f5 100%);
        color: #000000;
        border: 2px solid #000000;
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button:before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    .stButton>button:hover:before {
        left: 100%;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #000000 0%, #333333 100%);
        color: #ffffff;
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }
    
    .stButton>button:active {
        transform: translateY(-1px) scale(0.98);
    }
    
    /* Primary button special styling */
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
        color: #ffffff;
        border: 2px solid #000000;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        animation: pulse 2s infinite;
    }
    
    .stButton>button[kind="primary"]:hover {
        background: linear-gradient(135deg, #333333 0%, #4d4d4d 100%);
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
        animation: none;
    }
    
    /* Input styling */
    .stTextInput>div>input {
        color: #000000;
        background: #ffffff;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 0.8rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>input:focus {
        border-color: #000000;
        box-shadow: 0 0 0 3px rgba(0,0,0,0.1);
    }
    
    /* Simple metric styling - FIXED: Ensure black text with navy blue background */
    .stMetric {
        background: linear-gradient(135deg, #001f3f 0%, #003366 100%) !important;
        color: #ffffff !important;
        border: 2px solid #001f3f !important;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        animation: fadeIn 0.8s ease-out;
        transition: all 0.3s ease;
    }

    .stMetric > div {
        color: #ffffff !important;
    }

    .stMetric > div[data-testid="stMetricLabel"] {
        color: #ffffff !important;
        font-weight: 600;
        font-size: 1rem;
    }

    .stMetric > div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 800;
        font-size: 2.2rem;
    }

    .stMetric > div[data-testid="stMetricDelta"] {
        color: #ffffff !important;
    }

    .stMetric:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 6px 25px rgba(0,0,0,0.3);
        border-color: #00264d !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: #ffffff;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: #f8f9fa;
        border-color: #000000;
        transform: translateX(5px);
    }
    
    /* Success/Error boxes */
    .stSuccess, .stError {
        border-radius: 12px;
        border-width: 2px;
        animation: slideIn 0.6s ease-out;
        font-weight: 500;
    }
    
    /* Navigation section */
    .nav-section {
        background: #ffffff;
        padding: 2rem;
        border-radius: 16px;
        border: 2px solid #e0e0e0;
        margin: 2rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        animation: fadeIn 0.8s ease-out;
    }
    
    /* History info styling */
    .history-info {
        text-align: center;
        font-size: 1.2rem;
        color: #333333;
        margin: 1rem 0;
        font-weight: 600;
    }
    
    /* Divider animation */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #000000, transparent);
        margin: 2rem 0;
        animation: fadeIn 0.8s ease-out;
    }
    
    /* Loading animation */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Instruction box */
    .instruction-box {
        background: #ffffff;
        border: 2px solid #000000;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 6px 25px rgba(0,0,0,0.12);
        animation: fadeIn 1s ease-out;
    }
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* Container animations */
    .element-container {
        animation: fadeIn 0.5s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state with local storage persistence
def initialize_session_state():
    if 'exam_started' not in st.session_state:
        st.session_state.exam_started = False
    if 'all_questions' not in st.session_state:
        st.session_state.all_questions = []
    if 'current_exam_questions' not in st.session_state:
        st.session_state.current_exam_questions = []
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'exam_duration' not in st.session_state:
        st.session_state.exam_duration = 1800  # 30 minutes
    if 'exam_submitted' not in st.session_state:
        st.session_state.exam_submitted = False
    
    # Load exam history from session state (persists during session)
    if 'exam_history' not in st.session_state:
        st.session_state.exam_history = []
    
    # Track previously seen questions to avoid repetition
    if 'used_question_ids' not in st.session_state:
        st.session_state.used_question_ids = set()

# Load all questions
def load_all_questions():
    try:
        with open('questions.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("❌ questions.json file not found! Please ensure it's in the same directory as main.py")
        return []
    except json.JSONDecodeError:
        st.error("❌ Error parsing questions.json. Please check the file format.")
        return []

# Get random 30 questions that haven't been used recently
def get_random_questions(all_questions, count=30):
    if len(all_questions) <= count:
        return all_questions.copy()
    
    # Filter out recently used questions
    available_questions = [q for q in all_questions if q['id'] not in st.session_state.used_question_ids]
    
    # If not enough unique questions, use all questions
    if len(available_questions) < count:
        available_questions = all_questions.copy()
        st.session_state.used_question_ids.clear()  # Reset tracking if we've used most questions
    
    selected_questions = random.sample(available_questions, count)
    
    # Track used questions
    for question in selected_questions:
        st.session_state.used_question_ids.add(question['id'])
    
    return selected_questions

# Calculate remaining time
def get_remaining_time():
    if st.session_state.start_time is None:
        return st.session_state.exam_duration
    elapsed = (datetime.now() - st.session_state.start_time).total_seconds()
    remaining = max(0, st.session_state.exam_duration - elapsed)
    return int(remaining)

# Format time
def format_time(seconds):
    mins, secs = divmod(int(seconds), 60)
    hours, mins = divmod(mins, 60)
    if hours > 0:
        return f"{hours:02d}:{mins:02d}:{secs:02d}"
    return f"{mins:02d}:{secs:02d}"

# Get timer color class based on remaining time
def get_timer_color_class(remaining_time):
    if remaining_time > 900:  # More than 15 minutes
        return "timer-green"
    elif remaining_time > 300:  # Between 5-15 minutes
        return "timer-yellow"
    else:  # Less than 5 minutes
        return "timer-red"

# Save exam result to history
def save_exam_result(score, total, percentage):
    result = {
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'score': score,
        'total': total,
        'percentage': percentage
    }
    st.session_state.exam_history.append(result)

# Reset history
def reset_history():
    st.session_state.exam_history = []
    st.session_state.used_question_ids = set()

# Initialize session state
initialize_session_state()

# Start screen
if not st.session_state.exam_started:
    st.markdown('<div class="main-title">📊 FCT-IRS CBT Examination</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Federal Capital Territory Internal Revenue Service</div>', unsafe_allow_html=True)
    
    # Show exam history summary if exists
    if st.session_state.exam_history:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f'<div class="history-info">📈 Exam Attempts: {len(st.session_state.exam_history)}</div>', unsafe_allow_html=True)
        with col2:
            if st.button("🗑️ Reset History", use_container_width=True):
                reset_history()
                st.rerun()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="instruction-box">', unsafe_allow_html=True)
        st.markdown("### 📋 Examination Guidelines")
        st.markdown("""
        ⏱️ **Duration:** 30 minutes  
        📝 **Total Questions:** 30 questions (randomly selected)  
        🧭 **Navigation:** Move between questions freely  
        📤 **Submission:** Auto-submit when time expires or manual submit  
        📊 **Scoring:** View results immediately after submission  
        
        💡 **Important Information:** 
        - Each exam attempt features different 30 questions
        - Do not refresh the page during examination
        - Answers are saved automatically
        - Timer starts immediately upon commencement
        - Progress is saved locally during the session
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🚀 COMMENCE EXAMINATION", key="start", use_container_width=True, type="primary"):
            all_questions = load_all_questions()
            if all_questions:
                st.session_state.all_questions = all_questions
                st.session_state.current_exam_questions = get_random_questions(all_questions, 30)
                st.session_state.exam_started = True
                st.session_state.start_time = datetime.now()
                st.session_state.answers = {}
                st.session_state.current_question = 0
                st.rerun()

# Exam screen
elif st.session_state.exam_started and not st.session_state.exam_submitted:
    # Check if time expired
    remaining_time = get_remaining_time()
    if remaining_time <= 0:
        correct_answers = 0
        total_questions = len(st.session_state.current_exam_questions)
        for question in st.session_state.current_exam_questions:
            user_answer = st.session_state.answers.get(question['id'])
            if user_answer == question['correctAnswer']:
                correct_answers += 1
        score_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        save_exam_result(correct_answers, total_questions, score_percentage)
        st.session_state.exam_submitted = True
        st.rerun()
    
    # Header with timer and stats
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown('<div class="main-title">FCT-IRS CBT Examination</div>', unsafe_allow_html=True)
    
    with col2:
        answered = len(st.session_state.answers)
        total = len(st.session_state.current_exam_questions)
        st.markdown(f'<div class="stats-box">📊 Progress: {answered}/{total}</div>', unsafe_allow_html=True)
    
    with col3:
        timer_class = get_timer_color_class(remaining_time)
        timer_emoji = "🟢" if remaining_time > 900 else "🟡" if remaining_time > 300 else "🔴"
        st.markdown(f'<div class="timer-box {timer_class}">{timer_emoji} {format_time(remaining_time)}</div>', unsafe_allow_html=True)
    
    # Main content
    if st.session_state.current_exam_questions:
        question = st.session_state.current_exam_questions[st.session_state.current_question]
        
        # Question number
        st.markdown(f'<div class="question-number">📄 Question {st.session_state.current_question + 1} of {len(st.session_state.current_exam_questions)}</div>', unsafe_allow_html=True)
        
        # Question text
        st.markdown(f'<div class="question-text">{question["question"]}</div>', unsafe_allow_html=True)
        
        # Options
        current_answer = st.session_state.answers.get(question['id'])
        st.markdown("#### 🖊️ Select your answer:")
        st.markdown("")
        
        cols = st.columns(len(question['options']))
        for i, option in enumerate(question['options']):
            option_letter = option.split('.')[0].strip()
            option_text = option.split('.', 1)[1].strip() if '.' in option else option
            is_selected = current_answer == option_letter
            button_label = f"{option_letter}. {option_text}"
            
            button_type = "primary" if is_selected else "secondary"
            
            with cols[i]:
                if st.button(button_label, key=f"{question['id']}_{option_letter}", use_container_width=True, type=button_type):
                    st.session_state.answers[question['id']] = option_letter
                    st.rerun()
        
        # Navigation section
        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown("### 🧭 Question Navigator")
        st.markdown("")
        
        # Question navigation grid
        nav_cols = st.columns(10)
        for idx in range(len(st.session_state.current_exam_questions)):
            with nav_cols[idx % 10]:
                is_current = idx == st.session_state.current_question
                is_answered = st.session_state.current_exam_questions[idx]['id'] in st.session_state.answers
                button_type = "primary" if is_current else ("secondary" if is_answered else "secondary")
                emoji = "📍" if is_current else ("✅" if is_answered else "⚪")
                
                if st.button(f"{emoji} {idx + 1}", key=f"nav_{idx}", use_container_width=True, type=button_type):
                    st.session_state.current_question = idx
                    st.rerun()
        
        st.markdown("")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Navigation and action buttons
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        
        with col1:
            if st.session_state.current_question > 0:
                if st.button("◀️ Previous", use_container_width=True):
                    st.session_state.current_question -= 1
                    st.rerun()
        
        with col2:
            if st.session_state.current_question < len(st.session_state.current_exam_questions) - 1:
                if st.button("Next ▶️", use_container_width=True):
                    st.session_state.current_question += 1
                    st.rerun()
        
        with col3:
            if current_answer:
                if st.button("🔄 Clear", use_container_width=True):
                    if question['id'] in st.session_state.answers:
                        del st.session_state.answers[question['id']]
                    st.rerun()
        
        with col5:
            if st.button("📤 SUBMIT EXAM", type="primary", use_container_width=True):
                correct_answers = 0
                total_questions = len(st.session_state.current_exam_questions)
                for q in st.session_state.current_exam_questions:
                    user_answer = st.session_state.answers.get(q['id'])
                    if user_answer == q['correctAnswer']:
                        correct_answers += 1
                score_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
                save_exam_result(correct_answers, total_questions, score_percentage)
                st.session_state.exam_submitted = True
                st.rerun()

# Results screen
elif st.session_state.exam_submitted:
    st.markdown('<div class="main-title">📊 Examination Results</div>', unsafe_allow_html=True)
    
    # Calculate score
    correct_answers = 0
    total_questions = len(st.session_state.current_exam_questions)
    
    for question in st.session_state.current_exam_questions:
        user_answer = st.session_state.answers.get(question['id'])
        if user_answer == question['correctAnswer']:
            correct_answers += 1
    
    score_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    
    # Display score with black text (FIXED)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📋 Total Questions", total_questions)
    with col2:
        st.metric("✅ Correct Answers", correct_answers)
    with col3:
        st.metric("📈 Score", f"{score_percentage:.1f}%")
    
    # Pass/Fail status
    pass_mark = 70
    if score_percentage >= pass_mark:
        st.success(f"🎉 Congratulations! You PASSED with {score_percentage:.1f}%")
    else:
        st.error(f"📚 You scored {score_percentage:.1f}%. Pass mark is {pass_mark}%. Continue your studies.")
    
    # Detailed review
    st.markdown("### 📝 Detailed Review")
    
    for idx, question in enumerate(st.session_state.current_exam_questions):
        user_answer = st.session_state.answers.get(question['id'], 'Not answered')
        correct_answer = question['correctAnswer']
        is_correct = user_answer == correct_answer
        
        with st.expander(f"Question {idx + 1}: {'✅ Correct' if is_correct else '❌ Incorrect'}"):
            st.markdown(f"**{question['question']}**")
            st.markdown("")
            
            for option in question['options']:
                option_letter = option.split('.')[0].strip()
                if option_letter == correct_answer:
                    st.markdown(f"✅ **{option}** (Correct Answer)")
                elif option_letter == user_answer:
                    st.markdown(f"❌ **{option}** (Your Answer)")
                else:
                    st.markdown(f"⚪ {option}")
            
            st.info(f"**💡 Explanation:** {question.get('explanation', 'No explanation available')}")
    
    # Action buttons
    if st.button("🏠 Return to Dashboard", use_container_width=True, type="primary"):
        st.session_state.exam_started = False
        st.session_state.current_question = 0
        st.session_state.answers = {}
        st.session_state.start_time = None
        st.session_state.exam_submitted = False
        st.session_state.current_exam_questions = []
        st.rerun()

# Auto-refresh for timer
if st.session_state.exam_started and not st.session_state.exam_submitted:
    time.sleep(1)
    st.rerun()