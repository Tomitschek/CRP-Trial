"""
Statistical analysis functions for CRP data
"""
import numpy as np
import pandas as pd
import io
from scipy import stats
from statsmodels.formula.api import mixedlm
from tabulate import tabulate
from statsmodels.regression.mixed_linear_model import MixedLM

def time_to_normalize(group):
    """
    Calculate the time (day) when CRP first falls below 100
    
    Parameters:
    -----------
    group : pandas.DataFrame
        DataFrame for a single patient
        
    Returns:
    --------
    float or np.nan: Day when CRP < 100, or nan if never normalized
    """
    normalized = group[group['crp'] < 100]
    return normalized['day'].min() if not normalized.empty else np.nan

def analyze_data(df):
    """
    Analyze CRP data and produce descriptive statistics and model results
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with columns: patient_id, group, day, crp
        
    Returns:
    --------
    dict with analysis results
    """
    # Part 1: Understanding the Data
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    summary_stats = df.describe()

    # Create descriptive statistics
    desc_stats = df.groupby(['group', 'day'], observed=True)['crp'].agg(['mean', 'median', 'std', 'count'])
    missing_values = df.isnull().sum()

    # Part 3: Statistical Analysis
    df['group'] = pd.Categorical(df['group'])
    df['patient_id'] = pd.Categorical(df['patient_id'])

    model = mixedlm("crp ~ group + day", data=df, groups="patient_id")
    results = model.fit(method='nm')  # Use Nelder-Mead optimizer

    mixed_model_summary = results.summary().tables[1]
    mixed_model_df = pd.read_html(io.StringIO(mixed_model_summary.to_html()), header=0, index_col=0)[0]
    mixed_model_df.columns = mixed_model_df.columns.str.replace(r'P>|z|', r'P>\|z\|')
    mixed_model_markdown = tabulate(mixed_model_df, headers='keys', tablefmt='pipe')

    max_crp = df.groupby(['group', 'patient_id'], observed=True)['crp'].max().reset_index()
    t_stat, p_value = stats.ttest_ind(max_crp[max_crp['group'] == 'treated']['crp'], 
                                      max_crp[max_crp['group'] == 'control']['crp'])

    time_to_normal = df.groupby(['group', 'patient_id'], observed=True).apply(lambda x: time_to_normalize(x), include_groups=False).reset_index()
    time_to_normal.columns = ['group', 'patient_id', 'days_to_normalize']

    treated_times = time_to_normal[time_to_normal['group'] == 'treated']['days_to_normalize'].dropna()
    control_times = time_to_normal[time_to_normal['group'] == 'control']['days_to_normalize'].dropna()

    if len(treated_times) > 1 and len(control_times) > 1:
        t_stat_time, p_value_time = stats.ttest_ind(treated_times, control_times)
    else:
        t_stat_time, p_value_time = np.nan, np.nan

    return {
        "info_str": info_str,
        "summary_stats": summary_stats,
        "desc_stats": desc_stats,
        "missing_values": missing_values,
        "mixed_model_markdown": mixed_model_markdown,
        "t_stat": t_stat,
        "p_value": p_value,
        "t_stat_time": t_stat_time,
        "p_value_time": p_value_time
    }

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
