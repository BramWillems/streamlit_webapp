import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Knowledge Tracing Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS FOR MODERN/MINIMALIST DESIGN
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    :root {
        --primary-color: #1D9E75;
        --secondary-color: #EF9F27;
        --accent-color: #2E86AB;
        --background: #f8f9fa;
        --text-dark: #2c3e50;
        --text-light: #7f8c8d;
    }
    
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #f8f9fa;
        color: #2c3e50;
    }
    
    .stContainer {
        background-color: white;
    }
    
    h1, h2, h3 {
        color: #2c3e50;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1D9E75 0%, #158f5f 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2rem;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem;
    }
    
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HOME PAGE
# ─────────────────────────────────────────────────────────────────────────────
st.title("📊 Knowledge Tracing Analysis Dashboard")
st.markdown("---")

col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.markdown("""
    ### Welcome to Your Results Showcase
    
    This dashboard presents a comprehensive analysis of student learning patterns using two 
    complementary approaches:
    
    - **Bayesian Knowledge Tracing (BKT)** — A probabilistic model that characterizes skill 
      difficulty, learnability, and measurement noise at the population level.
    
    - **Deep Knowledge Tracing (DKT)** — A neural network model that learns individual student 
      knowledge states over time and predicts performance on future attempts.
    """)
    
    st.markdown("### Navigate Using the Menu")
    st.markdown("""
    Use the sidebar to explore:
    - 📈 **BKT Analysis** — Population-level skill characterization
    - 🧠 **DKT Analysis** — Individual learner trajectories & predictions
    - 📋 **Data Overview** — Summary statistics
    """)

with col2:
    st.markdown("""
    ### Key Statistics
    """)
    
    # Load summary stats if available
    summary_file = Path(__file__).parent / "data" / "summary_stats.csv"
    if summary_file.exists():
        try:
            stats_df = pd.read_csv(summary_file)
            for _, row in stats_df.head(3).iterrows():
                metric_name = row.get('metric', 'N/A')
                metric_value = row.get('value', 'N/A')
                st.metric(metric_name, metric_value)
        except:
            st.info("📊 Load data from notebook to see statistics")
    else:
        st.info("📊 Load data from notebook to see statistics")

st.markdown("---")

# Information cards
col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("""
    **🎯 What is BKT?**
    
    Bayesian Knowledge Tracing models the probability that a student has learned a skill 
    based on observed performance. It characterizes each skill using four parameters:
    - Prior knowledge
    - Learning rate
    - Guess probability
    - Slip probability
    """)

with col2:
    st.markdown("""
    **🧠 What is DKT?**
    
    Deep Knowledge Tracing uses a recurrent neural network to capture the temporal 
    dynamics of learning. It predicts the probability of correct response on the 
    next attempt based on the entire interaction history.
    """)

with col3:
    st.markdown("""
    **📚 Why Both?**
    
    BKT provides interpretable, skill-level insights. DKT captures complex temporal 
    patterns that traditional models miss. Together they offer a complete picture 
    of learning dynamics.
    """)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding: 1rem;">
    <small>Created as part of S3C2 student project</small>
</div>
""", unsafe_allow_html=True)
