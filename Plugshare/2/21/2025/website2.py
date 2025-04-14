import csv
import pandas as pd
import requests
import time
import sys

# -------------------------------------------------------------------
# Replace these with your own actual values from Google Cloud Console
API_KEY = "AIzaSyA6vpz88U95amjm0GAHyitEH0yqxFbKo8o"
SEARCH_ENGINE_ID = "d32fc18c6365a4276"
# -------------------------------------------------------------------

# Helper function to call Google Custom Search
def google_custom_search(query, api_key, cx, num_results=10, date_filter=False):
    """Perform a Google Custom Search and return up to num_results results."""
    # Each request can return up to 10 results in a single 'page'
    # If you need more than 10, you have to paginate.
    results = []
    
    # Construct the query parameters
    params = {
        'key': api_key,
        'cx': cx,
        'q': query,
        'num': min(num_results, 10)  # up to 10
    }
    
    # If you want to impose a date filter “April 2024 and beyond”,
    # Custom Search doesn't have a straightforward param for that.
    # You could try adding "April 2024" to the query as a text snippet or
    # advanced operators (not always reliable).
    # For demonstration, let's just do it in the calling code
    # by appending "April 2024" to the query. We'll omit date_filter logic here.
    
    try:
        response = requests.get("https://www.googleapis.com/customsearch/v1", params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract items from the response
        items = data.get("items", [])
        for item in items:
            link = item.get("link")
            if link:
                results.append(link)
        print(f"[DEBUG] Search Results: {results}")

    except requests.exceptions.RequestException as e:
        print(f"[DEBUG] Search Error: {e}")
    
    # Return up to num_results results
    return results[:num_results]

def main():
    input_csv = "testinput.csv"   # replace with your input CSV
    output_csv = "testtoutput.csv" # replace with your output CSV
    
    # Read input CSV
    print("[DEBUG] Reading input CSV...")
    df = pd.read_csv(input_csv)
    
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
    
    # Prepare new columns in dataframe copy
    df_copy = df.copy()
    df_copy["Search_Results"] = ""
    df_copy["Search_Results_April2024"] = ""
    
    num_rows = len(df_copy)
    
    # Go through each row
    for idx, row in df_copy.iterrows():
        base_query = " ".join(
            str(row[col]) for col in required_cols
        )
        
        print(f"[DEBUG] Row {idx+1}/{num_rows}: Searching for '{base_query}'")
        
        # 1) Regular search
        results_regular = google_custom_search(base_query, API_KEY, SEARCH_ENGINE_ID, num_results=10)
        df_copy.at[idx, "Search_Results"] = "|".join(results_regular)
        
        # 2) Filtered search (simply appending 'April 2024')
        filtered_query = base_query + " April 2024"
        print(f"[DEBUG] Row {idx+1}: Searching with filter 'April 2024' => '{filtered_query}'")
        
        results_filtered = google_custom_search(filtered_query, API_KEY, SEARCH_ENGINE_ID, num_results=10)
        df_copy.at[idx, "Search_Results_April2024"] = "|".join(results_filtered)
        
        # Rate-limit each iteration
        print("[DEBUG] Sleeping to reduce request rate...")
        time.sleep(2)  # adjust as needed
    
    # Write out to a new CSV file (doesn't overwrite original)
    print("[DEBUG] Writing output CSV...")
    df_copy.to_csv(output_csv, index=False)
    
    print(f"[DEBUG] Done. Output saved to '{output_csv}'.")

if __name__ == "__main__":
    main()
