import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from prediction_helper import (
    load_bkt_parameters,
    predict_bkt,
    predict_dkt_simple,
    compare_models,
    create_sample_learner_sequence
)

st.set_page_config(page_title="Student Predictions", page_icon="🔮", layout="wide")

st.title("🔮 Student Performance Predictions")
st.markdown("---")

st.markdown("""
This page uses **Bayesian Knowledge Tracing (BKT)** and **Deep Knowledge Tracing (DKT)** 
to predict a student's probability of success on their next attempt. Input a student's 
interaction history to see personalized predictions.
""")

# ─────────────────────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_resource
def load_data():
    """Load BKT parameters and available skills."""
    try:
        bkt_params = load_bkt_parameters()
        return bkt_params
    except Exception as e:
        st.error(f"Could not load BKT parameters: {e}")
        return None

bkt_params = load_data()

if bkt_params is None:
    st.stop()

skills = sorted(bkt_params.index.astype(str).tolist())
skill_labels = {s: f"Skill {s}" for s in skills}

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: INPUT METHOD SELECTION
# ─────────────────────────────────────────────────────────────────────────────

st.subheader("1️⃣ Enter Student History")

input_method = st.radio(
    "How would you like to input student data?",
    ["📝 Manual Entry", "🎲 Use Sample Data", "📋 Paste CSV"],
    horizontal=True
)

student_sequence = []

if input_method == "📝 Manual Entry":
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.markdown("### Add Attempts")
        
        selected_skill = st.selectbox(
            "Select skill",
            skills,
            format_func=lambda x: skill_labels[x]
        )
        
        attempt_result = st.radio(
            "Result:",
            ["✓ Correct", "✗ Incorrect"],
            horizontal=True
        )
        correct = 1 if attempt_result == "✓ Correct" else 0
        
        if st.button("➕ Add Attempt", use_container_width=True):
            st.session_state.sequence = st.session_state.get('sequence', [])
            st.session_state.sequence.append({
                'skill': selected_skill,
                'correct': correct
            })
            st.success(f"Added attempt: Skill {selected_skill} - {'✓ Correct' if correct else '✗ Incorrect'}")
    
    with col2:
        st.markdown("### Attempt History")
        if 'sequence' in st.session_state and st.session_state.sequence:
            history_df = pd.DataFrame(st.session_state.sequence)
            history_df['Result'] = history_df['correct'].map({1: '✓ Correct', 0: '✗ Incorrect'})
            history_df['Skill'] = history_df['skill'].apply(lambda x: skill_labels.get(x, x))
            
            st.dataframe(
                history_df[['Skill', 'Result']].reset_index(drop=True),
                use_container_width=True,
                hide_index=True
            )
            
            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state.sequence = []
                st.rerun()
            
            student_sequence = st.session_state.get('sequence', [])
        else:
            st.info("No attempts added yet. Add attempts using the controls on the left.")

elif input_method == "🎲 Use Sample Data":
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.markdown("### Sample Generation")
        n_attempts = st.slider("Number of attempts:", 2, 20, 10)
        skill_focus = st.selectbox(
            "Focus on skill:",
            skills,
            format_func=lambda x: skill_labels[x]
        )
        
        if st.button("🎲 Generate Sample", use_container_width=True):
            st.session_state.sequence = []
            for i in range(n_attempts):
                # Mix of focused skill and random skills
                if np.random.random() < 0.7:
                    s = skill_focus
                else:
                    s = np.random.choice(skills)
                
                # Improve over time
                prob_correct = 0.3 + 0.5 * (i / n_attempts)
                c = 1 if np.random.random() < prob_correct else 0
                st.session_state.sequence.append({'skill': s, 'correct': c})
    
    with col2:
        if 'sequence' in st.session_state and st.session_state.sequence:
            st.markdown("### Generated Sequence")
            history_df = pd.DataFrame(st.session_state.sequence)
            history_df['Result'] = history_df['correct'].map({1: '✓ Correct', 0: '✗ Incorrect'})
            history_df['Skill'] = history_df['skill'].apply(lambda x: skill_labels.get(x, x))
            
            st.dataframe(
                history_df[['Skill', 'Result']].reset_index(drop=True),
                use_container_width=True,
                hide_index=True
            )
            
            student_sequence = st.session_state.get('sequence', [])

elif input_method == "📋 Paste CSV":
    st.markdown("### CSV Format")
    st.code("skill,correct\n71,1\n74,0\n71,1", language="csv")
    
    csv_text = st.text_area(
        "Paste CSV data (skill, correct):",
        height=150,
        placeholder="skill,correct\n71,1\n74,0"
    )
    
    if csv_text:
        try:
            from io import StringIO
            csv_data = pd.read_csv(StringIO(csv_text))
            
            if 'skill' in csv_data.columns and 'correct' in csv_data.columns:
                student_sequence = [
                    {'skill': str(row['skill']), 'correct': int(row['correct'])}
                    for _, row in csv_data.iterrows()
                ]
                
                history_df = pd.DataFrame(student_sequence)
                history_df['Result'] = history_df['correct'].map({1: '✓ Correct', 0: '✗ Incorrect'})
                history_df['Skill'] = history_df['skill'].apply(lambda x: skill_labels.get(x, x))
                
                st.markdown("### Loaded Data")
                st.dataframe(
                    history_df[['Skill', 'Result']].reset_index(drop=True),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.error("CSV must have 'skill' and 'correct' columns")
        except Exception as e:
            st.error(f"Error parsing CSV: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: PREDICTIONS
# ─────────────────────────────────────────────────────────────────────────────

if student_sequence and len(student_sequence) > 0:
    st.markdown("---")
    st.subheader("2️⃣ Predictions")
    
    # Group by skill to show predictions
    from collections import defaultdict
    skill_sequences = defaultdict(list)
    
    for attempt in student_sequence:
        skill = attempt['skill']
        correct = attempt['correct']
        skill_sequences[skill].append(correct)
    
    # Create prediction cards with max 3 columns per row
    sorted_skills = sorted(skill_sequences.items())
    max_cols = 3
    
    for row_idx in range(0, len(sorted_skills), max_cols):
        row_skills = sorted_skills[row_idx:row_idx + max_cols]
        pred_cols = st.columns(len(row_skills), gap="medium")
        
        for col_idx, (skill, sequence) in enumerate(row_skills):
            with pred_cols[col_idx]:
                # Get BKT parameters for this skill
                skill_params = bkt_params.loc[int(skill)] if int(skill) in bkt_params.index else None
                
                if skill_params is not None:
                    bkt_result = predict_bkt(skill_params, sequence, skill)
                    
                    st.markdown(f"**Skill {skill}**")
                    
                    # Display metrics in a single column
                    st.metric(
                        "Predicted Success",
                        f"{bkt_result['predicted_prob_next']:.1%}"
                    )
                    
                    st.metric(
                        "Current Knowledge",
                        f"{bkt_result['final_knowledge_state']:.2f}"
                    )
                    
                    st.metric(
                        "Accuracy",
                        f"{bkt_result['accuracy']:.1%}"
                    )
                else:
                    st.warning(f"No BKT parameters for skill {skill}")
    
    # ─────────────────────────────────────────────────────────────────────────────
    # SECTION 3: DETAILED ANALYSIS
    # ─────────────────────────────────────────────────────────────────────────────
    
    st.markdown("---")
    st.subheader("3️⃣ Detailed Analysis")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("### Learning Trajectory")
        
        selected_skill_detail = st.selectbox(
            "Select skill for detailed view:",
            sorted(skill_sequences.keys()),
            format_func=lambda x: skill_labels.get(x, x),
            key="detail_skill"
        )
        
        if selected_skill_detail in skill_sequences:
            skill_params = bkt_params.loc[int(selected_skill_detail)] if int(selected_skill_detail) in bkt_params.index else None
            
            if skill_params is not None:
                sequence = skill_sequences[selected_skill_detail]
                bkt_result = predict_bkt(skill_params, sequence, selected_skill_detail)
                
                # Plot learning trajectory
                fig, ax = plt.subplots(figsize=(8, 5))
                
                attempts = list(range(1, len(bkt_result['all_predictions']) + 1))
                predictions = bkt_result['all_predictions']
                actual = sequence
                
                ax.plot(attempts, predictions, marker='o', label='Predicted P(correct)', 
                       linewidth=2, markersize=8, color='#1D9E75')
                
                # Color actual outcomes
                colors = ['#1D9E75' if c == 1 else '#EF9F27' for c in actual]
                ax.scatter(attempts, predictions, c=colors, s=150, zorder=5, alpha=0.7,
                          label='Outcome', edgecolors='black', linewidth=1.5)
                
                ax.set_xlabel('Attempt Number', fontsize=11, fontweight='bold')
                ax.set_ylabel('P(correct)', fontsize=11, fontweight='bold')
                ax.set_title(f'Knowledge State Evolution - Skill {selected_skill_detail}', 
                           fontsize=12, fontweight='bold')
                ax.set_ylim([0, 1])
                ax.grid(True, alpha=0.3)
                ax.legend()
                
                plt.tight_layout()
                st.pyplot(fig)
    
    with col2:
        st.markdown("### BKT Parameters")
        
        selected_skill_params = st.selectbox(
            "Select skill for parameters:",
            sorted(skill_sequences.keys()),
            format_func=lambda x: skill_labels.get(x, x),
            key="param_skill"
        )
        
        if selected_skill_params in skill_sequences:
            skill_params = bkt_params.loc[int(selected_skill_params)]
            
            st.markdown("#### Estimated Parameters")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Prior P(L₀)", f"{skill_params['prior']:.3f}")
                st.caption("Initial knowledge probability")
                
                st.metric("Learning Rate", f"{skill_params['learn']:.3f}")
                st.caption("Rate of knowledge gain")
            
            with col_b:
                st.metric("Guess", f"{skill_params['guess']:.3f}")
                st.caption("Probability of lucky guess")
                
                st.metric("Slip", f"{skill_params['slip']:.3f}")
                st.caption("Probability of careless error")
            
            st.markdown("#### Interpretation")
            
            if skill_params['prior'] > 0.7:
                st.success("✓ Students start with high prior knowledge")
            else:
                st.warning("⚠ Low prior knowledge — skill needs teaching")
            
            if skill_params['learn'] > 0.15:
                st.success("✓ High learning rate — skill is learnable")
            else:
                st.warning("⚠ Low learning rate — skill may be hard to master")
    
    # ─────────────────────────────────────────────────────────────────────────────
    # SECTION 4: MODEL COMPARISON
    # ─────────────────────────────────────────────────────────────────────────────
    
    st.markdown("---")
    st.subheader("4️⃣ BKT vs DKT Comparison")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("### What is BKT?")
        st.markdown("""
        **Bayesian Knowledge Tracing:**
        - Population-level model
        - Assumes all students with same history have same knowledge
        - Four parameters per skill
        - Fast and interpretable
        - Good for understanding skill difficulty
        
        **Best for:**
        - Understanding skill properties
        - Quick estimates
        - Explaining to stakeholders
        """)
    
    with col2:
        st.markdown("### What is DKT?")
        st.markdown("""
        **Deep Knowledge Tracing:**
        - Individual-level model
        - LSTM neural network
        - Captures complex temporal patterns
        - More flexible, less interpretable
        - Better at capturing individual differences
        
        **Best for:**
        - Personalized predictions
        - Complex learning patterns
        - Modern ML systems
        """)
    
    # Side-by-side prediction comparison
    st.markdown("### Prediction Comparison")
    
    comparison_skill = st.selectbox(
        "Select skill to compare models:",
        sorted(skill_sequences.keys()),
        format_func=lambda x: skill_labels.get(x, x),
        key="compare_skill"
    )
    
    if comparison_skill in skill_sequences:
        skill_params = bkt_params.loc[int(comparison_skill)]
        sequence = skill_sequences[comparison_skill]
        
        comparison = compare_models(skill_params, sequence, comparison_skill)
        
        col_bkt, col_dkt = st.columns(2)
        
        with col_bkt:
            st.metric(
                "🎯 BKT Prediction",
                f"{comparison['bkt']['predicted_prob']:.1%}",
            )
            st.caption(f"Knowledge state: {comparison['bkt']['knowledge_state']:.3f}")
        
        with col_dkt:
            st.metric(
                "🧠 DKT Prediction",
                f"{comparison['dkt']['predicted_prob']:.1%}",
            )
            st.caption("Recency-weighted estimate")
        
        # Show why they might differ
        diff = abs(comparison['bkt']['predicted_prob'] - comparison['dkt']['predicted_prob'])
        if diff > 0.15:
            st.warning(
                f"⚠️ Models disagree significantly ({diff:.1%} difference). "
                f"Check recent performance vs. overall pattern."
            )

else:
    st.info("""
    👈 **No student data yet**
    
    Add student interaction history using one of the input methods above to see predictions.
    """)

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5: NEXT DATAPOINT PREDICTION
# ─────────────────────────────────────────────────────────────────────────────

if student_sequence and len(student_sequence) > 0:
    st.markdown("---")
    st.subheader("5️⃣ Next Datapoint Prediction")
    st.markdown(
        "For each skill in the student's history, the table below predicts "
        "the **most likely outcome of their very next attempt**, combining BKT "
        "and DKT probabilities into a single ensemble estimate."
    )

    next_step_rows = []

    for skill, sequence in sorted(skill_sequences.items()):
        skill_params = bkt_params.loc[int(skill)] if int(skill) in bkt_params.index else None
        if skill_params is None:
            continue

        comparison = compare_models(skill_params, sequence, skill)

        bkt_prob  = comparison["bkt"]["predicted_prob"]   # P(correct) next attempt – BKT
        dkt_prob  = comparison["dkt"]["predicted_prob"]   # P(correct) next attempt – DKT
        ensemble  = (bkt_prob + dkt_prob) / 2            # simple average ensemble

        # Derive expected outcome label and confidence
        if ensemble >= 0.5:
            outcome_label = "✅ Correct"
            confidence    = ensemble          # how sure we are it is Correct
        else:
            outcome_label = "❌ Incorrect"
            confidence    = 1.0 - ensemble   # how sure we are it is Incorrect

        n_attempts    = len(sequence)
        n_correct     = sum(sequence)
        recent_trend  = (
            "↗ Improving"  if len(sequence) >= 3 and sum(sequence[-3:]) > sum(sequence[:3]) / max(len(sequence[:3]), 1)
            else "↘ Declining" if len(sequence) >= 3 and sum(sequence[-3:]) < sum(sequence[:3]) / max(len(sequence[:3]), 1)
            else "→ Stable"
        )

        # Build a short plain-English rationale
        if ensemble >= 0.75:
            rationale = f"Strong mastery signal — both models agree the student is likely to succeed."
        elif ensemble >= 0.5:
            rationale = f"Moderate confidence — models lean toward success but some uncertainty remains."
        elif ensemble >= 0.25:
            rationale = f"Models lean toward an error — student may still be consolidating this skill."
        else:
            rationale = f"Low mastery signal — an incorrect answer is the most probable next outcome."

        next_step_rows.append({
            "skill":          skill,
            "n_attempts":     n_attempts,
            "accuracy":       n_correct / n_attempts if n_attempts else 0,
            "bkt_prob":       bkt_prob,
            "dkt_prob":       dkt_prob,
            "ensemble":       ensemble,
            "outcome_label":  outcome_label,
            "confidence":     confidence,
            "recent_trend":   recent_trend,
            "rationale":      rationale,
        })

    if next_step_rows:
        # Sort: highest confidence first
        next_step_rows.sort(key=lambda r: r["confidence"], reverse=True)

        # ── Summary cards (top 3 most certain predictions) ──────────────────
        top_n = min(3, len(next_step_rows))
        top_cols = st.columns(top_n, gap="medium")

        for i, row in enumerate(next_step_rows[:top_n]):
            with top_cols[i]:
                st.markdown(
                    f"""
                    <div style="
                        border: 1px solid #e0e0e0;
                        border-radius: 10px;
                        padding: 16px 18px;
                        background: #f9f9f9;
                        height: 100%;
                    ">
                        <div style="font-size:0.8em;color:#888;margin-bottom:4px;">
                            Skill {row['skill']} &nbsp;·&nbsp; {row['recent_trend']}
                        </div>
                        <div style="font-size:1.5em;font-weight:700;margin-bottom:6px;">
                            {row['outcome_label']}
                        </div>
                        <div style="font-size:0.85em;color:#555;margin-bottom:10px;">
                            Ensemble P(correct) = <strong>{row['ensemble']:.1%}</strong>
                            &nbsp;·&nbsp; confidence <strong>{row['confidence']:.1%}</strong>
                        </div>
                        <div style="background:#e8e8e8;border-radius:6px;height:8px;">
                            <div style="
                                background: {'#1D9E75' if row['ensemble'] >= 0.5 else '#EF9F27'};
                                width: {row['confidence']*100:.0f}%;
                                height:8px;
                                border-radius:6px;
                            "></div>
                        </div>
                        <div style="font-size:0.78em;color:#666;margin-top:8px;">
                            {row['rationale']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # ── Full table for all skills ────────────────────────────────────────
        if len(next_step_rows) > 1:
            st.markdown("#### All Skills — Next Attempt Forecast")

            table_df = pd.DataFrame([
                {
                    "Skill":             skill_labels.get(r["skill"], r["skill"]),
                    "Attempts":          r["n_attempts"],
                    "Accuracy":          f"{r['accuracy']:.0%}",
                    "Trend":             r["recent_trend"],
                    "BKT P(correct)":    f"{r['bkt_prob']:.1%}",
                    "DKT P(correct)":    f"{r['dkt_prob']:.1%}",
                    "Ensemble P(correct)": f"{r['ensemble']:.1%}",
                    "Predicted Outcome": r["outcome_label"],
                    "Confidence":        f"{r['confidence']:.1%}",
                }
                for r in next_step_rows
            ])

            st.dataframe(table_df, use_container_width=True, hide_index=True)

        # ── Insight callout ──────────────────────────────────────────────────
        st.markdown("---")
        high_conf  = [r for r in next_step_rows if r["confidence"] >= 0.75]
        low_conf   = [r for r in next_step_rows if r["confidence"] < 0.55]
        ready_next = [r for r in next_step_rows if r["ensemble"] >= 0.75]

        insight_parts = []
        if ready_next:
            skills_str = ", ".join(f"Skill {r['skill']}" for r in ready_next)
            insight_parts.append(
                f"🎓 **Ready to advance:** {skills_str} — both models predict success "
                f"with high probability."
            )
        if low_conf:
            skills_str = ", ".join(f"Skill {r['skill']}" for r in low_conf)
            insight_parts.append(
                f"🤔 **Models uncertain:** {skills_str} — BKT and DKT diverge; "
                f"collect more data before drawing conclusions."
            )

        if insight_parts:
            for part in insight_parts:
                st.info(part)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6: DKT FUTURE SEQUENCE PREDICTION
# ─────────────────────────────────────────────────────────────────────────────

if student_sequence and len(student_sequence) > 0:
    st.markdown("---")
    st.subheader("6️⃣ DKT Future Sequence Prediction")
    st.markdown(
        "Select a skill and number of future steps. The model will predict each step "
        "using the student's history, then feed that prediction back as input for the next — "
        "simulating how the student's knowledge state evolves over time."
    )

    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        forecast_skill = st.selectbox(
            "Skill to forecast:",
            sorted(skill_sequences.keys()),
            format_func=lambda x: skill_labels.get(x, x),
            key="forecast_skill"
        )

        n_steps = st.slider(
            "Steps to predict ahead:",
            min_value=1,
            max_value=20,
            value=5,
            key="forecast_steps"
        )

        st.markdown("---")
        st.markdown("##### How it works")
        st.markdown("""
        1. Start from the student's **real interaction history** for the chosen skill  
        2. Predict P(correct) for step N using DKT  
        3. The predicted outcome (correct if P ≥ 0.5) is added to the history  
        4. Repeat for step N+1, N+2, …  
        
        **Confidence** = how strongly the model commits to its prediction  
        (distance from 0.5, scaled to 0–100%)
        """)

    with col2:
        # ── Run the DKT forward simulation ───────────────────────────────────
        def dkt_predict_next(interaction_history, skill):
            """Single DKT step: recency-weighted P(correct) for `skill`."""
            skill_history = [
                i for i in interaction_history if i.get("skill") == skill
            ]
            if not skill_history:
                return 0.5  # no data → prior

            weight_sum = 0.0
            weighted_correct = 0.0
            n = len(skill_history)

            for idx, interaction in enumerate(skill_history):
                time_weight = np.exp((idx - n) / 5)
                weighted_correct += interaction["correct"] * time_weight
                weight_sum += time_weight

            raw_prob = weighted_correct / weight_sum if weight_sum > 0 else 0.5
            # smooth toward 0.5 prior (same as predict_dkt_simple)
            return max(0.05, min(0.95, 0.7 * raw_prob + 0.3 * 0.5))

        # Build a mutable copy of history for the chosen skill
        running_history = list(student_sequence)   # all skills, for context
        skill_history_only = [
            i for i in running_history if i["skill"] == forecast_skill
        ]
        n_real = len(skill_history_only)

        rows = []
        cumulative_log_conf = 0.0  # log-sum for chain confidence

        for step in range(1, n_steps + 1):
            prob = dkt_predict_next(running_history, forecast_skill)

            predicted_correct = 1 if prob >= 0.5 else 0
            outcome_label     = "✅ Correct" if predicted_correct == 1 else "❌ Incorrect"

            # Confidence = how far from 0.5, mapped to 0–100%
            step_confidence = abs(prob - 0.5) * 2   # 0 = total uncertainty, 1 = certain

            # Chain confidence: geometric mean of step confidences so far
            # Use a floor so log is defined
            cumulative_log_conf += np.log(max(step_confidence, 0.01))
            chain_confidence = np.exp(cumulative_log_conf / step)

            rows.append({
                "Step":              step,
                "Attempt #":         n_real + step,
                "P(correct)":        prob,
                "Predicted Outcome": outcome_label,
                "Step Confidence":   step_confidence,
                "Chain Confidence":  chain_confidence,
            })

            # Feed prediction back into history for next step
            running_history.append({
                "skill":   forecast_skill,
                "correct": predicted_correct,
            })

        # ── Render table ─────────────────────────────────────────────────────
        display_df = pd.DataFrame([
            {
                "Step":              r["Step"],
                "Attempt #":         r["Attempt #"],
                "P(correct)":        f"{r['P(correct)']:.1%}",
                "Predicted Outcome": r["Predicted Outcome"],
                "Step Confidence":   f"{r['Step Confidence']:.1%}",
                "Chain Confidence":  f"{r['Chain Confidence']:.1%}",
            }
            for r in rows
        ])

        st.markdown(
            f"**Skill {forecast_skill}** — based on "
            f"**{n_real} real attempt{'s' if n_real != 1 else ''}**, "
            f"predicting next **{n_steps} step{'s' if n_steps != 1 else ''}**"
        )
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        # ── Chain confidence callout ──────────────────────────────────────────
        final_chain_conf = rows[-1]["Chain Confidence"]
        if final_chain_conf >= 0.60:
            st.success(
                f"✅ Overall chain confidence: **{final_chain_conf:.1%}** — "
                f"the model is reasonably certain about this sequence."
            )
        elif final_chain_conf >= 0.35:
            st.warning(
                f"⚠️ Overall chain confidence: **{final_chain_conf:.1%}** — "
                f"predictions become less certain further into the future."
            )
        else:
            st.error(
                f"❌ Overall chain confidence: **{final_chain_conf:.1%}** — "
                f"high uncertainty; more student data would help."
            )

        st.caption(
            "**Step Confidence**: how strongly the model commits to this single step (0% = coin-flip, 100% = certain).  "
            "**Chain Confidence**: geometric mean of all step confidences up to this point — degrades as uncertainty compounds."
        )


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; font-size: 0.9em;">
    <p>💡 <strong>Tip:</strong> Combine predictions from both models for best results.</p>
    <p>BKT is reliable and interpretable; DKT captures individual patterns.</p>
</div>
""", unsafe_allow_html=True)