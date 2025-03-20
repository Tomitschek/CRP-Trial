"""
Input/Output utilities for CRP data
"""
import os
import pandas as pd

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

def save_crp_data(df, filename):
    """
    Save the CRP data to a CSV file
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with columns: patient_id, group, day, crp
    filename : str
        Name of the file to save the data to
    """
    # Make sure directory exists
    os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
    
    # Round CRP values before saving
    df['crp'] = df['crp'].round(2)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def save_excel_format(df, filename):
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
    # Make sure directory exists
    os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
    
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
    try:
        wide_df.to_excel(filename, index=False)
        print(f"Wide format data saved to {filename}")
    except ImportError:
        csv_filename = filename.replace('.xlsx', '.csv')
        print(f"Warning: openpyxl not installed. Cannot save Excel file.")
        print(f"Saving as CSV instead: {csv_filename}")
        wide_df.to_csv(csv_filename, index=False)
    
    return wide_df
