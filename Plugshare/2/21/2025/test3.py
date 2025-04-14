import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def get_reviews_selenium(query):
    # Setup headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"ERROR: Failed to initialize Chrome WebDriver. Exception: {e}")
        return ""
    
    # Build the search URL
    url = "https://www.google.com/search?q=" + query.replace(" ", "+")
    try:
        print(f"DEBUG: Selenium navigating to {url}")
        driver.get(url)
        # Wait a few seconds for dynamic content to load
        time.sleep(3)
        
        # Attempt to locate review divs by their class name "b4vunb"
        review_elements = driver.find_elements(By.CSS_SELECTOR, "div.b4vunb")
        reviews = []
        for element in review_elements:
            try:
                a_tag = element.find_element(By.CSS_SELECTOR, "a.a-no-hover-decoration")
                review_text = a_tag.text.strip()
                if review_text:
                    reviews.append(review_text)
                    print(f"DEBUG: Selenium found review: {review_text}")
            except Exception as inner_e:
                print(f"WARNING: Selenium could not extract review text from an element. Exception: {inner_e}")
        if not reviews:
            print("DEBUG: Selenium found no reviews for query.")
        return " | ".join(reviews)
    except Exception as e:
        print(f"ERROR: Selenium failed to retrieve reviews for query '{query}'. Exception: {e}")
        return ""
    finally:
        driver.quit()

def main():
    try:
        print("DEBUG: Reading input.csv")
        df = pd.read_csv("input.csv")
        df_copy = df.copy()
        print("DEBUG: Successfully read input.csv")
    except Exception as e:
        print(f"ERROR: Failed to read input.csv. Exception: {e}")
        return

    # Process only the first 3 data rows (ignoring header row)
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
        
        reviews = get_reviews_selenium(query)
        print(f"DEBUG: Reviews retrieved via Selenium: {reviews}")
        
        orig_comments = str(row.get("Comments", "")).strip()
        updated_comments = f"{orig_comments} | {reviews}" if orig_comments and orig_comments.lower() != "nan" else reviews
        df_copy.at[idx, "Comments"] = updated_comments
        print(f"DEBUG: Updated Comments for row index {idx}: {df_copy.at[idx, 'Comments']}")

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
