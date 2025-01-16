# Ensure you have the required package installed:
# pip install statsmodels

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
import matplotlib.pyplot as plt
from statsmodels.regression.mixed_linear_model import MixedLM

def generate_patient_id():
    """Generate a random 8-digit ID starting with 64"""
    return int('64' + str(np.random.randint(000000, 1000000)).zfill(6))

def generate_crp_data(n_per_group=20, baseline_mean=5, baseline_sd=2, 
                     peak_treated=150, peak_control=180,
                     decay_treated=0.5, decay_control=0.3,
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
    random_seed : int
        Random seed for reproducibility
    
    Returns:
    --------
    pandas.DataFrame with columns:
        - patient_id: unique identifier for each patient
        - group: treatment group (treated/control)
        - day: day of measurement (0-7)
        - crp: CRP value
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
    for idx, patient in enumerate(patient_ids):  # Changed from range to enumerate
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
            
            # Adjust group differences
            if day >= 3:
                effect_size = 6  # Further reduced effect size
                random_effect = np.random.normal(0, 8)  # Increased random variation in effect
                if is_treated:
                    crp -= effect_size + random_effect
                else:
                    crp += effect_size + random_effect
            
            # Store the data point with randomized minimum CRP and round to 2 decimal places
            all_data.append({
                'patient_id': patient,  # Using the generated ID instead of index
                'group': group,
                'day': day,
                'crp': round(max(get_min_crp(), crp), 2)  # Round to 2 decimal places
            })
    
    # Convert to DataFrame
    df = pd.DataFrame(all_data)
    return df

def analyze_crp_data(df):
    """
    Analyze CRP data using a linear mixed model and t-tests at each time point
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with columns: patient_id, group, day, crp
    
    Returns:
    --------
    tuple: (mixed model results, t-test results DataFrame)
    """
    # Fit mixed linear model
    model = MixedLM.from_formula(
        "crp ~ group + day + group:day",
        groups="patient_id",
        data=df
    )
    mixed_model_results = model.fit()
    
    # Perform t-tests at each time point
    t_test_results = []
    for day in sorted(df['day'].unique()):
        day_data = df[df['day'] == day]
        treated = day_data[day_data['group'] == 'treated']['crp']
        control = day_data[day_data['group'] == 'control']['crp']
        
        t_stat, p_val = stats.ttest_ind(treated, control)
        t_test_results.append({
            'day': day,
            'p_value': p_val,
            'treated_mean': treated.mean(),
            'control_mean': control.mean()
        })
    
    return mixed_model_results, pd.DataFrame(t_test_results)

def plot_results(df, t_test_results):
    """
    Create a plot showing CRP trajectories for both groups, including SD as shaded area and p-values
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with columns: patient_id, group, day, crp
    t_test_results : pandas.DataFrame
        DataFrame with columns: day, p_value, treated_mean, control_mean
    """
    plt.figure(figsize=(10, 6))
    
    # Calculate means, standard errors, and standard deviations for each group at each time point
    summary = df.groupby(['day', 'group'])['crp'].agg(['mean', 'sem', 'std']).reset_index()
    
    # Plot each group
    for group in ['treated', 'control']:
        group_data = summary[summary['group'] == group]
        plt.errorbar(group_data['day'], group_data['mean'], 
                     yerr=group_data['sem'], 
                     label=f"{group.capitalize()} (Mean ± SEM)",
                     marker='o')
        
        # Plot SD as shaded area
        plt.fill_between(group_data['day'], 
                         group_data['mean'] - group_data['std'], 
                         group_data['mean'] + group_data['std'], 
                         alpha=0.2)
    
    # Annotate with p-values
    for _, row in t_test_results.iterrows():
        plt.annotate(f"p={row['p_value']:.3f}", (row['day'], max(row['treated_mean'], row['control_mean'])), textcoords="offset points", xytext=(0,-15), ha='center', color='red')
    
    plt.xlabel('Days after surgery')
    plt.ylabel('CRP (mg/L)')
    plt.title('CRP Levels Over Time by Treatment Group')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    return plt

def save_crp_data(df, filename="crp_data.csv"):
    """
    Save the CRP data to a CSV file
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with columns: patient_id, group, day, crp
    filename : str
        Name of the file to save the data to
    """
    # Round CRP values before saving
    df['crp'] = df['crp'].round(2)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def save_excel_format(df, filename="crp_data_wide.xlsx"):
    """
    Save the CRP data to an Excel file in wide format
    (one row per patient, columns for each day)
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with columns: patient_id, group, day, crp
    filename : str
        Name of the Excel file to save
    """
    # Round CRP values before pivoting
    df = df.copy()
    df['crp'] = df['crp'].round(2)
    
    # Reshape the data to wide format
    wide_df = df.pivot(index=['patient_id', 'group'], columns='day', values='crp').reset_index()
    
    # Rename the columns
    wide_df.columns = ['patient_id', 'group'] + [f'day_{i}' for i in range(8)]
    
    # Sort by group and patient_id
    wide_df = wide_df.sort_values(['group', 'patient_id'])
    
    # Save to Excel
    wide_df.to_excel(filename, index=False)
    print(f"Wide format data saved to {filename}")
    
    return wide_df

if __name__ == "__main__":
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Generate data
    df = generate_crp_data(n_per_group=20)
    
    # Save raw data
    save_crp_data(df, "crp_raw_data.csv")
    
    # Save Excel format
    save_excel_format(df, "crp_data_wide.xlsx")
    
    # Analyze and plot
    mixed_results, t_test_results = analyze_crp_data(df)
    
    # Print results
    print("\nMixed Model Results:")
    print(mixed_results.summary())
    
    print("\nT-test Results at Each Time Point:")
    print(t_test_results)
    
    # Create and show plot
    plot_results(df, t_test_results)
    plt.show()