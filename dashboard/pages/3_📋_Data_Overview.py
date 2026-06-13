import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

st.set_page_config(page_title="Data Overview", page_icon="📋", layout="wide")

st.title("📋 Data Overview & Summary")
st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# DATASET SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("Dataset Summary")

summary_file = Path(__file__).parent.parent / "data" / "data_summary.csv"
if summary_file.exists():
    try:
        summary_df = pd.read_csv(summary_file)
        
        # Create metric cards
        col1, col2, col3, col4 = st.columns(4, gap="medium")
        
        metrics = {
            'Students': summary_df[summary_df['metric'] == 'n_students']['value'].values,
            'Interactions': summary_df[summary_df['metric'] == 'n_interactions']['value'].values,
            'Skills': summary_df[summary_df['metric'] == 'n_skills']['value'].values,
            'Avg Per Student': summary_df[summary_df['metric'] == 'avg_interactions_per_student']['value'].values,
        }
        
        with col1:
            if len(metrics['Students']) > 0:
                st.metric("👥 Students", f"{int(metrics['Students'][0])}")
        
        with col2:
            if len(metrics['Interactions']) > 0:
                st.metric("🔗 Total Interactions", f"{int(metrics['Interactions'][0]):,}")
        
        with col3:
            if len(metrics['Skills']) > 0:
                st.metric("🎯 Skills Covered", f"{int(metrics['Skills'][0])}")
        
        with col4:
            if len(metrics['Avg Per Student']) > 0:
                st.metric("📊 Avg per Student", f"{metrics['Avg Per Student'][0]:.1f}")
        
    except Exception as e:
        st.warning(f"Could not load summary data: {e}")
else:
    st.info("📊 Run the notebook to generate summary statistics")

# ─────────────────────────────────────────────────────────────────────────────
# PERFORMANCE DISTRIBUTION
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("Performance Distribution")

col1, col2 = st.columns(2, gap="large")

perf_dist = Path(__file__).parent.parent / "data" / "performance_distribution.png"
if perf_dist.exists():
    with col1:
        st.image(str(perf_dist), use_container_width=True)

with col2:
    st.markdown("""
    ### What This Shows
    
    **Correct Rate Distribution**
    - How often students answered correctly overall
    - Shows whether dataset is balanced (50/50) or skewed
    - Affects model training and evaluation
    
    **Interpretation:**
    - **Center at 50%**: Skills of moderate difficulty
    - **Right-leaning**: Easy skills (high success rate)
    - **Left-leaning**: Hard skills (low success rate)
    
    This distribution is important for understanding whether prediction 
    models need to be weighted or balanced.
    """)

# ─────────────────────────────────────────────────────────────────────────────
# INTERACTION PATTERNS
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("Interaction Patterns")

pattern_file = Path(__file__).parent.parent / "data" / "interaction_patterns.csv"
if pattern_file.exists():
    try:
        patterns_df = pd.read_csv(pattern_file)
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("### Sequence Length Statistics")
            
            # Calculate statistics
            if 'sequence_length' in patterns_df.columns:
                seq_lens = patterns_df['sequence_length']
                
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Min", int(seq_lens.min()))
                with col_b:
                    st.metric("Median", int(seq_lens.median()))
                with col_c:
                    st.metric("Max", int(seq_lens.max()))
                
                st.markdown(f"**Mean**: {seq_lens.mean():.1f} interactions per student")
        
        with col2:
            seq_length_plot = Path(__file__).parent.parent / "data" / "sequence_lengths.png"
            if seq_length_plot.exists():
                st.image(str(seq_length_plot), use_container_width=True)
                st.caption("Distribution of sequence lengths per student")
    
    except Exception as e:
        st.warning(f"Could not load interaction patterns: {e}")
else:
    st.info("📊 Run the notebook to generate interaction patterns")

# ─────────────────────────────────────────────────────────────────────────────
# SKILL DISTRIBUTION
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("Skill Coverage")

col1, col2 = st.columns(2, gap="large")

skill_dist = Path(__file__).parent.parent / "data" / "skill_distribution.png"
if skill_dist.exists():
    with col1:
        st.image(str(skill_dist), use_container_width=True)
        st.caption("Number of interactions per skill")

skill_table = Path(__file__).parent.parent / "data" / "skill_statistics.csv"
if skill_table.exists():
    try:
        skills_df = pd.read_csv(skill_table)
        with col2:
            st.markdown("### Skill Statistics")
            st.dataframe(
                skills_df.head(10),
                use_container_width=True,
                hide_index=True
            )
            st.caption(f"Showing top 10 of {len(skills_df)} skills")
    except:
        pass

# ─────────────────────────────────────────────────────────────────────────────
# DATA QUALITY NOTES
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("📝 Data Quality Notes")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    ### Strengths
    - ✅ Large sample of real student interactions
    - ✅ Multi-skill coverage with meaningful tags
    - ✅ Balanced correct/incorrect responses
    - ✅ Temporal ordering preserved for sequence analysis
    """)

with col2:
    st.markdown("""
    ### Considerations
    - ⚠️ Short sequences (median ~2 attempts per student-skill)
    - ⚠️ Affects BKT reliability for individual estimates
    - ⚠️ Some skills have sparse coverage
    - ℹ️ BKT uses population-level parameters instead
    """)

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# METHODOLOGY NOTES
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("🔬 Methodology Overview")

tab1, tab2, tab3 = st.tabs(["Data Preprocessing", "Train/Test Split", "Evaluation Metrics"])

with tab1:
    st.markdown("""
    ### Data Preprocessing Steps
    
    1. **Question Mapping**
       - Link questions to skill tags
       - Handle multiple skills per question
       - Explode into skill-level records
    
    2. **Temporal Ordering**
       - Sort interactions by timestamp
       - Assign sequence position per student
       - Preserve chronological information
    
    3. **Binary Outcomes**
       - Compare user answers to correct answers
       - Create binary (correct/incorrect) labels
       - Remove ambiguous or invalid responses
    """)

with tab2:
    st.markdown("""
    ### Train/Test Split Strategy
    
    **BKT Training**
    - All data used (population parameters)
    - No held-out test set required
    - EM algorithm fits parameters
    
    **DKT Training**
    - 70% Training set
    - 15% Validation set  
    - 15% Test set
    - Stratified by student
    """)

with tab3:
    st.markdown("""
    ### Evaluation Metrics
    
    **AUC-ROC (Area Under Curve)**
    - Threshold-independent metric
    - Measures discrimination ability
    - Range: 0.5 (random) to 1.0 (perfect)
    
    **Why AUC?**
    - Handles class imbalance well
    - Interpretable as ranking ability
    - Standard in knowledge tracing literature
    """)
