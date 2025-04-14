import pandas as pd

def update_csv(file_path):
    # Read CSV with proper encoding and error handling
    df = pd.read_csv(file_path, dtype=str, encoding='utf-8', on_bad_lines='skip')
    
    # Identify the last two columns dynamically
    last_two_columns = df.columns[-2:]
    
    # Process each row, ensuring NaN values are handled
    for col in last_two_columns:
        df[col] = df[col].fillna('')  # Replace NaN with empty string
        df[col] = df[col].apply(lambda x: '\n'.join(x.split('|')) if x else '')
    
    # Save back to the same file
    df.to_csv(file_path, index=False, encoding='utf-8')
    print(f"Updated CSV saved at {file_path}")

# Example usage
update_csv('testtoutput.csv')
