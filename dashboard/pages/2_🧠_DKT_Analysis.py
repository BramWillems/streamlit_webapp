import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import torch
from pathlib import Path

st.set_page_config(page_title="DKT Analysis", page_icon="🧠", layout="wide")

st.title("🧠 Deep Knowledge Tracing (DKT) Analysis")
st.markdown("---")

st.markdown("""
DKT uses a recurrent neural network to model individual student knowledge states 
over time and predict performance on future attempts.
""")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: MODEL PERFORMANCE
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("1️⃣ Model Training & Performance")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    ### Model Architecture
    
    **Input Layer**
    - Student skill interactions
    - Correctness of previous responses
    
    **Hidden Layer**
    - LSTM (Long Short-Term Memory)
    - Captures temporal dependencies
    
    **Output Layer**
    - Predicted P(correct) for all skills
    - Updated based on entire history
    """)

with col2:
    # Load performance metrics
    perf_file = Path(__file__).parent.parent / "data" / "dkt_performance.csv"
    if perf_file.exists():
        try:
            perf_df = pd.read_csv(perf_file)
            
            col_a, col_b = st.columns(2)
            with col_a:
                if 'train_auc' in perf_df.columns:
                    train_auc = perf_df['train_auc'].iloc[-1]
                    st.metric("Train AUC", f"{train_auc:.4f}")
            
            with col_b:
                if 'val_auc' in perf_df.columns:
                    val_auc = perf_df['val_auc'].iloc[-1]
                    st.metric("Validation AUC", f"{val_auc:.4f}")
            
            # Download button
            csv = perf_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Performance Data",
                data=csv,
                file_name="dkt_performance.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.warning(f"Could not load performance data: {e}")
    else:
        st.info("📊 Run the notebook to generate performance metrics")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: TRAINING CURVES
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("2️⃣ Training Progress")

train_plot = Path(__file__).parent.parent / "data" / "dkt_training_curves.png"
if train_plot.exists():
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.image(str(train_plot), use_container_width=True)
    
    with col2:
        st.markdown("""
        ### Interpreting the Curves
        
        **Left Plot: Training Loss**
        - Should decrease over epochs
        - Indicates model is learning patterns
        
        **Right Plot: Validation AUC**
        - Higher is better (max = 1.0)
        - Measures prediction accuracy
        - Should increase with training
        
        **Good Training Signs:**
        - Smooth decreasing trends
        - Convergence to stable values
        - No overfitting (val diverging from train)
        """)
else:
    st.info("📊 Run the notebook to generate training plots")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: INDIVIDUAL LEARNER ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("3️⃣ Individual Learner Predictions")

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown("""
    ### How DKT Makes Predictions
    
    1. **Read History**
       - All past skill attempts
       - Whether each was correct
    
    2. **Update State**
       - LSTM processes sequence
       - Forms knowledge representation
    
    3. **Predict Next**
       - Outputs P(correct) per skill
       - For the student's next attempt
    """)

with col2:
    learner_file = Path(__file__).parent.parent / "data" / "sample_learner_profile.csv"
    if learner_file.exists():
        try:
            learner_df = pd.read_csv(learner_file)
            st.markdown("### Sample Learner Data")
            st.dataframe(
                learner_df.head(15),
                use_container_width=True,
                hide_index=True
            )
            st.caption(f"Showing first 15 of {len(learner_df)} interactions")
        except Exception as e:
            st.warning(f"Could not load learner data: {e}")
    else:
        st.info("📊 Run the notebook to generate sample learner profiles")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: KNOWLEDGE STATE VISUALIZATION
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("4️⃣ Knowledge State Evolution")

col1, col2 = st.columns(2, gap="large")

with col1:
    pred_skills_plot = Path(__file__).parent.parent / "data" / "dkt_predicted_skills.png"
    if pred_skills_plot.exists():
        st.image(str(pred_skills_plot), use_container_width=True)
        st.caption("Predicted probabilities for next attempt across all skills")

with col2:
    knowledge_plot = Path(__file__).parent.parent / "data" / "dkt_knowledge_trajectory.png"
    if knowledge_plot.exists():
        st.image(str(knowledge_plot), use_container_width=True)
        st.caption("How knowledge estimate for one skill evolves over time")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5: MODEL INSIGHTS
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("💡 Key Insights from DKT")

insight1, insight2, insight3 = st.columns(3, gap="medium")

with insight1:
    st.markdown("""
    ### Adaptive Modeling
    
    DKT adapts predictions as students interact more. Early predictions are 
    uncertain, but become more confident with history.
    """)

with insight2:
    st.markdown("""
    ### Temporal Patterns
    
    The LSTM captures temporal dependencies that traditional models miss, such as 
    how struggling early affects later performance.
    """)

with insight3:
    st.markdown("""
    ### Personalization
    
    Each student gets unique predictions based entirely on their interaction 
    history—true personalized learning.
    """)

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6: COMPARISON WITH ACTUAL
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("5️⃣ Prediction Accuracy")

accuracy_file = Path(__file__).parent.parent / "data" / "dkt_accuracy_summary.csv"
if accuracy_file.exists():
    try:
        accuracy_df = pd.read_csv(accuracy_file)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            test_auc = accuracy_df[accuracy_df['metric'] == 'test_auc']['value'].values
            if len(test_auc) > 0:
                st.metric("Test Set AUC", f"{test_auc[0]:.4f}")
        
        with col2:
            correct_preds = accuracy_df[accuracy_df['metric'] == 'correct_predictions'].values
            if len(correct_preds) > 0:
                st.metric("Correct Predictions", f"{correct_preds[0][1]:.1%}")
        
        with col3:
            st.metric("Model Type", "LSTM-based RNN")
        
        st.markdown("---")
        st.markdown("""
        **What does AUC-ROC mean?**
        - Measures how well model ranks correct vs incorrect
        - 0.5 = random guessing
        - 1.0 = perfect predictions
        - 0.75+ = good discrimination
        """)
    except Exception as e:
        st.warning(f"Could not load accuracy data: {e}")
else:
    st.info("📊 Run the notebook to generate accuracy metrics")
