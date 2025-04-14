import csv
import logging
import random
import time
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging to output to both file and console
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper_debug.log'),
        logging.StreamHandler()
    ]
)

def init_driver():
    try:
        options = Options()
        options.add_argument('--headless')  # Run headless
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        # Override the user agent
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/115.0.0.0 Safari/537.36")
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        logging.info("WebDriver initialized successfully")
        return driver
    except Exception as e:
        logging.error(f"Failed to initialize WebDriver: {e}")
        logging.error(traceback.format_exc())
        raise

def scrape_google_reviews(driver, query):
    try:
        logging.info(f"Starting scrape for query: {query}")
        # Introduce a random delay to mimic human behavior
        time.sleep(random.uniform(2, 4))
        
        search_url = f"https://www.google.com/search?q={query}"
        driver.get(search_url)
        logging.debug(f"Navigated to search URL: {search_url}")
        # Wait additional time for the page to load dynamic content
        time.sleep(random.uniform(5, 7))
        
        # Use several CSS selectors to locate review elements
        review_selectors = [
            "div.RfWLue div.b4vunb a",
            "div.review-snippet",
            "div[data-review-id]",
            "span[jscontroller='fIQYlf']"
        ]
        
        reviews = []
        for selector in review_selectors:
            try:
                elements = WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                )
                if elements:
                    reviews = [e.text.strip() for e in elements if e.text.strip()]
                    logging.info(f"Found {len(reviews)} reviews using selector: {selector}")
                    if reviews:
                        break
            except Exception as e:
                logging.debug(f"Selector {selector} failed: {e}")
                continue
        
        if not reviews:
            logging.info("No reviews found for this query")
            reviews = ["No reviews found"]
        
        return "; ".join(reviews)
    except Exception as e:
        logging.error(f"Error scraping reviews for query '{query}': {e}")
        logging.error(traceback.format_exc())
        return "Error occurred"

def process_rows(input_csv, output_csv):
    try:
        with open(input_csv, "r", encoding="utf-8") as infile:
            reader = csv.DictReader(infile)
            rows = list(reader)
            logging.info(f"Read {len(rows)} rows from {input_csv}")
    except Exception as e:
        logging.error(f"Failed to read {input_csv}: {e}")
        logging.error(traceback.format_exc())
        return
    
    # Process only the first 3 data rows (proof of concept)
    rows_to_process = rows[:3]
    
    try:
        driver = init_driver()
    except Exception as e:
        logging.error("Cannot proceed without WebDriver")
        return
    
    for row in rows_to_process:
        # Build query by concatenating the specified columns
        query_parts = []
        for col in ["LocationName", "Address", "City", "State", "Postcode", "Country"]:
            value = row.get(col, "").strip()
            if value:
                query_parts.append(value)
        query = ", ".join(query_parts)
        logging.info(f"Processing StationID {row.get('StationID')} with query: {query}")
        
        reviews = scrape_google_reviews(driver, query)
        logging.info(f"Reviews retrieved: {reviews}")
        
        existing_comments = row.get("Comments", "").strip()
        if existing_comments:
            row["Comments"] = f"{existing_comments}; {reviews}"
        else:
            row["Comments"] = reviews
        
        logging.info(f"Updated Comments for StationID {row.get('StationID')}: {row['Comments']}")
    
    driver.quit()
    logging.info("WebDriver closed")
    
    # Write the processed rows to output CSV (only the first 3 rows)
    fieldnames = rows[0].keys()
    try:
        with open(output_csv, "w", encoding="utf-8", newline="") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows_to_process)
        logging.info(f"Successfully saved output to {output_csv}")
    except Exception as e:
        logging.error(f"Failed to save output CSV: {e}")
        logging.error(traceback.format_exc())

if __name__ == "__main__":
    input_csv = "input.csv"  # Ensure this CSV is in the same directory with the proper header
    output_csv = "output.csv"
    process_rows(input_csv, output_csv)
