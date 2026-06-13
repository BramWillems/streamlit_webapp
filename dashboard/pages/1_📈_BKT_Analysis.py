import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="BKT Analysis", page_icon="📈", layout="wide")

st.title("📈 Bayesian Knowledge Tracing (BKT) Analysis")
st.markdown("---")

st.markdown("""
BKT models student learning at the **population level**, characterizing each skill using 
four key parameters derived through Expectation-Maximization.
""")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: SKILL PARAMETERS
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("1️⃣ Skill Parameter Estimates")

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown("""
    ### Parameters Explained
    
    **Prior P(L₀)**
    - Probability that student starts with knowledge
    - Low = skill requires learning
    
    **Learn Rate**
    - How quickly students learn from practice
    - High = fast learners
    
    **Guess**
    - Probability of correct answer without knowledge
    - Low = hard to guess
    
    **Slip**
    - Probability of error despite having knowledge
    - Low = reliable students
    """)

with col2:
    params_file = Path(__file__).parent.parent / "data" / "bkt_parameters.csv"
    if params_file.exists():
        try:
            params_df = pd.read_csv(params_file)
            st.dataframe(
                params_df,
                use_container_width=True,
                hide_index=True
            )
            
            # Download button
            csv = params_df.to_csv(index=False)
            st.download_button(
                label="📥 Download BKT Parameters",
                data=csv,
                file_name="bkt_parameters.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.warning(f"Could not load BKT parameters: {e}")
    else:
        st.info("📊 Run the notebook to generate BKT parameters data")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: SKILL DIFFICULTY & LEARNABILITY
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("2️⃣ Skill Difficulty vs. Learnability")

skill_plot = Path(__file__).parent.parent / "data" / "bkt_skill_space.png"
if skill_plot.exists():
    st.image(str(skill_plot), use_container_width=True)
    st.markdown("""
    **Interpretation:**
    - **Bottom-left**: Easy skills that students learn quickly
    - **Top-right**: Hard skills with slow learning
    - **Top-left**: Hard to learn quickly
    - **Bottom-right**: Easy but slow to master
    """)
else:
    st.info("📊 Run the notebook to generate visualizations")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: LEARNING CURVES
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("3️⃣ Learning Curves by Skill")

col1, col2 = st.columns(2, gap="large")

learning_plot = Path(__file__).parent.parent / "data" / "bkt_learning_curves.png"
if learning_plot.exists():
    with col1:
        st.image(str(learning_plot), use_container_width=True)
    
    with col2:
        st.markdown("""
        ### What Are Learning Curves?
        
        These curves show the predicted probability of correct response as 
        students gain more practice on a skill.
        
        **Steeper slopes** = faster learning  
        **Higher starting point** = more prior knowledge  
        **Asymptotic level** = final mastery
        
        Each colored line represents one skill. Skills naturally cluster into 
        learning patterns:
        - Some are learned quickly to mastery
        - Others plateau at moderate levels
        - A few remain challenging even with practice
        """)
else:
    st.info("📊 Run the notebook to generate visualizations")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: MASTERY RATES
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("4️⃣ Skill Mastery Status")

mastery_plot = Path(__file__).parent.parent / "data" / "bkt_mastery.png"
mastery_data = Path(__file__).parent.parent / "data" / "bkt_mastery_data.csv"

col1, col2 = st.columns(2, gap="large")

with col1:
    if mastery_plot.exists():
        st.image(str(mastery_plot), use_container_width=True)

with col2:
    if mastery_data.exists():
        try:
            mastery_df = pd.read_csv(mastery_data)
            
            # Statistics
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                mastered = (mastery_df['mastery_rate'] >= 0.5).sum()
                st.metric("Skills Mastered", f"{mastered} / {len(mastery_df)}")
            
            with col_b:
                avg_mastery = mastery_df['mastery_rate'].mean()
                st.metric("Avg Mastery Rate", f"{avg_mastery:.1%}")
            
            with col_c:
                developing = (mastery_df['mastery_rate'] < 0.5).sum()
                st.metric("Skills Developing", f"{developing} / {len(mastery_df)}")
            
            # Show table
            st.markdown("### Mastery Details")
            st.dataframe(
                mastery_df.sort_values('mastery_rate', ascending=False),
                use_container_width=True,
                hide_index=True
            )
        except Exception as e:
            st.warning(f"Could not load mastery data: {e}")
    else:
        st.info("📊 Run the notebook to generate mastery data")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5: KEY INSIGHTS
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("💡 Key Insights from BKT")

insight1, insight2, insight3 = st.columns(3, gap="medium")

with insight1:
    st.markdown("""
    ### Learning Patterns
    
    Different skills have different learning profiles. Some skills are 
    prerequisites for others, forming a learning progression.
    """)

with insight2:
    st.markdown("""
    ### Individual Differences
    
    Even though BKT is population-level, the parameters reveal where 
    students tend to struggle most.
    """)

with insight3:
    st.markdown("""
    ### Intervention Targets
    
    Skills with low mastery and high difficulty are good candidates 
    for targeted intervention and support.
    """)
