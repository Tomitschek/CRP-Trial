"""
Plotting functions for CRP data visualization
"""
import os
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# Für deutsche Umlaute in Matplotlib
matplotlib.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'DejaVu Sans'

def create_exploratory_plots(df, output_dir):
    """
    Create exploratory plots of CRP data
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with columns: patient_id, group, day, crp
    output_dir : str
        Directory to save plots
        
    Returns:
    --------
    dict with paths to the created plots
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Overview line plot
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='day', y='crp', hue='group')
    plt.title('CRP-Verläufe über die Zeit nach Gruppe')
    plt.xlabel('Tag nach Operation')
    plt.ylabel('CRP-Wert (mg/L)')
    plt.legend(title='Gruppe', labels=['Kontrolle', 'Behandelt'])
    overview_path = os.path.join(output_dir, 'crp_over_time.png')
    plt.savefig(overview_path)
    plt.close()

    # Individual patient plots
    g = sns.FacetGrid(df, col="patient_id", col_wrap=5, height=2, aspect=1.5)
    g.map(plt.plot, "day", "crp")
    g.fig.suptitle('Individuelle Patientenverläufe', y=1.02)
    g.set_axis_labels("Tag nach Operation", "CRP-Wert (mg/L)")
    individual_path = os.path.join(output_dir, 'individual_patient_plots.png')
    g.savefig(individual_path)
    plt.close()

    # Boxplot of CRP values by day and group
    plt.figure(figsize=(12, 8))
    sns.boxplot(data=df, x='day', y='crp', hue='group')
    plt.title('CRP-Werte nach Tag und Gruppe')
    plt.xlabel('Tag nach Operation')
    plt.ylabel('CRP-Wert (mg/L)')
    plt.legend(title='Gruppe', labels=['Kontrolle', 'Behandelt'])
    boxplot_path = os.path.join(output_dir, 'crp_boxplot.png')
    plt.savefig(boxplot_path)
    plt.close()
    
    return {
        'overview': overview_path,
        'individual': individual_path,
        'boxplot': boxplot_path
    }

def plot_results(df, t_test_results, output_dir):
    """
    Create a plot showing CRP trajectories for both groups, including SD as shaded area and p-values
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with columns: patient_id, group, day, crp
    t_test_results : pandas.DataFrame
        DataFrame with columns: day, p_value, treated_mean, control_mean
    output_dir : str
        Directory to save plot
        
    Returns:
    --------
    str: Path to the created plot
    """
    os.makedirs(output_dir, exist_ok=True)
    
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
    
    results_path = os.path.join(output_dir, 'crp_over_time_by_group.png')
    plt.savefig(results_path)
    plt.close()
    
    return results_path
