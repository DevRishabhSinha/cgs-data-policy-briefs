import pandas as pd

# List of files in order
file_list = [
    "output_reviews2567final.csv",
    "output_reviews25678final.csv",
    "output_reviews256789final.csv",
    "output_reviews2567890final.csv",
    "output_reviews25678901final.csv",
    "output_reviews256789012final.csv",
    "output_reviews2567890123final.csv",
    "output_reviews25678901234final.csv",
    "output_reviews256789012345final.csv",
    "output_reviews2567890123456final.csv",
    "output_reviews25678901234567final.csv"
]

# Read the first file with headers
combined_df = pd.read_csv(file_list[0])

# Read the rest without headers and append
for file in file_list[1:]:
    temp_df = pd.read_csv(file, skiprows=1)  # Skip the first row (headers)
    combined_df = pd.concat([combined_df, temp_df], ignore_index=True)

# Save to a new file
combined_df.to_csv("combined_output_reviews.csv", index=False)

print("Concatenation complete! Saved as 'combined_output_reviews.csv'")
