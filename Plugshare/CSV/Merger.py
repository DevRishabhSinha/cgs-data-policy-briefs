import pandas as pd

# Function to load a CSV file with flexible error handling
def load_csv(file_name):
    try:
        # Try reading the CSV with expected column handling
        df = pd.read_csv(file_name, on_bad_lines='skip')
    except pd.errors.ParserError as e:
        # In case of a parser error, try a more flexible approach
        print(f"Error reading {file_name}: {e}")
        df = pd.read_csv(file_name, on_bad_lines='warn', engine='python')
    return df

# Load the CSV files with error handling
df1 = load_csv('revised_scraped_dat.csv')
df2 = load_csv('output.csv')

# Combine the dataframes, removing duplicates
combined_df = pd.concat([df1, df2]).drop_duplicates()

# Save the combined dataframe to a new CSV file
combined_df.to_csv('combined.csv', index=False)
