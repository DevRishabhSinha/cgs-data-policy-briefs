import csv
import pandas as pd
import sys
from time import sleep

# If you're using the unofficial googlesearch package:
# pip install google
try:
    from googlesearch import search
except ImportError:
    sys.exit("Error: 'googlesearch' module not found. Install with 'pip install google' or 'pip install googlesearch-python'.")

def safe_google_search(query, num_results=10):
    """Return the top num_results links from Google for the given query."""
    links = []
    try:
        # 'tbs' or advanced operators for date filtering is not guaranteed to work with googlesearch
        # but you can experiment with parameters such as 'tbs=qdr:m' or append "after:2024-04-01" etc.
        # For demonstration, just call the search
        for url in search(query, num_results=num_results):
            links.append(url)
            if len(links) >= num_results:
                break
    except Exception as e:
        print(f"[DEBUG] Encountered an error while searching: {e}")
    return links

def main():
    input_csv = "testinput.csv"    # <--- Replace with your input CSV name
    output_csv = "testoutput.csv"  # <--- Replace with your desired output CSV name

    # Read data into a DataFrame
    print("[DEBUG] Reading input CSV...")
    df = pd.read_csv(input_csv)

    # Ensure columns exist
    required_cols = [
        "Name_source", 
        "Name_English", 
        "Name_Indo", 
        "Name_Other", 
        "Manager", 
        "Investor_1", 
        "Investor_2"
    ]
    for col in required_cols:
        if col not in df.columns:
            sys.exit(f"[ERROR] Missing required column '{col}' in input CSV.")

    # Prepare new columns
    df["Search_Results"] = ""
    df["Search_Results_April2024"] = ""

    # Process row by row
    for idx, row in df.iterrows():
        # Build the base query by concatenating the relevant columns
        base_query = " ".join([
            str(row["Name_source"]),
            str(row["Name_English"]),
            str(row["Name_Indo"]),
            str(row["Name_Other"]),
            str(row["Manager"]),
            str(row["Investor_1"]),
            str(row["Investor_2"])
        ])

        print(f"[DEBUG] Row {idx+1}/{len(df)}: Searching for '{base_query}'")

        # Regular search
        results = safe_google_search(base_query, num_results=10)
        df.at[idx, "Search_Results"] = "|".join(results)

        # Filtered search (append "April 2024" or advanced operator if available)
        # This can help refine the search results regarding the date/time window.
        filtered_query = base_query + " April 2024"
        print(f"[DEBUG] Row {idx+1}: Searching with filter 'April 2024' => '{filtered_query}'")
        results_filtered = safe_google_search(filtered_query, num_results=10)
        df.at[idx, "Search_Results_April2024"] = "|".join(results_filtered)

        # Throttle requests to avoid sending too many too quickly
        print("[DEBUG] Sleeping to reduce request rate...")
        sleep(2)  # Adjust delay as needed

    # Write the modified data to a new CSV (does not overwrite the original)
    print("[DEBUG] Writing output CSV...")
    df.to_csv(output_csv, index=False)

    print(f"[DEBUG] Done. Output saved to '{output_csv}'.")

if __name__ == "__main__":
    main()
