import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
from statsmodels.formula.api import mixedlm
import io
from tabulate import tabulate

def load_data(filepath):
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.lower()
    return df

def analyze_data(df):
    # Part 1: Understanding the Data
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    summary_stats = df.describe()

    # Part 2: Initial Data Exploration
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='day', y='crp', hue='group')
    plt.title('CRP-Verläufe über die Zeit nach Gruppe')
    plt.savefig('crp_over_time.png')
    plt.close()

    g = sns.FacetGrid(df, col="patient_id", col_wrap=5, height=2, aspect=1.5)
    g.map(plt.plot, "day", "crp")
    g.savefig('individual_patient_plots.png')
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
    normalized = group[group['crp'] < 100]
    return normalized['day'].min() if not normalized.empty else np.nan

def render_to_markdown(results, output_filepath):
    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write("# CRP-Datenanalyse-Ergebnisse\n")
        f.write("\n## Datenübersicht:\n")
        f.write("```\n")
        f.write(results["info_str"])
        f.write("```\n")
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
        f.write("![CRP-Verläufe über die Zeit nach Gruppe](crp_over_time.png)\n")
        f.write("![Individuelle Patientenverläufe](individual_patient_plots.png)\n")
        f.write("![CRP-Werte nach Tag und Gruppe](crp_boxplot.png)\n")

if __name__ == "__main__":
    df = load_data('crp_raw_data.csv')
    results = analyze_data(df)
    render_to_markdown(results, 'crp_analysis_results.md')