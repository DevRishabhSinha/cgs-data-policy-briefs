import pandas as pd

def combine_csvs(csv_files, output_file):
    """
    Combines multiple CSV files in the specified order, keeping only the header from the first file.
    
    Parameters:
    csv_files (list): List of CSV file paths in the desired order
    output_file (str): Path for the output combined CSV
    """
    
    # Read the first CSV with headers
    combined_df = pd.read_csv(csv_files[0])
    
    # Read and append each subsequent CSV, skipping their headers
    for file in csv_files[1:]:
        df = pd.read_csv(file, header=0)  # header=0 reads the header but doesn't use it
        combined_df = pd.concat([combined_df, df], ignore_index=True)
    
    # Write the combined dataframe to a new CSV
    combined_df.to_csv(output_file, index=False)

# Example usage
csv_files = [
    'combined_output.csv',    # This will be the top file with headers kept
    'missing_stragglers20250130_233105.csv',
]

output_file = 'final_combined_output.csv'
combine_csvs(csv_files, output_file)