import pandas as pd
import numpy as np

def fill_missing_smart(df):
    """
    Fills missing values by progressively checking:
      1. (Make, Manufacturer Name, Model, Model Year)
      2. (Make, Manufacturer Name, Model)
      3. (Make, Manufacturer Name)
      4. (Make)
      5. Global mean/mode fallback

    For numeric columns, we use the mean within each group.
    For categorical columns, we use the mode within each group.
    """

    # Define grouping levels in order of specificity
    group_levels = [
        ["Make", "Manufacturer Name", "Model", "Model Year"],
        ["Make", "Manufacturer Name", "Model"],
        ["Make", "Manufacturer Name"],
        ["Make"]
    ]

    # Separate numeric and non-numeric (categorical) columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns

    # Step 1 - 4: Fill missing values at each grouping level
    for level in group_levels:
        # For each numeric column, fill with mean of that group
        for col in numeric_cols:
            # Create a series of the mean by group
            group_mean = df.groupby(level)[col].transform('mean')
            # Fill only missing values in df[col] from the group mean
            df[col] = df[col].fillna(group_mean)

        # For each categorical column, fill with the mode of that group
        for col in categorical_cols:
            # The group mode might be ambiguous if multiple modes exist.
            # We'll just pick the first mode value if there's more than one.
            def get_mode(s):
                m = s.mode(dropna=True)
                return m[0] if not m.empty else np.nan

            group_mode = df.groupby(level)[col].transform(get_mode)
            df[col] = df[col].fillna(group_mode)

    # Step 5: Global fill for any remaining missing values
    # Numeric -> global mean
    for col in numeric_cols:
        mean_val = df[col].mean(skipna=True)
        df[col] = df[col].fillna(mean_val)

    # Categorical -> global mode
    for col in categorical_cols:
        m = df[col].mode(dropna=True)
        mode_val = m[0] if not m.empty else ""
        df[col] = df[col].fillna(mode_val)

    return df

def main():
    csv_path = "final_combined_output.csv"  # update with your CSV path
    df = pd.read_csv(csv_path)

    # Fill missing values with the multi-level fallback logic
    df_filled = fill_missing_smart(df)

    # Write out the filled DataFrame
    df_filled.to_csv("final_vehicles_filled.csv", index=False)

if __name__ == "__main__":
    main()

