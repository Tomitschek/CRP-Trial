import matplotlib.pyplot as plt
import argparse
import os
import sys

# Add the parent directory to sys.path to enable imports from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.generate import generate_crp_data, save_crp_data, save_excel_format
from src.analyse import load_data, analyze_data, analyze_crp_data, plot_results, render_to_markdown

def main():
    """
    Main function to execute CRP data generation, analysis, and visualization
    """
    # Get root path and output path
    root_dir = os.path.dirname(os.path.dirname(__file__))
    output_dir = os.path.join(root_dir, 'output')
    
    # Create output directory if it doesn't exist
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

    if args.generate:
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
    
    # Analyze data
    print("Analyzing data...")
    results = analyze_data(df)
    mixed_results, t_test_results = analyze_crp_data(df)
    
    # Print results
    print("\nLinear Mixed Model Results:")
    print(mixed_results.summary())
    
    print("\nT-test Results at Each Time Point:")
    print(t_test_results)
    
    # Render Markdown results
    render_to_markdown(results, args.output_md)
    print(f"Analysis results saved to {args.output_md}")
    
    # Create and show plot
    print("Generating plots...")
    plt_obj = plot_results(df, t_test_results)
    plt_obj.savefig(os.path.join(output_dir, 'crp_over_time_by_group.png'))
    print("Plots saved")
    
    print("Analysis complete!")

if __name__ == "__main__":
    main()
