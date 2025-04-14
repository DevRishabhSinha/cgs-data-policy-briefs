import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def init_driver():
    """Initialize and return a WebDriver instance."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scrape_google_reviews(driver, query):
    """Scrape reviews for a given query using an existing WebDriver instance."""
    try:
        driver.get("https://www.google.com")
        search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
        search_box.send_keys(f"{query} reviews")
        search_box.send_keys(Keys.RETURN)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search")))

        review_divs = driver.find_elements(By.CSS_SELECTOR, "div.RfWLue")
        reviews = [div.text.strip() for div in review_divs if div.text.strip()]
        return reviews if reviews else ["No reviews found."]
    except Exception as e:
        print(f"[ERROR] Failed to scrape query '{query}': {e}")
        return ["Error occurred."]
    
def process_batch(batch):
    """Process a batch of queries using a single WebDriver instance."""
    driver = init_driver()
    results = []
    for row in batch:
        query = f"{row['LocationName']} {row['Address']} {row['City']} {row['State']} {row['Postcode']} {row['Country']}"
        reviews = scrape_google_reviews(driver, query)
        row["Reviews"] = "; ".join(reviews)
        results.append(row)
    driver.quit()
    return results

def process_csv(input_csv, output_csv, batch_size=100, max_workers=4):
    """Read input CSV, process in parallel batches, and write results to output CSV."""
    with open(input_csv, "r", encoding="utf-8") as infile, open(output_csv, "w", encoding="utf-8", newline="") as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ["Reviews"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        rows = list(reader)[:10]
        batches = [rows[i:i + batch_size] for i in range(0, len(rows), batch_size)]

        print(f"[INFO] Starting processing with {len(batches)} batches...")
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(process_batch, batch): batch for batch in batches}
            for future in as_completed(futures):
                try:
                    batch_results = future.result()
                    writer.writerows(batch_results)
                    print(f"[INFO] Processed batch of {len(batch_results)} rows.")
                except Exception as e:
                    print(f"[ERROR] Batch processing failed: {e}")

if __name__ == "__main__":
    input_csv = "input.csv"  # Input file containing address data
    output_csv = "output_reviews235.csv"  # Output file for results
    process_csv(input_csv, output_csv, batch_size=100, max_workers=4)