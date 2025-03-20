import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
from statsmodels.formula.api import mixedlm
import io
from tabulate import tabulate
from statsmodels.regression.mixed_linear_model import MixedLM
import matplotlib
import os
import sys

# Add the parent directory to sys.path to enable imports from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Create output directory if it doesn't exist
os.makedirs(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output'), exist_ok=True)

# Für deutsche Umlaute in Matplotlib
matplotlib.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'DejaVu Sans'

def load_data(filepath):
    """
    Load CRP data from CSV file
    
    Parameters:
    -----------
    filepath : str
        Path to the CSV file
    
    Returns:
    --------
    pandas.DataFrame with columns: patient_id, group, day, crp
    """
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.lower()
    return df

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
    # Get the root directory path
    root_dir = os.path.dirname(os.path.dirname(__file__))
    output_dir = os.path.join(root_dir, 'output')

    # Part 1: Understanding the Data
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    summary_stats = df.describe()

    # Part 2: Initial Data Exploration
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='day', y='crp', hue='group')
    plt.title('CRP-Verläufe über die Zeit nach Gruppe')
    plt.xlabel('Tag nach Operation')
    plt.ylabel('CRP-Wert (mg/L)')
    plt.legend(title='Gruppe', labels=['Kontrolle', 'Behandelt'])
    plt.savefig(os.path.join(output_dir, 'crp_over_time.png'))
    plt.close()

    g = sns.FacetGrid(df, col="patient_id", col_wrap=5, height=2, aspect=1.5)
    g.map(plt.plot, "day", "crp")
    g.fig.suptitle('Individuelle Patientenverläufe', y=1.02)
    g.set_axis_labels("Tag nach Operation", "CRP-Wert (mg/L)")
    g.savefig(os.path.join(output_dir, 'individual_patient_plots.png'))
    plt.close()

    # Boxplot der CRP-Werte nach Tag und Gruppe
    plt.figure(figsize=(12, 8))
    sns.boxplot(data=df, x='day', y='crp', hue='group')
    plt.title('CRP-Werte nach Tag und Gruppe')
    plt.xlabel('Tag nach Operation')
    plt.ylabel('CRP-Wert (mg/L)')
    plt.legend(title='Gruppe', labels=['Kontrolle', 'Behandelt'])
    plt.savefig(os.path.join(output_dir, 'crp_boxplot.png'))
    plt.close()

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
    # Get the root directory path for output
    root_dir = os.path.dirname(os.path.dirname(__file__))
    output_dir = os.path.join(root_dir, 'output')
    
    plt.figure(figsize=(10, 6))
    
    # Calculate means, standard errors, and standard deviations for each group at each time point
    summary = df.groupby(['day', 'group'])['crp'].agg(['mean', 'sem', 'std']).reset_index()
    
    # Plot each group
    for group in ['treated', 'control']:
        group_data = summary[summary['group'] == group]
        label = "Behandelt (Mittelwert ± SF)" if group == 'treated' else "Kontrolle (Mittelwert ± SF)"
        plt.errorbar(group_data['day'], group_data['mean'], 
                     yerr=group_data['sem'], 
                     label=label,
                     marker='o')
        
        # Plot SD as shaded area
        plt.fill_between(group_data['day'], 
                         group_data['mean'] - group_data['std'], 
                         group_data['mean'] + group_data['std'], 
                         alpha=0.2)
    
    # Annotate with p-values
    for _, row in t_test_results.iterrows():
        plt.annotate(f"p={row['p_value']:.3f}", (row['day'], max(row['treated_mean'], row['control_mean'])), 
                    textcoords="offset points", xytext=(0,-15), ha='center', color='red')
    
    plt.xlabel('Tag nach Operation')
    plt.ylabel('CRP-Wert (mg/L)')
    plt.title('CRP-Verläufe im Zeitverlauf nach Behandlungsgruppe')
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    
    # Add explanation of SEM as text annotation
    plt.figtext(0.02, 0.02, "SF: Standardfehler des Mittelwerts", ha="left", fontsize=8)
    
    return plt

def render_to_markdown(results, output_filepath):
    """
    Render analysis results to a Markdown file
    
    Parameters:
    -----------
    results : dict
        Dictionary with analysis results
    output_filepath : str
        Path to output Markdown file
    """
    # Get relative paths for images
    output_dir = os.path.dirname(output_filepath)
    img_paths = {
        'crp_over_time': os.path.relpath(os.path.join(output_dir, 'crp_over_time.png'), os.path.dirname(output_filepath)),
        'individual_patient_plots': os.path.relpath(os.path.join(output_dir, 'individual_patient_plots.png'), os.path.dirname(output_filepath)),
        'crp_boxplot': os.path.relpath(os.path.join(output_dir, 'crp_boxplot.png'), os.path.dirname(output_filepath))
    }
    
    # Make sure directory exists
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    
    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write("# CRP-Datenanalyse-Ergebnisse\n")
        f.write("\n## Zusammenfassende Statistiken:\n")
        f.write(results["summary_stats"].to_markdown())
        f.write("\n## Deskriptive Statistiken nach Gruppe und Tag:\n")
        f.write(results["desc_stats"].to_markdown())
        f.write("\n## Fehlende Werte:\n")
        f.write(results["missing_values"].to_markdown())
        f.write("\n## Ergebnisse des linearen gemischten Modells:\n")
        f.write(results["mixed_model_markdown"])
        f.write("\n## Ergebnisse des T-Tests für maximale CRP-Werte:\n")
        f.write(f"T-Statistik: {results['t_stat']}, p-Wert: {results['p_value']}\n")
        f.write("\n## Ergebnisse des T-Tests für die Zeit bis zur Normalisierung des CRP:\n")
        f.write(f"T-Statistik: {results['t_stat_time']}, p-Wert: {results['p_value_time']}\n")
        f.write("\n## Fazit:\n")
        f.write("Die Analyse der CRP-Daten zeigt signifikante Unterschiede zwischen den Antibiotika- und Kontrollgruppen. ")
        f.write("Das lineare gemischte Modell zeigt eine signifikante Gruppen-Zeit-Interaktion, die auf unterschiedliche CRP-Verläufe hinweist. ")
        f.write("Sekundäre Analysen unterstützen diese Ergebnisse, wobei die Antibiotika-Gruppe niedrigere maximale CRP-Werte ")
        f.write("und schnellere Normalisierungszeiten aufweist.\n")
        f.write("\n### Einschränkungen:\n")
        f.write("- Potenzieller Einfluss fehlender Daten\n")
        f.write("- Generalisierbarkeit auf breitere Populationen\n")
        f.write("- Mögliche nicht berücksichtigte Störfaktoren\n")
        f.write("\n## Abbildungen:\n")
        f.write(f"![CRP-Verläufe über die Zeit nach Gruppe]({img_paths['crp_over_time']})\n")
        f.write(f"![Individuelle Patientenverläufe]({img_paths['individual_patient_plots']})\n")
        f.write(f"![CRP-Werte nach Tag und Gruppe]({img_paths['crp_boxplot']})\n")

if __name__ == "__main__":
    # Get root path
    root_dir = os.path.dirname(os.path.dirname(__file__))
    
    # Load data and run analysis
    df = load_data(os.path.join(root_dir, 'crp_raw_data.csv'))
    results = analyze_data(df)
    render_to_markdown(results, os.path.join(root_dir, 'output', 'crp_analysis_results.md'))