import pandas as pd

# Load your dataframe
df = pd.read_csv('extended_vin_data.csv')

# Create a copy of the original dataframe to ensure the original remains unchanged
filled_in_df = df.copy()

# Loop through each column in the dataframe
for column in filled_in_df.columns:

    # If column data type is numeric (int or float), fill NaN with mean of the column
    if filled_in_df[column].dtype in ['int64', 'float64']:
        filled_in_df[column].fillna(filled_in_df[column].mean(), inplace=True)

    # If column data type is object (likely string, indicating categorical data), fill NaN with mode of the column
    elif filled_in_df[column].dtype == 'object':
        filled_in_df[column].fillna(filled_in_df[column].mode()[0], inplace=True)

# Save the imputed dataframe if needed
filled_in_df.to_csv('filled_in_data.csv', index=False)

print("Data imputation completed and saved to 'filled_in_data.csv'.")
