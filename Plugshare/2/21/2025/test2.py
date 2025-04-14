import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_reviews(query):
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/115.0.0.0 Safari/537.36")
    }
    url = "https://www.google.com/search"
    params = {"q": query}
    try:
        print(f"DEBUG: Searching for query: {query}")
        resp = requests.get(url, params=params, headers=headers, timeout=5)
        print(f"DEBUG: Received response with status code: {resp.status_code}")
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        # Extract review texts from divs with class "b4vunb"
        review_divs = soup.find_all("div", class_="b4vunb")
        reviews = []
        for div in review_divs:
            a_tag = div.find("a", class_="a-no-hover-decoration")
            if a_tag:
                review_text = a_tag.get_text(strip=True)
                reviews.append(review_text)
                print(f"DEBUG: Found review: {review_text}")
        if not reviews:
            print("DEBUG: No reviews found for this query.")
        return " | ".join(reviews) if reviews else ""
    except Exception as e:
        print(f"ERROR: Failed to retrieve reviews for query '{query}'. Exception: {e}")
        return f"Error: {e}"

def main():
    try:
        print("DEBUG: Reading input.csv")
        df = pd.read_csv("input.csv")
        df_copy = df.copy()
        print("DEBUG: Successfully read input.csv")
    except Exception as e:
        print(f"ERROR: Failed to read input.csv. Exception: {e}")
        return

    # Process only the first 3 data rows (ignoring header)
    try:
        for idx, row in df_copy.head(3).iterrows():
            print(f"DEBUG: Processing row index {idx}")
            query_parts = []
            for col in ["LocationName", "Address", "City", "State", "Postcode", "Country"]:
                try:
                    if pd.notnull(row[col]):
                        query_parts.append(str(row[col]))
                except Exception as e:
                    print(f"WARNING: Error processing column '{col}' in row index {idx}. Exception: {e}")
            query = ", ".join(query_parts)
            print(f"DEBUG: Built query: {query}")
            
            reviews = get_reviews(query)
            print(f"DEBUG: Reviews retrieved: {reviews}")
            
            orig_comments = str(row.get("Comments", "")).strip()
            updated_comments = f"{orig_comments} | {reviews}" if orig_comments and orig_comments.lower() != "nan" else reviews
            df_copy.at[idx, "Comments"] = updated_comments
            print(f"DEBUG: Updated Comments for row index {idx}: {df_copy.at[idx, 'Comments']}")
    except Exception as e:
        print(f"ERROR: Exception during row processing. Exception: {e}")

    try:
        print("DEBUG: Printing updated first 3 rows:")
        print(df_copy.head(3))
    except Exception as e:
        print(f"ERROR: Failed to print updated rows. Exception: {e}")

    try:
        df_copy.head(3).to_csv("output.csv", index=False)
        print("DEBUG: Successfully saved output.csv")
    except Exception as e:
        print(f"ERROR: Failed to save output.csv. Exception: {e}")

if __name__ == "__main__":
    main()
