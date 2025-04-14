import csv
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm

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

def process_row(row):
    """Process a single row to scrape reviews."""
    driver = init_driver()
    try:
        query = f"{row['LocationName']} {row['Address']} {row['City']} {row['State']} {row['Postcode']} {row['Country']}"
        reviews = scrape_google_reviews(driver, query)
        reviews_text = "; ".join(reviews)

        # Append reviews to the 'Comments' column
        if 'Comments' in row and row['Comments'].strip():
            row['Comments'] += f" | Reviews: {reviews_text}"
        else:
            row['Comments'] = f"Reviews: {reviews_text}"
        return row
    finally:
        driver.quit()

def process_csv(input_csv, output_csv, batch_size=100, max_workers=4):
    """Read input CSV, process rows, and write to the output CSV with progress tracking."""
    if not os.path.exists(output_csv):
        # Write header if output file doesn't exist
        with open(input_csv, "r", encoding="utf-8") as infile, open(output_csv, "w", encoding="utf-8", newline="") as outfile:
            reader = csv.DictReader(infile)
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            writer.writeheader()

    with open(input_csv, "r", encoding="utf-8") as infile, open(output_csv, "a", encoding="utf-8", newline="") as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)

        # Skip already processed rows
        existing_rows = {tuple(row.values()) for row in csv.DictReader(open(output_csv, "r", encoding="utf-8"))}
        rows = [row for row in reader if tuple(row.values()) not in existing_rows][:10]
        total_rows = len(rows)

        print(f"[INFO] Found {total_rows} rows to process.")
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            with tqdm(total=total_rows, desc="Processing rows") as progress_bar:
                futures = {executor.submit(process_row, row): row for row in rows}
                for future in as_completed(futures):
                    try:
                        processed_row = future.result()
                        writer.writerow(processed_row)
                        progress_bar.update(1)
                    except Exception as e:
                        print(f"[ERROR] Failed to process a row: {e}")

if __name__ == "__main__":
    input_csv = "input.csv"  # Input file containing address data
    output_csv = "output_reviews225.csv"  # Output file for results
    process_csv(input_csv, output_csv, batch_size=5, max_workers=20)
