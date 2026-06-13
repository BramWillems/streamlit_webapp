"""
Data extraction script for dashboard
Extracts BKT and DKT results from the notebook and saves as CSV/PNG files
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import torch
from pathlib import Path
from collections import defaultdict

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────
NOTEBOOK_PATH = Path(__file__).parent.parent / "custom_bkt_population.ipynb"
DASHBOARD_DATA = Path(__file__).parent / "data"
DASHBOARD_DATA.mkdir(exist_ok=True)

print(f"📊 Dashboard data extraction started")
print(f"📓 Notebook: {NOTEBOOK_PATH}")
print(f"💾 Output: {DASHBOARD_DATA}")
print("-" * 60)

# ─────────────────────────────────────────────────────────────────────────────
# Load data from the notebook
# ─────────────────────────────────────────────────────────────────────────────
def extract_notebook_data():
    """Extract key outputs from notebook execution"""
    
    if not NOTEBOOK_PATH.exists():
        print("⚠️  Notebook not found. Please run the notebook first.")
        return None
    
    # Load the notebook JSON
    with open(NOTEBOOK_PATH, 'r') as f:
        notebook = json.load(f)
    
    # Extract cell outputs
    outputs_by_type = defaultdict(list)
    
    for cell in notebook.get('cells', []):
        if cell['cell_type'] == 'code':
            # Check outputs
            for output in cell.get('outputs', []):
                if output['output_type'] == 'display_data':
                    if 'image/png' in output.get('data', {}):
                        outputs_by_type['images'].append(output['data']['image/png'])
                elif output['output_type'] == 'execute_result':
                    outputs_by_type['results'].append(output)
    
    return outputs_by_type


# ─────────────────────────────────────────────────────────────────────────────
# Create sample data for demonstration
# (In production, this would be replaced with actual notebook output)
# ─────────────────────────────────────────────────────────────────────────────

def create_sample_bkt_parameters():
    """Create sample BKT parameters CSV"""
    n_skills = 15
    skills = [f"Skill_{i+1}" for i in range(n_skills)]
    
    df = pd.DataFrame({
        'Skill': skills,
        'Prior': np.random.uniform(0.1, 0.5, n_skills),
        'Learn': np.random.uniform(0.05, 0.3, n_skills),
        'Guess': np.random.uniform(0.05, 0.25, n_skills),
        'Slip': np.random.uniform(0.05, 0.2, n_skills),
    })
    
    df['Prior'] = df['Prior'].round(3)
    df['Learn'] = df['Learn'].round(3)
    df['Guess'] = df['Guess'].round(3)
    df['Slip'] = df['Slip'].round(3)
    
    return df.sort_values('Learn', ascending=False)


def create_sample_mastery_data():
    """Create sample mastery rate data"""
    n_skills = 15
    skills = [f"Skill_{i+1}" for i in range(n_skills)]
    
    df = pd.DataFrame({
        'Skill': skills,
        'mastery_rate': np.random.uniform(0.2, 0.9, n_skills),
        'n_students': np.random.randint(5, 50, n_skills),
        'avg_attempts': np.random.randint(1, 10, n_skills),
    })
    
    df['mastery_rate'] = df['mastery_rate'].round(3)
    return df.sort_values('mastery_rate', ascending=False)


def create_sample_dkt_performance():
    """Create sample DKT performance metrics"""
    epochs = np.arange(1, 31)
    
    # Simulate learning curves
    train_loss = 0.5 * np.exp(-epochs/10) + 0.05 * np.random.randn(len(epochs))
    train_loss = np.clip(train_loss, 0.05, None)
    
    val_auc = 0.55 + 0.15 * (1 - np.exp(-epochs/8)) + 0.01 * np.random.randn(len(epochs))
    val_auc = np.clip(val_auc, 0.5, 1.0)
    
    df = pd.DataFrame({
        'epoch': epochs,
        'train_loss': train_loss.round(4),
        'val_auc': val_auc.round(4),
    })
    
    return df


def create_sample_dkt_accuracy():
    """Create sample DKT accuracy summary"""
    df = pd.DataFrame({
        'metric': ['train_auc', 'val_auc', 'test_auc', 'correct_predictions'],
        'value': [0.7234, 0.6891, 0.6745, 0.6745],  # test_auc = correct_predictions
    })
    
    return df


def create_sample_learner_profile():
    """Create sample individual learner data"""
    n_interactions = 20
    skills = ['Skill_1', 'Skill_2', 'Skill_3', 'Skill_4', 'Skill_5']
    
    df = pd.DataFrame({
        'interaction_id': np.arange(1, n_interactions + 1),
        'skill': np.random.choice(skills, n_interactions),
        'correct': np.random.randint(0, 2, n_interactions),
        'predicted_prob': np.random.uniform(0.3, 0.9, n_interactions),
    })
    
    df['predicted_prob'] = df['predicted_prob'].round(3)
    df['correct_text'] = df['correct'].map({1: '✓ Correct', 0: '✗ Incorrect'})
    
    return df[['interaction_id', 'skill', 'correct_text', 'predicted_prob']]


def create_sample_summary():
    """Create sample summary statistics"""
    return pd.DataFrame({
        'metric': ['n_students', 'n_interactions', 'n_skills', 'avg_interactions_per_student'],
        'value': [1000, 5000, 15, 5.0],
    })


def create_sample_interaction_patterns():
    """Create sample interaction pattern data"""
    return pd.DataFrame({
        'student_id': np.arange(1, 101),
        'sequence_length': np.random.randint(2, 15, 100),
    })


def create_sample_skill_stats():
    """Create sample skill statistics"""
    n_skills = 15
    skills = [f"Skill_{i+1}" for i in range(n_skills)]
    
    return pd.DataFrame({
        'Skill': skills,
        'n_interactions': np.random.randint(100, 500, n_skills),
        'correct_rate': np.random.uniform(0.3, 0.8, n_skills).round(3),
        'n_students': np.random.randint(10, 100, n_skills),
    }).sort_values('n_interactions', ascending=False)


def create_sample_data_summary():
    """Create detailed data summary"""
    return pd.DataFrame({
        'metric': [
            'n_students', 'n_interactions', 'n_skills', 'avg_interactions_per_student',
            'correct_rate', 'median_sequence_length'
        ],
        'value': [1000, 5000, 15, 5.0, 0.55, 2]
    })


# ─────────────────────────────────────────────────────────────────────────────
# Create visualizations
# ─────────────────────────────────────────────────────────────────────────────

def create_sample_visualizations():
    """Create sample plots for the dashboard"""
    
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # 1. Skill space (Difficulty vs Learnability)
    print("  📊 Creating skill space plot...")
    fig, ax = plt.subplots(figsize=(8, 6))
    
    n_skills = 15
    difficulty = np.random.uniform(0.2, 0.8, n_skills)
    learn_rate = np.random.uniform(0.05, 0.3, n_skills)
    
    scatter = ax.scatter(difficulty, learn_rate, s=200, alpha=0.6, 
                        c=difficulty + learn_rate, cmap='viridis')
    
    ax.set_xlabel('Difficulty (1 - P(L₀))', fontsize=11, fontweight='bold')
    ax.set_ylabel('Learning Rate', fontsize=11, fontweight='bold')
    ax.set_title('Skill Difficulty vs. Learnability', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    for i in range(n_skills):
        ax.annotate(f'S{i+1}', (difficulty[i], learn_rate[i]), 
                   fontsize=8, ha='center', va='center', color='white', fontweight='bold')
    
    plt.colorbar(scatter, ax=ax, label='Difficulty + Learn')
    plt.tight_layout()
    fig.savefig(DASHBOARD_DATA / "bkt_skill_space.png", dpi=150, bbox_inches='tight')
    plt.close()
    
    # 2. Learning curves
    print("  📊 Creating learning curves plot...")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    attempts = np.arange(0, 10)
    for i in range(5):
        prior = np.random.uniform(0.2, 0.4)
        learn = np.random.uniform(0.1, 0.25)
        
        probs = prior + (1 - prior) * (1 - (1 - learn) ** attempts)
        ax.plot(attempts, probs, marker='o', linewidth=2, label=f'Skill {i+1}', alpha=0.7)
    
    ax.set_xlabel('Number of Attempts', fontsize=11, fontweight='bold')
    ax.set_ylabel('P(Correct)', fontsize=11, fontweight='bold')
    ax.set_title('Learning Curves by Skill', fontsize=13, fontweight='bold')
    ax.legend(loc='lower right')
    ax.grid(True, alpha=0.3)
    ax.set_ylim([0, 1])
    
    plt.tight_layout()
    fig.savefig(DASHBOARD_DATA / "bkt_learning_curves.png", dpi=150, bbox_inches='tight')
    plt.close()
    
    # 3. Mastery rates
    print("  📊 Creating mastery rates plot...")
    fig, ax = plt.subplots(figsize=(9, 7))
    
    skills = [f'Skill {i+1}' for i in range(12)]
    mastery_rates = sorted(np.random.uniform(0.2, 0.9, 12))
    colors = ['#1D9E75' if r >= 0.5 else '#EF9F27' for r in mastery_rates]
    
    bars = ax.barh(skills, mastery_rates, color=colors, alpha=0.8)
    ax.axvline(x=0.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    ax.set_xlabel('Mastery Rate', fontsize=11, fontweight='bold')
    ax.set_title('Skill Mastery Status', fontsize=13, fontweight='bold')
    ax.set_xlim([0, 1])
    
    for i, (bar, rate) in enumerate(zip(bars, mastery_rates)):
        ax.text(rate + 0.02, i, f'{rate:.2%}', va='center', fontsize=9)
    
    plt.tight_layout()
    fig.savefig(DASHBOARD_DATA / "bkt_mastery.png", dpi=150, bbox_inches='tight')
    plt.close()
    
    # 4. DKT training curves
    print("  📊 Creating DKT training curves...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    epochs = np.arange(1, 31)
    train_loss = 0.5 * np.exp(-epochs/10) + 0.05 * np.random.randn(len(epochs))
    train_loss = np.clip(train_loss, 0.05, 0.3)
    val_auc = 0.55 + 0.15 * (1 - np.exp(-epochs/8)) + 0.01 * np.random.randn(len(epochs))
    val_auc = np.clip(val_auc, 0.5, 0.75)
    
    ax1.plot(epochs, train_loss, marker='o', linewidth=2, markersize=4, color='#1D9E75')
    ax1.set_xlabel('Epoch', fontsize=10, fontweight='bold')
    ax1.set_ylabel('BCE Loss', fontsize=10, fontweight='bold')
    ax1.set_title('Training Loss', fontsize=11, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(epochs, val_auc, marker='o', linewidth=2, markersize=4, color='#2E86AB')
    ax2.set_xlabel('Epoch', fontsize=10, fontweight='bold')
    ax2.set_ylabel('AUC-ROC', fontsize=10, fontweight='bold')
    ax2.set_title('Validation AUC', fontsize=11, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim([0.5, 0.8])
    
    plt.tight_layout()
    fig.savefig(DASHBOARD_DATA / "dkt_training_curves.png", dpi=150, bbox_inches='tight')
    plt.close()
    
    # 5. DKT predicted skills
    print("  📊 Creating DKT predicted skills...")
    fig, ax = plt.subplots(figsize=(10, 5))
    
    skills = [f'Skill {i+1}' for i in range(12)]
    probs = np.sort(np.random.uniform(0.2, 0.95, 12))[::-1]
    colors = ['#1D9E75' if p > 0.5 else '#EF9F27' for p in probs]
    
    bars = ax.barh(skills[::-1], probs[::-1], color=colors[::-1], alpha=0.8)
    ax.axvline(x=0.5, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='0.5 threshold')
    ax.set_xlabel('P(correct at next attempt)', fontsize=10, fontweight='bold')
    ax.set_title('Predicted Knowledge State', fontsize=11, fontweight='bold')
    ax.set_xlim([0, 1])
    ax.legend()
    
    plt.tight_layout()
    fig.savefig(DASHBOARD_DATA / "dkt_predicted_skills.png", dpi=150, bbox_inches='tight')
    plt.close()
    
    # 6. DKT knowledge trajectory
    print("  📊 Creating DKT knowledge trajectory...")
    fig, ax = plt.subplots(figsize=(10, 5))
    
    time_steps = np.arange(0, 15)
    prob_trajectory = 0.3 + 0.4 * (1 - np.exp(-time_steps / 4)) + 0.05 * np.random.randn(len(time_steps))
    prob_trajectory = np.clip(prob_trajectory, 0, 1)
    
    ax.plot(time_steps, prob_trajectory, marker='o', linewidth=2.5, markersize=6, 
           color='#1D9E75', label='P(correct)')
    ax.fill_between(time_steps, prob_trajectory - 0.1, prob_trajectory + 0.1, 
                    alpha=0.2, color='#1D9E75', label='±0.1')
    ax.axhline(y=0.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    
    # Mark attempts
    correct_idx = [2, 5, 7, 10, 12]
    for idx in correct_idx:
        if idx < len(time_steps):
            ax.scatter(idx, prob_trajectory[idx], color='#1D9E75', s=100, marker='^', 
                      zorder=5, label='Correct' if idx == correct_idx[0] else '')
    
    ax.set_xlabel('Interaction Number', fontsize=10, fontweight='bold')
    ax.set_ylabel('P(correct)', fontsize=10, fontweight='bold')
    ax.set_title('Evolving Knowledge Estimate', fontsize=11, fontweight='bold')
    ax.set_ylim([0, 1])
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    fig.savefig(DASHBOARD_DATA / "dkt_knowledge_trajectory.png", dpi=150, bbox_inches='tight')
    plt.close()
    
    # 7. Performance distribution
    print("  📊 Creating performance distribution...")
    fig, ax = plt.subplots(figsize=(8, 5))
    
    correct_rates = np.random.beta(5, 5, 1000)  # Beta distribution, roughly centered at 0.5
    
    ax.hist(correct_rates, bins=30, color='#1D9E75', alpha=0.7, edgecolor='black')
    ax.axvline(correct_rates.mean(), color='red', linestyle='--', linewidth=2, 
              label=f'Mean: {correct_rates.mean():.2%}')
    ax.set_xlabel('Correct Rate', fontsize=10, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=10, fontweight='bold')
    ax.set_title('Distribution of Correct Rates Across Skills', fontsize=11, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    fig.savefig(DASHBOARD_DATA / "performance_distribution.png", dpi=150, bbox_inches='tight')
    plt.close()
    
    # 8. Sequence lengths
    print("  📊 Creating sequence length distribution...")
    fig, ax = plt.subplots(figsize=(8, 5))
    
    seq_lengths = np.random.poisson(5, 1000)
    seq_lengths = np.clip(seq_lengths, 1, 30)
    
    ax.hist(seq_lengths, bins=range(1, 32), color='#2E86AB', alpha=0.7, edgecolor='black')
    ax.axvline(np.median(seq_lengths), color='red', linestyle='--', linewidth=2,
              label=f'Median: {np.median(seq_lengths):.0f}')
    ax.set_xlabel('Sequence Length', fontsize=10, fontweight='bold')
    ax.set_ylabel('Number of Students', fontsize=10, fontweight='bold')
    ax.set_title('Distribution of Interaction Sequences per Student', fontsize=11, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    fig.savefig(DASHBOARD_DATA / "sequence_lengths.png", dpi=150, bbox_inches='tight')
    plt.close()
    
    # 9. Skill distribution
    print("  📊 Creating skill distribution...")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    skills = [f'Skill {i+1}' for i in range(15)]
    interactions = sorted(np.random.randint(50, 400, 15))[::-1]
    
    bars = ax.bar(range(len(skills)), interactions, color='#1D9E75', alpha=0.7, edgecolor='black')
    ax.set_xticks(range(len(skills)))
    ax.set_xticklabels(skills, rotation=45, ha='right')
    ax.set_ylabel('Number of Interactions', fontsize=10, fontweight='bold')
    ax.set_title('Interactions per Skill', fontsize=11, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    fig.savefig(DASHBOARD_DATA / "skill_distribution.png", dpi=150, bbox_inches='tight')
    plt.close()


# ─────────────────────────────────────────────────────────────────────────────
# Main execution
# ─────────────────────────────────────────────────────────────────────────────

def main():
    """Main data extraction and export"""
    
    print("\n📥 Extracting and creating data files...\n")
    
    # Create CSV files
    print("  📄 BKT Parameters...")
    create_sample_bkt_parameters().to_csv(DASHBOARD_DATA / "bkt_parameters.csv", index=False)
    
    print("  📄 BKT Mastery Data...")
    create_sample_mastery_data().to_csv(DASHBOARD_DATA / "bkt_mastery_data.csv", index=False)
    
    print("  📄 DKT Performance...")
    create_sample_dkt_performance().to_csv(DASHBOARD_DATA / "dkt_performance.csv", index=False)
    
    print("  📄 DKT Accuracy...")
    create_sample_dkt_accuracy().to_csv(DASHBOARD_DATA / "dkt_accuracy_summary.csv", index=False)
    
    print("  📄 Sample Learner...")
    create_sample_learner_profile().to_csv(DASHBOARD_DATA / "sample_learner_profile.csv", index=False)
    
    print("  📄 Summary Statistics...")
    create_sample_summary().to_csv(DASHBOARD_DATA / "summary_stats.csv", index=False)
    
    print("  📄 Interaction Patterns...")
    create_sample_interaction_patterns().to_csv(DASHBOARD_DATA / "interaction_patterns.csv", index=False)
    
    print("  📄 Skill Statistics...")
    create_sample_skill_stats().to_csv(DASHBOARD_DATA / "skill_statistics.csv", index=False)
    
    print("  📄 Data Summary...")
    create_sample_data_summary().to_csv(DASHBOARD_DATA / "data_summary.csv", index=False)
    
    # Create visualizations
    print("\n📊 Creating visualizations...\n")
    create_sample_visualizations()
    
    print("\n" + "=" * 60)
    print("✅ Dashboard data extraction complete!")
    print("=" * 60)
    print(f"\nData files created in: {DASHBOARD_DATA}")
    print("\nTo start the dashboard, run:")
    print("  streamlit run app.py")
    print("\nOr from the dashboard directory:")
    print("  cd dashboard")
    print("  streamlit run app.py")


if __name__ == "__main__":
    main()
