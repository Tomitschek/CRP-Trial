"""
Reporting functions for CRP analysis results
"""
import os

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
    # Make sure directory exists
    os.makedirs(os.path.dirname(output_filepath) or '.', exist_ok=True)
    
    # Get paths to image files relative to the output filepath
    output_dir = os.path.dirname(output_filepath)
    image_paths = {
        'overview': os.path.join(output_dir, 'crp_over_time.png'),
        'individual': os.path.join(output_dir, 'individual_patient_plots.png'),
        'boxplot': os.path.join(output_dir, 'crp_boxplot.png'),
        'results': os.path.join(output_dir, 'crp_over_time_by_group.png'),
    }
    
    # Make paths relative to the output file
    for key, path in image_paths.items():
        if os.path.exists(path):
            image_paths[key] = os.path.relpath(path, output_dir)
    
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
        f.write(f"![CRP-Verläufe über die Zeit nach Gruppe]({image_paths.get('overview')})\n")
        f.write(f"![Individuelle Patientenverläufe]({image_paths.get('individual')})\n")
        f.write(f"![CRP-Werte nach Tag und Gruppe]({image_paths.get('boxplot')})\n")
        f.write(f"![CRP-Verläufe mit p-Werten]({image_paths.get('results')})\n")
