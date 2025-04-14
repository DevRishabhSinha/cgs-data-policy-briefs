import pandas as pd

# Assuming the files are named and stored correctly, adjust the paths if necessary
file_paths = [
    'data/scraped_info (10).csv',
    'data/scraped_info (12).csv',
    'data/scraped_info (13).csv',
    'data/scraped_info (14).csv',
    'data/scraped_info (15).csv'
]

# Use a list comprehension to read each CSV file and store them in a list
dataframes = [pd.read_csv(file) for file in file_paths]

# Concatenate all dataframes into one, putting one below the other
combined_df = pd.concat(dataframes)

# Save the combined dataframe to a new CSV file
combined_df.to_csv('data/combined_scraped_info.csv', index=False)
