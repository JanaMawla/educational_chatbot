import streamlit as st
import pandas as pd
import json
import os
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv

# Optional: try to import plotly for charts
try:
    import plotly.express as px
    import plotly.graph_objects as go
    CHARTS_ENABLED = True
except ImportError:
    CHARTS_ENABLED = False

load_dotenv()

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="🎓 Educational Data Chatbot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# ULTIMATE EMERALD GREEN UI DESIGN
# ==================================================
st.markdown("""
<style>
/* ============================================
   IMPORT FONTS
   ============================================ */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@600;700;800&display=swap');

/* ============================================
   EMERALD GREEN THEME - DESIGN TOKENS
   ============================================ */
:root {
    /* Burgundy/Red Palette */
    --primary-burgundy: #DC2626;
    --secondary-burgundy: #991B1B;
    --deep-burgundy: #7F1D1D;
    --light-burgundy: #FEE2E2;
    --ultra-light-burgundy: #FEF2F2;
    
    /* Neutrals */
    --white: #ffffff;
    --off-white: #fafbfc;
    --gray-50: #f9fafb;
    --gray-100: #f3f4f6;
    --gray-200: #e5e7eb;
    --gray-300: #d1d5db;
    --gray-400: #9ca3af;
    --gray-500: #6b7280;
    --gray-600: #4b5563;
    --gray-700: #374151;
    --gray-800: #1f2937;
    --gray-900: #111827;
    
    /* Semantic Colors */
    --success: #10b981;
    --warning: #f59e0b;
    --error: #ef4444;
    --info: #3b82f6;
    
    /* Burgundy Gradients */
    --gradient-primary: linear-gradient(135deg, #DC2626 0%, #991B1B 100%);
    --gradient-light: linear-gradient(135deg, #FCA5A5 0%, #F87171 100%);
    --gradient-subtle: linear-gradient(180deg, #ffffff 0%, #FEF2F2 100%);
    --gradient-glow: radial-gradient(circle at center, rgba(220, 38, 38, 0.3) 0%, transparent 70%);
    
    /* Shadows */
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    --shadow-burgundy: 0 10px 40px rgba(220, 38, 38, 0.35);
    --shadow-burgundy-lg: 0 20px 60px rgba(220, 38, 38, 0.4);
    
    /* Border Radius */
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 20px;
    --radius-2xl: 24px;
    --radius-full: 9999px;
    
    /* Spacing */
    --space-2: 0.5rem;
    --space-3: 0.75rem;
    --space-4: 1rem;
    --space-5: 1.25rem;
    --space-6: 1.5rem;
    --space-8: 2rem;
    --space-10: 2.5rem;
    --space-12: 3rem;
    
    /* Typography */
    --font-body: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    --font-heading: 'Poppins', 'Inter', sans-serif;
}

/* ============================================
   GLOBAL RESETS & BASE STYLES
   ============================================ */
* {
    font-family: var(--font-body);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

#MainMenu, footer, header {
    visibility: hidden;
    display: none;
}

.stApp {
    background: var(--off-white);
}

.block-container {
    padding: var(--space-6) var(--space-6) var(--space-12) var(--space-6) !important;
    max-width: 1400px !important;
}

/* ============================================
   HEADER SECTION - HERO
   ============================================ */
.hero-section {
    background: var(--gradient-primary);
    padding: var(--space-10) var(--space-8);
    border-radius: var(--radius-2xl);
    margin-bottom: var(--space-8);
    box-shadow: var(--shadow-burgundy);
    position: relative;
    overflow: hidden;
}

.hero-section::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
    animation: pulse 8s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1) rotate(0deg); opacity: 0.3; }
    50% { transform: scale(1.1) rotate(180deg); opacity: 0.5; }
}

.hero-content {
    position: relative;
    z-index: 1;
    text-align: center;
}

.hero-title {
    font-family: var(--font-heading);
    font-size: 3.5rem;
    font-weight: 800;
    color: var(--white);
    margin-bottom: var(--space-3);
    letter-spacing: -0.02em;
    text-shadow: 0 2px 20px rgba(0,0,0,0.2);
    line-height: 1.1;
}

.hero-subtitle {
    font-size: 1.25rem;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.95);
    margin-bottom: var(--space-4);
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    padding: var(--space-2) var(--space-5);
    border-radius: var(--radius-full);
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--white);
    border: 1px solid rgba(255, 255, 255, 0.3);
}

.hero-badge-dot {
    width: 8px;
    height: 8px;
    background: #34d399;
    border-radius: 50%;
    animation: blink 2s ease-in-out infinite;
}

@keyframes blink {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.8); }
}

/* ============================================
   STATS DASHBOARD
   ============================================ */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: var(--space-6);
    margin-bottom: var(--space-8);
}

.stat-card {
    background: var(--white);
    padding: var(--space-6);
    border-radius: var(--radius-xl);
    box-shadow: var(--shadow-md);
    border: 1px solid var(--gray-100);
    position: relative;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: default;
}

.stat-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: var(--gradient-primary);
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-6px);
    box-shadow: var(--shadow-burgundy);
    border-color: var(--primary-burgundy);
}

.stat-card:hover::before {
    transform: scaleX(1);
}

.stat-icon {
    width: 56px;
    height: 56px;
    background: var(--gradient-light);
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.75rem;
    margin-bottom: var(--space-4);
    box-shadow: 0 4px 12px rgba(220, 38, 38, 0.2);
}

.stat-value {
    font-family: var(--font-heading);
    font-size: 2.75rem;
    font-weight: 800;
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: var(--space-2);
    line-height: 1;
}

.stat-label {
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--gray-600);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ============================================
   CHAT INTERFACE - USER RIGHT, ASSISTANT LEFT
   ============================================ */
/* Make messages appear side by side properly */
.stChatMessage {
    background: transparent !important;
    border: none !important;
    padding: var(--space-4) 0 !important;
    margin-bottom: var(--space-4) !important;
    display: flex !important;
    width: 100% !important;
}

/* Assistant Messages - LEFT SIDE */
.stChatMessage[data-testid*="assistant"] {
    justify-content: flex-start !important;
}

.stChatMessage[data-testid*="assistant"] > div {
    max-width: 75% !important;
}

.stChatMessage[data-testid*="assistant"] [data-testid="stChatMessageContent"] {
    background: var(--white) !important;
    color: var(--gray-900) !important;
    padding: var(--space-5) var(--space-6) !important;
    border-radius: var(--radius-lg) var(--radius-lg) var(--radius-lg) var(--radius-sm) !important;
    box-shadow: var(--shadow-md) !important;
    border: 1px solid var(--gray-200) !important;
    animation: slideInLeft 0.3s ease-out;
}

/* User Messages - RIGHT SIDE */
.stChatMessage[data-testid*="user"] {
    justify-content: flex-end !important;
}

.stChatMessage[data-testid*="user"] > div {
    max-width: 65% !important;
}

.stChatMessage[data-testid*="user"] [data-testid="stChatMessageContent"] {
    background: var(--gradient-primary) !important;
    color: var(--white) !important;
    padding: var(--space-4) var(--space-6) !important;
    border-radius: var(--radius-lg) var(--radius-lg) var(--radius-sm) var(--radius-lg) !important;
    box-shadow: var(--shadow-md) !important;
    border: none !important;
    animation: slideInRight 0.3s ease-out;
    text-align: left !important;
}

@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-15px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes slideInRight {
    from { opacity: 0; transform: translateX(15px); }
    to { opacity: 1; transform: translateX(0); }
}

.stChatMessage h3 {
    font-family: var(--font-heading);
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--primary-burgundy);
    border-bottom: 2px solid var(--ultra-light-burgundy);
    padding-bottom: var(--space-2);
    margin-top: var(--space-4);
    margin-bottom: var(--space-3);
}

.stChatMessage p {
    line-height: 1.7;
    color: var(--gray-700);
    margin-bottom: var(--space-3);
}

.stChatMessage strong {
    color: var(--primary-burgundy);
    font-weight: 700;
}

# ==================================================
# CHAT INPUT - BIGGER & MORE PROMINENT
# ==================================================
.stChatInput {
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    background: var(--white) !important;
    padding: var(--space-6) var(--space-8) !important;
    border-top: 1px solid var(--gray-200) !important;
    z-index: 999 !important;
    box-shadow: 0 -4px 20px rgba(0,0,0,0.1) !important;
}

.stChatInput > div {
    max-width: 1200px !important;
    margin: 0 auto !important;
    position: relative !important;
    background: var(--white) !important;
    border: 3px solid transparent !important;
    border-radius: var(--radius-2xl) !important;
    padding: var(--space-3) !important;
    box-shadow: var(--shadow-xl) !important;
    background-image: var(--gradient-subtle) !important;
    transition: all 0.3s ease !important;
}

/* Animated gradient border */
.stChatInput > div::before {
    content: '';
    position: absolute;
    inset: -3px;
    border-radius: var(--radius-2xl);
    padding: 3px;
    background: var(--gradient-primary);
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    opacity: 0;
    transition: opacity 0.3s ease;
    z-index: -1;
}

.stChatInput:focus-within > div::before {
    opacity: 1;
}

.stChatInput:focus-within > div {
    box-shadow: 0 0 0 4px rgba(220, 38, 38, 0.15), var(--shadow-burgundy-lg) !important;
    transform: translateY(-3px) !important;
}

/* Glow effect on focus */
.stChatInput:focus-within > div::after {
    content: '';
    position: absolute;
    inset: -30px;
    background: var(--gradient-glow);
    border-radius: var(--radius-2xl);
    z-index: -2;
    opacity: 0.6;
}

.stChatInput textarea {
    font-size: 1.05rem !important;
    color: var(--gray-900) !important;
    min-height: 80px !important;
    max-height: 200px !important;
    padding: var(--space-5) var(--space-6) !important;
    line-height: 1.6 !important;
}

.stChatInput textarea::placeholder {
    color: var(--gray-400) !important;
    font-weight: 500 !important;
    font-size: 1rem !important;
}

/* Add bottom padding to main content so input doesn't cover messages */
.main .block-container {
    padding-bottom: 200px !important;
}

/* ============================================
   BUTTONS
   ============================================ */
.stButton button {
    width: 100% !important;
    background: var(--white) !important;
    color: var(--gray-700) !important;
    border: 2px solid var(--gray-200) !important;
    border-radius: var(--radius-md) !important;
    padding: var(--space-4) var(--space-5) !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    text-align: left !important;
    transition: all 0.2s ease !important;
    box-shadow: var(--shadow-sm) !important;
}

.stButton button:hover {
    background: var(--gradient-light) !important;
    color: var(--white) !important;
    border-color: var(--primary-burgundy) !important;
    transform: translateY(-2px) !important;
    box-shadow: var(--shadow-lg) !important;
}

/* Download button */
.stDownloadButton button {
    background: var(--gradient-primary) !important;
    color: var(--white) !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    padding: var(--space-3) var(--space-6) !important;
    font-weight: 600 !important;
    box-shadow: var(--shadow-md) !important;
    transition: all 0.2s ease !important;
}

.stDownloadButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: var(--shadow-burgundy) !important;
}

/* ============================================
   SIDEBAR
   ============================================ */
.css-1d391kg {
    background: var(--gray-50) !important;
}

[data-testid="stSidebar"] {
    background: var(--white) !important;
    border-right: 1px solid var(--gray-200) !important;
}

[data-testid="stSidebar"] h3 {
    color: var(--primary-burgundy) !important;
    font-weight: 700 !important;
}

/* ============================================
   LOADING & EMPTY STATES
   ============================================ */
.stSpinner > div {
    border-top-color: var(--primary-burgundy) !important;
}

.empty-state {
    text-align: center;
    padding: var(--space-12) var(--space-6);
}

.empty-icon {
    font-size: 4rem;
    margin-bottom: var(--space-4);
    opacity: 0.3;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

/* ============================================
   RESPONSIVE
   ============================================ */
@media (max-width: 768px) {
    .hero-title { font-size: 2.5rem; }
    .hero-subtitle { font-size: 1rem; }
    .stats-grid { grid-template-columns: 1fr; }
    .stat-value { font-size: 2rem; }
    .block-container { padding: var(--space-4) var(--space-3) !important; }
}

/* ============================================
   SCROLLBAR
   ============================================ */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: var(--gray-100); border-radius: var(--radius-full); }
::-webkit-scrollbar-thumb { background: var(--gray-300); border-radius: var(--radius-full); }
::-webkit-scrollbar-thumb:hover { background: var(--primary-burgundy); }
</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD DATA
# ==================================================
@st.cache_data
def load_data():
    df = pd.read_excel("Students_Dataset.xlsx")
    return df

try:
    df = load_data()
    total_students = df['student_id'].nunique()
    total_assessments = len(df)
    total_courses = df['course_name'].nunique()
    total_levels = df['class_level'].nunique()
except Exception as e:
    st.error(f"❌ Error loading dataset: {e}")
    st.stop()

# ==================================================
# OPENAI CLIENT
# ==================================================
try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    st.error("⚠️ OpenAI API Key not found")
    st.stop()

# ==================================================
# SESSION STATE
# ==================================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "filters" not in st.session_state:
    st.session_state.filters = {}

# ==================================================
# SIDEBAR - FILTERS
# ==================================================
with st.sidebar:
    st.markdown("### 🎛️ Data Filters")
    st.markdown("Filter the dataset before asking questions")
    
    filter_course = st.multiselect(
        "📚 Courses",
        options=df['course_name'].unique(),
        default=[]
    )
    
    filter_class = st.multiselect(
        "🎓 Class Levels",
        options=df['class_level'].unique(),
        default=[]
    )
    
    filter_gender = st.multiselect(
        "👥 Gender",
        options=df['student_gender'].unique(),
        default=[]
    )
    
    # Apply filters
    filtered_df = df.copy()
    if filter_course:
        filtered_df = filtered_df[filtered_df['course_name'].isin(filter_course)]
    if filter_class:
        filtered_df = filtered_df[filtered_df['class_level'].isin(filter_class)]
    if filter_gender:
        filtered_df = filtered_df[filtered_df['student_gender'].isin(filter_gender)]
    
    if filter_course or filter_class or filter_gender:
        st.session_state.filters = {
            'course': filter_course,
            'class': filter_class,
            'gender': filter_gender
        }
    else:
        st.session_state.filters = {}
    
    if st.button("🔄 Reset Filters", use_container_width=True):
        st.session_state.filters = {}
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 Filtered View")
    st.metric("Records", len(filtered_df))
    st.metric("Students", filtered_df['student_id'].nunique())
    st.metric("Avg Score", f"{filtered_df['assessment_score'].mean():.1f}")

# ==================================================
# SMART AI SYSTEM WITH VISUALIZATIONS
# ==================================================

def create_visualization(question, df_to_use):
    """Generate chart for ANY statistical question - ENHANCED"""
    if not CHARTS_ENABLED:
        return None
    
    try:
        q_lower = question.lower()
        
        # COMPARISON questions → Bar chart
        if any(word in q_lower for word in ['compare', 'vs', 'versus', 'between', 'difference', 'better', 'best', 'worst', 'top', 'highest', 'lowest']):
            
            # Course comparison
            if any(word in q_lower for word in ['course', 'subject', 'biology', 'computer', 'mathematics', 'science', 'chemistry', 'all']):
                data = df_to_use.groupby('course_name')['assessment_score'].mean().sort_values(ascending=False)
                fig = go.Figure(data=[
                    go.Bar(x=data.index, y=data.values, 
                           marker=dict(color=data.values, colorscale='Reds'),
                           text=[f"{v:.1f}" for v in data.values],
                           textposition='outside')
                ])
                fig.update_layout(title="📊 Course Performance", 
                                  height=400, template="plotly_white",
                                  yaxis_title="Average Score")
                return fig
            
            # Gender comparison
            elif any(word in q_lower for word in ['gender', 'male', 'female', 'boy', 'girl', 'm', 'f']):
                data = df_to_use.groupby('student_gender')['assessment_score'].mean()
                fig = go.Figure(data=[
                    go.Bar(x=['Male' if x=='M' else 'Female' for x in data.index], 
                           y=data.values,
                           marker=dict(color=['#DC2626', '#991B1B']),
                           text=[f"{v:.1f}" for v in data.values],
                           textposition='outside')
                ])
                fig.update_layout(title="👥 Gender Performance",
                                  height=400, template="plotly_white",
                                  yaxis_title="Average Score")
                return fig
            
            # Class level comparison
            elif any(word in q_lower for word in ['class', 'level', 'c1', 'c2', 'c3', 'c4', 'c5']):
                data = df_to_use.groupby('class_level')['assessment_score'].mean().sort_values(ascending=False)
                fig = go.Figure(data=[
                    go.Bar(x=data.index, y=data.values,
                           marker=dict(color=data.values, colorscale='Reds'),
                           text=[f"{v:.1f}" for v in data.values],
                           textposition='outside')
                ])
                fig.update_layout(title="🎓 Class Performance",
                                  height=400, template="plotly_white",
                                  yaxis_title="Average Score")
                return fig
        
        # DISTRIBUTION questions → Pie chart
        if any(word in q_lower for word in ['distribution', 'breakdown', 'percentage', 'how many', 'split', 'divide']):
            if 'gender' in q_lower:
                data = df_to_use['student_gender'].value_counts()
                fig = go.Figure(data=[go.Pie(
                    labels=['Male' if x=='M' else 'Female' for x in data.index],
                    values=data.values,
                    hole=0.4,
                    marker=dict(colors=['#DC2626', '#991B1B'])
                )])
                fig.update_layout(title="👥 Gender Distribution", height=400)
                return fig
            
            elif 'course' in q_lower:
                data = df_to_use['course_name'].value_counts()
                fig = go.Figure(data=[go.Pie(
                    labels=data.index,
                    values=data.values,
                    hole=0.4,
                    marker=dict(colors=px.colors.sequential.Reds)
                )])
                fig.update_layout(title="📚 Course Distribution", height=400)
                return fig
            
            elif 'class' in q_lower or 'level' in q_lower:
                data = df_to_use['class_level'].value_counts()
                fig = go.Figure(data=[go.Pie(
                    labels=data.index,
                    values=data.values,
                    hole=0.4,
                    marker=dict(colors=px.colors.sequential.Reds)
                )])
                fig.update_layout(title="🎓 Class Distribution", height=400)
                return fig
        
        # CORRELATION questions → Scatter plot
        if any(word in q_lower for word in ['correlation', 'relationship', 'affect', 'impact', 'influence', 'relate', 'connection', 'correlate']):
            if 'attendance' in q_lower:
                fig = px.scatter(df_to_use, x='attendance_rate', y='assessment_score',
                                trendline="ols", color_discrete_sequence=['#DC2626'],
                                title="📈 Attendance vs Performance")
                fig.update_layout(height=400, template="plotly_white")
                return fig
            
            elif any(word in q_lower for word in ['hand', 'participation', 'raise']):
                fig = px.scatter(df_to_use, x='raised_hand_count', y='assessment_score',
                                trendline="ols", color_discrete_sequence=['#991B1B'],
                                title="✋ Participation vs Performance")
                fig.update_layout(height=400, template="plotly_white")
                return fig
            
            elif 'moodle' in q_lower:
                fig = px.scatter(df_to_use, x='moodle_views', y='assessment_score',
                                trendline="ols", color_discrete_sequence=['#DC2626'],
                                title="👀 Moodle Usage vs Performance")
                fig.update_layout(height=400, template="plotly_white")
                return fig
        
        # AVERAGE questions → Show bar chart by default
        if 'average' in q_lower or 'mean' in q_lower:
            data = df_to_use.groupby('course_name')['assessment_score'].mean().sort_values(ascending=False)
            fig = go.Figure(data=[
                go.Bar(x=data.index, y=data.values,
                       marker=dict(color=data.values, colorscale='Reds'),
                       text=[f"{v:.1f}" for v in data.values],
                       textposition='outside')
            ])
            fig.update_layout(title="📊 Average Scores",
                              height=400, template="plotly_white",
                              yaxis_title="Average Score")
            return fig
    
    except Exception as e:
        return None
    
    return None

def smart_answer(question, df_to_use):
    """ChatGPT-style responses - conversational, structured, insightful"""
    
    q_lower = question.lower()
    
    # Determine if this is a "big" question needing detailed response
    is_big_question = any(word in q_lower for word in [
        'everything', 'all', 'overview', 'summary', 'interesting', 
        'insights', 'tell me about', 'what should', 'recommendations'
    ])
    
    # Build context with relevant stats
    context = f"""USER QUESTION: "{question}"

DATASET: {len(df_to_use):,} assessments, {df_to_use['student_id'].nunique()} students
Courses: {', '.join(df_to_use['course_name'].unique())}
Overall Average: {df_to_use['assessment_score'].mean():.1f}/100
"""

    # Add relevant stats
    if any(word in q_lower for word in ['course', 'biology', 'computer', 'math', 'science', 'chemistry']):
        course_data = df_to_use.groupby('course_name')['assessment_score'].mean().sort_values(ascending=False)
        context += f"\nCOURSE SCORES:\n{course_data.to_string()}\n"
    
    if any(word in q_lower for word in ['gender', 'male', 'female']):
        gender_data = df_to_use.groupby('student_gender')['assessment_score'].mean()
        context += f"\nGENDER SCORES: M={gender_data.get('M', 0):.1f}, F={gender_data.get('F', 0):.1f}\n"
    
    if any(word in q_lower for word in ['class', 'level']):
        class_data = df_to_use.groupby('class_level')['assessment_score'].mean().sort_values(ascending=False)
        context += f"\nCLASS SCORES:\n{class_data.to_string()}\n"
    
    if is_big_question:
        # Add engagement stats for overview questions
        context += f"""
ENGAGEMENT STATS:
- Avg Attendance: {df_to_use['attendance_rate'].mean():.1f}%
- Avg Hand Raises: {df_to_use['raised_hand_count'].mean():.1f}
- Avg Moodle Views: {df_to_use['moodle_views'].mean():.1f}
- Avg Downloads: {df_to_use['resources_downloads'].mean():.1f}

CORRELATIONS WITH SCORES:
- Attendance: {df_to_use['attendance_rate'].corr(df_to_use['assessment_score']):.3f}
- Hand Raises: {df_to_use['raised_hand_count'].corr(df_to_use['assessment_score']):.3f}
- Moodle Views: {df_to_use['moodle_views'].corr(df_to_use['assessment_score']):.3f}
"""

    # Different prompts for big vs small questions
    if is_big_question:
        prompt = f"""{context}

This is a BIG question - provide a DETAILED, INSIGHTFUL response like ChatGPT would.

STYLE:
- Start with ### and emoji
- Use **bold** for emphasis
- Break into SHORT sections with subheadings
- Use bullet points for lists
- 2-3 sentences per paragraph MAX
- Focus on INSIGHTS, not just numbers
- Be conversational and engaging

STRUCTURE:
### [Title]

Brief intro (1-2 sentences)

**Section 1:**
- Point with data
- Point with data

**Section 2:**
- Insight
- Insight

Final takeaway or recommendation.

NOW ANSWER: "{question}"
"""
    else:
        prompt = f"""{context}

This is a SIMPLE question - provide a SHORT, DIRECT response like ChatGPT would.

STYLE:
- Start with ### and emoji
- 2-4 sentences total
- Use **bold** for key numbers
- Conversational tone
- Answer the EXACT question

EXAMPLE:

Q: "Compare Biology vs Computer"
A: ### 📊 Biology vs Computer

Computer students score **70.3** on average, while Biology students score **70.0**. Computer edges ahead by just 0.3 points - they're basically tied! Both perform right around the overall average.

NOW ANSWER: "{question}"
"""

    try:
        start_time = datetime.now()
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.15,
            max_tokens=400 if is_big_question else 200
        )
        
        elapsed = (datetime.now() - start_time).total_seconds()
        answer = response.choices[0].message.content.strip()
        
        # Generate visualization
        chart = create_visualization(question, df_to_use)
        
        return answer, chart, elapsed
    
    except Exception as e:
        return f"❌ Error: {str(e)}", None, 0

# ==================================================
# HEADER
# ==================================================
st.markdown("""
<div class="hero-section">
    <div class="hero-content">
        <div class="hero-title">🎓 Educational Data Chatbot</div>
        <div class="hero-subtitle">Advanced Educational Data Intelligence Platform</div>
        <div class="hero-badge">
            <div class="hero-badge-dot"></div>
            Powered by GPT-4o-mini · Real-time Analysis · Smart Insights
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================================================
# STATS DASHBOARD - UPDATED
# ==================================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-value">{total_levels}</div>
        <div class="stat-label">Class Levels</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-value">{total_students}</div>
        <div class="stat-label">Students</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon">📚</div>
        <div class="stat-value">{total_courses}</div>
        <div class="stat-label">Courses</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon">📝</div>
        <div class="stat-value">{total_assessments:,}</div>
        <div class="stat-label">Assessments</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================================================
# EXAMPLE QUESTIONS - FIXED
# ==================================================
if not st.session_state.messages:
    st.markdown("### 💡 Quick Start: Ask Me Anything!")
    
    col1, col2 = st.columns(2)
    
    examples = [
        "📊 Compare all courses performance",
        "👥 Show me gender performance breakdown",
        "📈 What correlates with high scores?",
        "🎯 Which class performs best?",
        "🔍 How many students score above 80?",
        "💡 Tell me something interesting about the data",
        "⭐ Which course has the best students?",
        "📉 Are there any concerning trends?"
    ]
    
    for i, example in enumerate(examples):
        col = col1 if i % 2 == 0 else col2
        with col:
            if st.button(example, key=f"ex_{i}"):
                # Add user message
                st.session_state.messages.append({"role": "user", "content": example})
                
                # Get AI response immediately
                with st.spinner("✨ Thinking..."):
                    answer, chart, elapsed = smart_answer(example, filtered_df if st.session_state.filters else df)
                
                # Add assistant message
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "chart": chart,
                    "time": elapsed
                })
                st.rerun()

# ==================================================
# DISPLAY CHAT
# ==================================================
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])
        
        # Show chart if exists with unique key
        if msg["role"] == "assistant" and "chart" in msg and msg["chart"]:
            st.plotly_chart(msg["chart"], use_container_width=True, key=f"chart_{i}")
        
        # Show response time
        if msg["role"] == "assistant" and "time" in msg:
            st.caption(f"⚡ Answered in {msg['time']:.2f}s")

# ==================================================
# CHAT INPUT
# ==================================================
if prompt := st.chat_input("💭 Ask me anything about the student data... I can answer ANY question!"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    # Get AI response with professional loading
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("✨ Thinking..."):
            answer, chart, elapsed = smart_answer(prompt, filtered_df if st.session_state.filters else df)
        
        st.markdown(answer)
        
        # Show chart with unique key
        if chart:
            chart_key = f"chart_{len(st.session_state.messages)}"
            st.plotly_chart(chart, use_container_width=True, key=chart_key)
        
        st.caption(f"⚡ Answered in {elapsed:.2f}s")
    
    # Add to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "chart": chart,
        "time": elapsed
    })

# ==================================================
# DOWNLOAD
# ==================================================
if st.session_state.messages:
    st.markdown("<br><br>", unsafe_allow_html=True)
    chat_text = "\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
    st.download_button(
        "📥 Download Full Chat History",
        chat_text,
        f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )