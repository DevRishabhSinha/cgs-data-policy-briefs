import csv
import traceback
import logging
import random
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm

# Configuration
BATCH_SIZE = 10
MAX_WORKERS = 10
MIN_DELAY = 2
MAX_DELAY = 4

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
       options.add_argument('--headless=new')
       options.add_argument('--no-sandbox')
       options.add_argument('--disable-dev-shm-usage')
       options.add_argument('--disable-blink-features=AutomationControlled')
       options.add_experimental_option("excludeSwitches", ["enable-automation"])
       options.add_experimental_option('useAutomationExtension', False)
       
       driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
       driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
       logging.info("WebDriver initialized successfully")
       return driver
   except Exception as e:
       logging.error(f"Failed to initialize WebDriver: {str(e)}")
       logging.error(f"Traceback: {traceback.format_exc()}")
       raise

def scrape_google_reviews(driver, query):
   try:
       logging.info(f"Starting scrape for: {query}")
       time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
       
       search_url = f"https://www.google.com/search?q={query}"
       driver.get(search_url)
       logging.debug(f"Navigated to search URL: {search_url}")
       
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
                   logging.info(f"Found {len(reviews)} reviews with {selector}")
                   break
           except Exception as e:
               logging.debug(f"Selector {selector} failed: {str(e)}")
               continue
               
       return "; ".join(reviews) if reviews else "No reviews found"
           
   except Exception as e:
       logging.error(f"Error scraping: {str(e)}")
       logging.error(f"Traceback: {traceback.format_exc()}")
       return "Error occurred"

def process_batch(batch):
   driver = None
   results = []
   try:
       driver = init_driver()
       for row in batch:
           query = f"{row['LocationName']} {row['Address']} {row['City']} {row['State']} {row['Postcode']}"
           logging.info(f"Processing query: {query}")
           
           reviews = scrape_google_reviews(driver, query)
           
           existing_comments = row.get('Comments', '')
           if existing_comments:
               row['Comments'] = f"{existing_comments}; {reviews}"
           else:
               row['Comments'] = reviews
               
           results.append(row)
           
   except Exception as e:
       logging.error(f"Batch processing error: {str(e)}")
       logging.error(f"Traceback: {traceback.format_exc()}")
   finally:
       if driver:
           driver.quit()
           logging.info("WebDriver closed")
   return results

def process_csv(input_csv, output_csv, batch_size=BATCH_SIZE, max_workers=MAX_WORKERS):
   try:
       with open(input_csv, "r", encoding="utf-8") as infile:
           reader = csv.DictReader(infile)
           rows = list(reader)
           fieldnames = reader.fieldnames
           logging.info(f"Read {len(rows)} rows from input CSV")

       if not os.path.exists(output_csv):
           with open(output_csv, "w", encoding="utf-8", newline="") as outfile:
               writer = csv.DictWriter(outfile, fieldnames=fieldnames)
               writer.writeheader()

       processed_ids = set()
       if os.path.exists(output_csv):
           with open(output_csv, "r", encoding="utf-8") as outfile:
               reader = csv.DictReader(outfile)
               for row in reader:
                   processed_ids.add(row['StationID'])

       rows = [row for row in rows if row['StationID'] not in processed_ids]
       batches = [rows[i:i + batch_size] for i in range(0, len(rows), batch_size)]
       
       logging.info(f"Processing {len(rows)} remaining rows in {len(batches)} batches")
       
       with ThreadPoolExecutor(max_workers=max_workers) as executor:
           futures = {executor.submit(process_batch, batch): batch for batch in batches}
           
           with tqdm(total=len(batches), desc="Processing batches") as pbar:
               for future in as_completed(futures):
                   try:
                       batch_results = future.result()
                       with open(output_csv, "a", encoding="utf-8", newline="") as outfile:
                           writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                           writer.writerows(batch_results)
                       pbar.update(1)
                   except Exception as e:
                       logging.error(f"Error processing batch: {str(e)}")
                       logging.error(f"Traceback: {traceback.format_exc()}")

       logging.info("Scraping process completed")

   except Exception as e:
       logging.error(f"CSV processing error: {str(e)}")
       logging.error(f"Traceback: {traceback.format_exc()}")
       raise

if __name__ == "__main__":
   try:
       input_csv = "input.csv" 
       output_csv = "output_reviews2567final.csv"
       logging.info("Starting scraping process")
       process_csv(input_csv, output_csv)
       logging.info("Scraping process completed")
   except Exception as e:
       logging.error(f"Main process error: {str(e)}")
       logging.error(f"Traceback: {traceback.format_exc()}")