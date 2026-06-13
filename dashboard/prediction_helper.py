"""
Helper module for BKT and DKT predictions
"""

import numpy as np
import pandas as pd
from pathlib import Path


# ─────────────────────────────────────────────────────────────────────────────
# BKT PREDICTION FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def forward_pass_bkt(sequence, prior, learn, guess, slip):
    """
    Compute filtered knowledge state and predictions using BKT forward pass.
    
    Parameters:
    -----------
    sequence : list of int
        Binary correctness values (0 or 1) for each attempt
    prior : float
        P(L₀) - initial probability of knowledge
    learn : float
        Learning rate - probability of transitioning from unknown to known
    guess : float
        Probability of correct answer without knowledge
    slip : float
        Probability of incorrect answer despite having knowledge
    
    Returns:
    --------
    dict with:
        - predictions: list of P(correct) at each step
        - final_knowledge: P(L) after seeing all attempts
        - sequence_log_likelihood: log probability of observed sequence
    """
    p_l = prior
    predictions = []
    log_likelihood = 0.0
    
    for correct in sequence:
        # P(correct | knowledge state)
        p_correct = p_l * (1 - slip) + (1 - p_l) * guess
        predictions.append(p_correct)
        
        # Bayes update of knowledge state
        if correct == 1:
            numerator = p_l * (1 - slip)
            denominator = numerator + (1 - p_l) * guess
        else:
            numerator = p_l * slip
            denominator = numerator + (1 - p_l) * (1 - guess)
        
        p_l_given_obs = numerator / denominator if denominator > 0 else p_l
        
        # Update log likelihood
        log_likelihood += np.log(denominator) if denominator > 0 else -1e6
        
        # State transition (learning happens)
        p_l = p_l_given_obs + (1 - p_l_given_obs) * learn
    
    return {
        'predictions': predictions,
        'final_knowledge': p_l,
        'next_prediction': p_l * (1 - slip) + (1 - p_l) * guess,
        'sequence_log_likelihood': log_likelihood,
    }


def predict_bkt(bkt_params, sequence, skill_id=None):
    """
    Make a prediction for the next attempt using BKT parameters.
    
    Parameters:
    -----------
    bkt_params : pd.DataFrame or dict
        BKT parameters (prior, learn, guess, slip) for a skill
    sequence : list of int
        Binary correctness sequence
    skill_id : optional
        For reference/documentation
    
    Returns:
    --------
    dict with predictions and analysis
    """
    if isinstance(bkt_params, pd.Series):
        prior = bkt_params['prior']
        learn = bkt_params['learn']
        guess = bkt_params['guess']
        slip = bkt_params['slip']
    elif isinstance(bkt_params, dict):
        prior = bkt_params.get('prior', 0.3)
        learn = bkt_params.get('learn', 0.1)
        guess = bkt_params.get('guess', 0.2)
        slip = bkt_params.get('slip', 0.1)
    else:
        raise ValueError("bkt_params must be a DataFrame Series or dict")
    
    result = forward_pass_bkt(sequence, prior, learn, guess, slip)
    
    return {
        'skill_id': skill_id,
        'n_attempts': len(sequence),
        'correct_count': sum(sequence),
        'accuracy': sum(sequence) / len(sequence) if sequence else 0,
        'bkt_params': {
            'prior': prior,
            'learn': learn,
            'guess': guess,
            'slip': slip,
        },
        'predicted_prob_next': result['next_prediction'],
        'final_knowledge_state': result['final_knowledge'],
        'all_predictions': result['predictions'],
    }


def load_bkt_parameters(bkt_params_path=None):
    """Load BKT parameters from CSV file."""
    if bkt_params_path is None:
        bkt_params_path = Path(__file__).parent.parent / "bkt_params.csv"
    
    if not Path(bkt_params_path).exists():
        raise FileNotFoundError(f"BKT parameters file not found: {bkt_params_path}")
    
    df = pd.read_csv(bkt_params_path)
    # Use skill ID as index
    if 'skill' in df.columns:
        df = df.set_index('skill')
    
    return df


# ─────────────────────────────────────────────────────────────────────────────
# DKT PREDICTION FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def predict_dkt_simple(interaction_history, skill_embedding_dim=5):
    """
    Simple DKT prediction using a basic LSTM-inspired update rule.
    
    This is a simplified version that doesn't require a full trained model.
    In production, you'd load the actual trained PyTorch model.
    
    Parameters:
    -----------
    interaction_history : list of dict
        Each dict should have: {'skill': skill_id, 'correct': 0/1}
    skill_embedding_dim : int
        Dimension of skill embeddings
    
    Returns:
    --------
    dict with predictions for each skill
    """
    # Simple heuristic: decay recent performance by skill
    skill_performance = {}
    
    for i, interaction in enumerate(interaction_history):
        skill = interaction.get('skill', 'unknown')
        correct = interaction.get('correct', 0)
        
        # Weight recent interactions more heavily (exponential decay)
        time_weight = np.exp((i - len(interaction_history)) / 5)
        
        if skill not in skill_performance:
            skill_performance[skill] = {'sum_weighted': 0, 'weight_sum': 0}
        
        skill_performance[skill]['sum_weighted'] += correct * time_weight
        skill_performance[skill]['weight_sum'] += time_weight
    
    # Compute predicted probabilities
    predictions = {}
    for skill, stats in skill_performance.items():
        if stats['weight_sum'] > 0:
            prob = stats['sum_weighted'] / stats['weight_sum']
            # Smooth with a prior (0.5)
            smoothed_prob = 0.7 * prob + 0.3 * 0.5
            predictions[skill] = max(0.1, min(0.9, smoothed_prob))
        else:
            predictions[skill] = 0.5
    
    return {
        'skill_predictions': predictions,
        'n_interactions': len(interaction_history),
        'model_type': 'DKT (simplified)',
    }


# ─────────────────────────────────────────────────────────────────────────────
# UTILITY FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def create_sample_learner_sequence(skills, n_attempts=10):
    """Create a sample learner sequence for testing."""
    sequence = []
    for i in range(n_attempts):
        skill = np.random.choice(skills)
        # Simulate improving performance over time
        prob_correct = 0.3 + 0.5 * (i / n_attempts)
        correct = 1 if np.random.random() < prob_correct else 0
        sequence.append({'skill': skill, 'correct': correct})
    return sequence


def compare_models(bkt_params, sequence, skill_id=None):
    """Compare predictions between BKT and simplified DKT."""
    
    bkt_result = predict_bkt(bkt_params, sequence, skill_id)
    
    dkt_result = predict_dkt_simple(
        [{'skill': skill_id, 'correct': c} for c in sequence]
    )
    
    comparison = {
        'bkt': {
            'model': 'BKT',
            'predicted_prob': bkt_result['predicted_prob_next'],
            'knowledge_state': bkt_result['final_knowledge_state'],
            'description': f"BKT estimates P(L)={bkt_result['final_knowledge_state']:.3f}",
        },
        'dkt': {
            'model': 'DKT',
            'predicted_prob': dkt_result['skill_predictions'].get(skill_id, 0.5),
            'description': f"DKT uses recency-weighted history",
        },
    }
    
    return comparison
