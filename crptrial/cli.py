"""
Command-line interface for CRP-Trial
"""
import os
import argparse

from crptrial.generate import generate_crp_data
from crptrial.utils.io import load_data, save_crp_data, save_excel_format
from crptrial.analysis.stats import analyze_data, analyze_crp_data
from crptrial.analysis.plotting import create_exploratory_plots, plot_results
from crptrial.analysis.reporting import render_to_markdown

def main():
    """
    Main function to execute CRP data generation, analysis, and visualization
    """
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.getcwd(), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    parser = argparse.ArgumentParser(description='CRP Data Analysis Tool')
    parser.add_argument('--generate', action='store_true', help='Generate new synthetic CRP data')
    parser.add_argument('--day-effects', type=str, default="{5: 50}", 
                        help='Dictionary of day effects (e.g., "{5: 50}" for large effect on day 5)')
    parser.add_argument('--input-file', default=os.path.join(output_dir, 'crp_raw_data.csv'), 
                        help='Input CSV file with CRP data')
    parser.add_argument('--output-md', default=os.path.join(output_dir, 'crp_analysis_results.md'), 
                        help='Output Markdown file')
    parser.add_argument('--output-excel', default=os.path.join(output_dir, 'crp_data_wide.xlsx'), 
                        help='Output Excel file for wide format')
    args = parser.parse_args()

    # Check if input file exists and generate data if needed
    if args.generate or not os.path.exists(args.input_file):
        if not args.generate:
            print(f"Input file '{args.input_file}' not found. Generating sample data...")
        
        try:
            # Parse day_effects from string to dictionary
            day_effects = eval(args.day_effects)
            if not isinstance(day_effects, dict):
                raise ValueError("day_effects must be a dictionary")
                
            print(f"Generating CRP data with day effects: {day_effects}")
            df = generate_crp_data(day_effects=day_effects)
            save_crp_data(df, args.input_file)
            save_excel_format(df, args.output_excel)
        except Exception as e:
            print(f"Error generating data: {e}")
            return

    # Load data (either generated or existing)
    df = load_data(args.input_file)
    print(f"Loaded CRP data from {args.input_file}")
    
    # Create exploratory plots
    print("Creating exploratory plots...")
    plot_paths = create_exploratory_plots(df, output_dir)
    
    # Analyze data
    print("Analyzing data...")
    results = analyze_data(df)
    mixed_results, t_test_results = analyze_crp_data(df)
    
    # Print results
    print("\nLinear Mixed Model Results:")
    print(mixed_results.summary())
    
    print("\nT-test Results at Each Time Point:")
    print(t_test_results)
    
    # Create results plot
    print("Creating results plot...")
    results_plot_path = plot_results(df, t_test_results, output_dir)
    
    # Render Markdown results
    render_to_markdown(results, args.output_md)
    print(f"Analysis results saved to {args.output_md}")
    
    print("Analysis complete!")

if __name__ == "__main__":
    main()
