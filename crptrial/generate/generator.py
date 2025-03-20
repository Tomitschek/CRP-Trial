"""
Generator module for creating synthetic CRP data
"""
import numpy as np
import pandas as pd

def generate_patient_id():
    """Generate a random 8-digit ID starting with 64"""
    return int('64' + str(np.random.randint(000000, 1000000)).zfill(6))

def generate_crp_data(n_per_group=20, baseline_mean=5, baseline_sd=2, 
                     peak_treated=150, peak_control=180,
                     decay_treated=0.5, decay_control=0.3,
                     day_effects={3: 15, 4: 25, 5: 35, 6: 30, 7: 20},
                     random_seed=42):
    """
    Generate synthetic CRP data for two groups over 8 days (0-7)
    
    Parameters:
    -----------
    n_per_group : int
        Number of patients per group
    baseline_mean, baseline_sd : float
        Mean and SD of baseline CRP values
    peak_treated, peak_control : float
        Peak CRP values for treated and control groups
    decay_treated, decay_control : float
        Decay rate of CRP after peak for each group
    day_effects : dict
        Dictionary mapping days to effect sizes. Positive values mean treatment
        group has lower CRP values on that day. Default creates significant
        differences increasing from day 3 to day 5, then slightly decreasing.
    random_seed : int
        Random seed for reproducibility
    
    Returns:
    --------
    pandas.DataFrame with columns:
        - patient_id: unique identifier for each patient
        - group: treatment group (treated/control)
        - day: day of measurement (0-7)
        - crp: CRP value
    
    Examples:
    ---------
    # To create dataset with huge difference on day 5 only:
    df = generate_crp_data(day_effects={5: 50})
    
    # To create dataset with increasing treatment effect:
    df = generate_crp_data(day_effects={3: 10, 4: 20, 5: 30, 6: 40, 7: 50})
    """
    np.random.seed(random_seed)
    
    # Generate unique patient IDs
    patient_ids = [generate_patient_id() for _ in range(2 * n_per_group)]
    while len(set(patient_ids)) < len(patient_ids):  # Ensure uniqueness
        patient_ids = [generate_patient_id() for _ in range(2 * n_per_group)]
    
    # Time points
    days = np.arange(8)  # Days 0-7
    
    # Initialize empty lists to store data
    all_data = []
    
    def get_min_crp():
        """Helper function to generate random minimum CRP values"""
        return 0.5 + np.random.exponential(0.5)  # Random value between 0.5 and ~2.0
    
    # Generate data for each patient
    for idx, patient in enumerate(patient_ids):
        # Determine group
        is_treated = idx < n_per_group
        group = 'treated' if is_treated else 'control'
        
        # Generate individual patient characteristics
        baseline = np.random.normal(baseline_mean, baseline_sd)
        individual_variation = np.random.normal(0, 35)  # Further increased variation
        peak = peak_treated if is_treated else peak_control
        decay = decay_treated if is_treated else decay_control
        
        for day in days:
            if day == 0:
                crp = max(get_min_crp(), baseline + np.random.normal(0, 15))  # Ensure minimum CRP of 0.5
            else:
                # CRP rises to peak at day 2-3 then decays
                if day <= 2:
                    progress = day / 2
                    base_crp = baseline + (peak - baseline) * progress
                    # High variation for days 0-2 to ensure p > 0.1
                    crp = base_crp + np.random.normal(0, base_crp * 0.3)
                else:
                    # Exponential decay after peak
                    base_crp = peak * np.exp(-decay * (day - 2))
                    # Even more variation for days 3-7
                    crp = base_crp + np.random.normal(0, base_crp * 0.35)  # Further increased noise
                
                crp += individual_variation
            
            # Apply day-specific treatment effects
            if day in day_effects and day_effects[day] > 0:
                effect_size = day_effects[day]
                random_effect = np.random.normal(0, effect_size * 0.3)  # Some randomness in effect
                if is_treated:
                    crp -= effect_size + random_effect
                else:
                    crp += random_effect
            
            # Store the data point with randomized minimum CRP and round to 2 decimal places
            all_data.append({
                'patient_id': patient,
                'group': group,
                'day': day,
                'crp': round(max(get_min_crp(), crp), 2)  # Round to 2 decimal places
            })
    
    # Convert to DataFrame
    df = pd.DataFrame(all_data)
    return df
