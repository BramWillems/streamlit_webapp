import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Project Overview", page_icon="📘", layout="wide")

st.title("📘 Project Overview & Methodology")
st.markdown("---")

st.markdown("""
This page exists to answer the questions a reader needs answered **before** the rest of
the dashboard makes sense: *what is this for, who is it for, what do the numbers mean,
and why these two models?* Read this page first.
""")

DATA_DIR = Path(__file__).parent.parent / "data"


def load_csv(name):
    """Load a CSV from the data directory if it exists, else return None."""
    path = DATA_DIR / name
    if path.exists():
        try:
            return pd.read_csv(path)
        except Exception:
            return None
    return None


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: WHAT IS THIS PROJECT, AND WHO IS IT FOR?
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("1️⃣ What Is This Project, and Who Is It For?")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("""
    ### The problem

    A student answers a question correctly or incorrectly, but that single data point
    doesn't tell an instructor **why**. Did the student already know the material and
    just slip up? Are they guessing? Are they on a genuine upward learning trajectory,
    or stuck?

    Knowledge tracing tries to answer that by turning a raw stream of
    right/wrong attempts into an estimate of what a student actually **knows**, and a
    forecast of how they'll do **next time** — separately for every skill they
    practice.

    This project builds two such models — **BKT** and **DKT** — and packages their
    output into a dashboard that lets someone inspect skills, students, and
    predictions without touching code.
    """)

with col2:
    st.markdown("""
    ### Who it's for, and what decision it supports

    | Audience | Decision this dashboard informs |
    |---|---|
    | **Instructors / tutors** | Which students need help, and on which specific skill, *before* a test reveals it |
    | **Curriculum designers** | Which skills are structurally hard to learn (low prior, low learning rate) vs. just under-practiced |
    | **Learning scientists / reviewers** | Whether a population-level model (BKT) or an individual-level model (DKT) better fits this dataset, and why |

    **The goal in one sentence:** estimate per-skill mastery and forecast next-attempt
    performance, accurately enough and transparently enough that someone can act on it —
    re-teach, give more practice, or move a student forward.
    """)

st.info(
    "📖 **How this maps to the rest of the guide:** the hand-in guide explains how the "
    "raw interaction data is cleaned and turned into the model inputs in the `/data` "
    "folder. This dashboard is what happens **after** that step — it is the "
    "presentation and interpretation layer on top of the fitted models."
)

st.markdown("#### Where to find what")
nav_df = pd.DataFrame([
    {"Page": "📋 Data Overview", "Answers": "What does the raw dataset look like, and is it suitable for these models?"},
    {"Page": "📈 BKT Analysis", "Answers": "Which skills are easy/hard, fast/slow to learn, at the population level?"},
    {"Page": "🧠 DKT Analysis", "Answers": "How well does the neural model predict performance, and how confident should we be in that?"},
    {"Page": "🔮 Student Predictions", "Answers": "Given one specific student's history, what should happen next?"},
])
st.dataframe(nav_df, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: HOW TO READ A PREDICTION
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("2️⃣ How to Read a Prediction — and What to Do About It")

st.markdown("""
The dashboard reports a few different numbers that look similar but answer different
questions. Mixing them up is the most common misreading, so here's the distinction
worked through with a concrete example.
""")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("""
    ### Worked example: "P(correct) = 0.73"

    Say a skill shows a **predicted probability of correct response of 0.73** for a
    student's next attempt. That number is the model's belief about the **next
    observable event** — it is *not* the same as "73% mastered."

    BKT actually separates two things that this single number blends together:

    - **Knowledge state** — the model's hidden estimate of whether the student
      *truly* knows the skill (shown as "Current Knowledge" in Student Predictions).
    - **P(correct)** — knowledge state adjusted for **guess** (could be right
      without knowing it) and **slip** (could be wrong despite knowing it).

    So a high P(correct) driven mainly by a high *guess* rate is a weaker signal than
    the same P(correct) driven by a high *knowledge state*. **Always check both
    numbers, not just P(correct), before deciding a student has mastered something.**
    """)

with col2:
    st.markdown("### Interpretation guide (the thresholds the dashboard itself uses)")
    interp_df = pd.DataFrame([
        {"P(correct)": "0% – 25%", "What it signals": "Skill likely not yet learned",
         "Suggested action": "Re-teach the underlying concept"},
        {"P(correct)": "25% – 50%", "What it signals": "Fragile or partial understanding",
         "Suggested action": "Provide additional guided practice"},
        {"P(correct)": "50% – 75%", "What it signals": "Leaning correct, some uncertainty remains",
         "Suggested action": "Monitor; light scaffolding"},
        {"P(correct)": "75% – 100%", "What it signals": "Strong mastery signal",
         "Suggested action": "Move on to the next skill"},
    ])
    st.dataframe(interp_df, use_container_width=True, hide_index=True)

    st.markdown("""
    Two more thresholds used elsewhere in the dashboard, for reference:
    - **Mastery rate ≥ 50%** marks a skill as "mastered" at the population level
      (BKT Analysis page).
    - **Confidence ≥ 75%** is flagged as a high-confidence prediction; **below 55%**
      is flagged as genuinely uncertain — meaning collect more attempts before acting
      (Student Predictions page).
    """)

st.warning(
    "⚠️ **These are decision-support numbers, not ground truth.** A model output should "
    "lower the cost of deciding where to look first — it should not be the sole basis "
    "for a high-stakes decision about a real student without a teacher's judgment."
)

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: METHODOLOGY
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("3️⃣ Methodology")

method_tab1, method_tab2, method_tab3 = st.tabs(
    ["🤔 Why BKT *and* DKT?", "⚙️ Training & Configuration", "✅ Validation & Results"]
)

with method_tab1:
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("""
        #### Why Bayesian Knowledge Tracing

        BKT was chosen because it is the standard, well-understood baseline in the
        knowledge-tracing literature, and because of a specific property of this
        dataset: per the Data Overview page, the median student has only **~2
        attempts per skill**. That's too sparse to reliably fit an individual model
        per student. BKT sidesteps this by fitting **one set of four parameters per
        skill**, shared across all students — it only needs to be reliable in
        aggregate, not per person, which matches what the data can actually support.

        It also gives directly interpretable outputs (prior knowledge, learning
        rate, guess, slip) that map onto pedagogical questions a non-technical
        stakeholder can act on, which a black-box model alone would not.
        """)
    with col2:
        st.markdown("""
        #### Why Deep Knowledge Tracing

        DKT was added specifically to capture what BKT structurally cannot: BKT
        assumes every student with the same history has the same knowledge state,
        and treats each skill independently. In reality, struggling on one skill
        can be informative about another, and performance trends within a single
        sequence carry information BKT's fixed parameters don't use.

        A recurrent (LSTM) architecture can share information across a student's
        *entire* interaction sequence, not just one skill at a time, so it can still
        produce individualized estimates even when any single skill's history is
        short — directly addressing the sparsity limitation above.

        **In short:** BKT was chosen for interpretability and to match population
        skill-level analysis; DKT was added to test whether modeling sequence and
        individual variation captures something BKT's assumptions miss. The
        dashboard reports both, and where they disagree, that disagreement is
        itself informative (flagged explicitly in Student Predictions).
        """)

with method_tab2:
    st.markdown("""
    #### BKT
    Parameters were fit with **Expectation-Maximization**, one prior/learn/guess/slip
    set per skill, using **all available interaction data** — BKT does not require a
    held-out test set, since the goal is to characterize the skill itself rather than
    generalize to unseen students.

    #### DKT
    The LSTM was trained on skill-tagged interaction sequences with a **70% /
    15% / 15% train / validation / test split, stratified by student** (so no student's
    interactions appear in more than one split). Training minimizes a binary
    cross-entropy loss between predicted and actual correctness at each step;
    validation AUC is monitored across epochs to check for convergence and catch
    overfitting (see the training curves on the DKT Analysis page).
    """)
    st.info(
        "📝 **For the report:** record the exact architecture and training "
        "hyperparameters here — LSTM hidden size, number of layers, learning rate, "
        "batch size, optimizer, and number of epochs — pulled directly from the "
        "training notebook, so a reviewer can reproduce the run."
    )

with method_tab3:
    st.markdown("#### What the project's own data says about model quality")

    perf_df = load_csv("dkt_performance.csv")
    acc_df = load_csv("dkt_accuracy_summary.csv")
    mastery_df = load_csv("bkt_mastery_data.csv")
    summary_df = load_csv("data_summary.csv")

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        if perf_df is not None and "val_auc" in perf_df.columns:
            st.metric("DKT Validation AUC", f"{perf_df['val_auc'].iloc[-1]:.3f}")
        else:
            st.info("Run the notebook to populate DKT validation AUC")

    with col2:
        if acc_df is not None:
            test_auc = acc_df[acc_df["metric"] == "test_auc"]["value"].values
            if len(test_auc) > 0:
                st.metric("DKT Test AUC (held-out)", f"{test_auc[0]:.3f}")
            else:
                st.info("Test AUC not found")
        else:
            st.info("Run the notebook to populate DKT test AUC")

    with col3:
        if mastery_df is not None and "mastery_rate" in mastery_df.columns:
            st.metric("Mean BKT Mastery Rate", f"{mastery_df['mastery_rate'].mean():.1%}")
        else:
            st.info("Run the notebook to populate BKT mastery data")

    st.markdown("""
    **How to read this:** DKT's test AUC is the model's discrimination ability
    on students it never saw during training — this is the number that matters for
    judging real-world usefulness, not the training AUC. An AUC near 0.5 means the
    model is no better than chance; **0.75 and above is generally considered good
    discrimination** in the knowledge-tracing literature. BKT is validated
    differently — since it has no held-out set by design, its check is **calibration**:
    do predicted mastery rates line up with the actual proportion of correct answers
    observed for each skill (see the mastery plot on the BKT Analysis page)?
    """)

    if summary_df is not None:
        st.caption(
            "Dataset scale these results were computed on is shown on the Data "
            "Overview page (students, interactions, skills)."
        )

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: LIMITATIONS & FUTURE WORK
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("4️⃣ Limitations & Future Work")

lim1, lim2, lim3 = st.columns(3, gap="medium")

with lim1:
    st.markdown("""
    ### Model limitations

    - BKT assumes one knowledge state per skill shared by all students — it cannot
      represent individual differences within a skill.
    - With short per-skill sequences, guess and slip can be hard to estimate
      reliably (parameter identifiability).
    - DKT's ensemble with BKT uses a simple average; this heuristic hasn't been
      tuned or validated against an alternative weighting.
    """)

with lim2:
    st.markdown("""
    ### Evaluation limitations

    - AUC measures ranking ability, not calibration — a model can rank well while
      still being over- or under-confident in absolute probabilities.
    - No fairness or subgroup analysis has been done (e.g., performance across
      different student populations or skill categories).
    - Predictions are correlational; they describe patterns in past data and are
      not causal claims about why a student struggles.
    """)

with lim3:
    st.markdown("""
    ### Future work

    - Hyperparameter tuning and cross-validation for the LSTM.
    - Try attention-based knowledge-tracing models (e.g., SAKT/AKT) as a stronger
      DKT baseline.
    - Incorporate item difficulty explicitly (e.g., IRT-style features).
    - Pilot the dashboard with real instructors and measure whether it changes
      what they do, not just what they see.
    """)

st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #999; font-size: 0.9em;">
        <p>This page is the methodology companion to the rest of the dashboard —
        see the other pages for the underlying data, parameters, and predictions
        referenced above.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
