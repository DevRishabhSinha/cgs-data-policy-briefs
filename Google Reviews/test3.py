import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def scrape_google_reviews(query):
    # Set up WebDriver with Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run browser in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print(f"[INFO] Searching for reviews for: {query}")
        driver.get("https://www.google.com")
        search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
        search_box.send_keys(f"{query} reviews")
        search_box.send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search")))

        # Save page for debugging
        with open("debug_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        # Look for review divs
        review_divs = driver.find_elements(By.CSS_SELECTOR, "div.RfWLue")
        reviews = []
        for div in review_divs:
            try:
                reviews.append(div.text.strip())
            except Exception as e:
                print(f"[ERROR] Unable to extract review: {e}")
        
        return reviews if reviews else "No reviews found."

    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")
        return None
    finally:
        driver.quit()

def process_csv(input_csv, output_csv):
    with open(input_csv, "r", encoding="utf-8") as infile, open(output_csv, "w", encoding="utf-8", newline="") as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ["Reviews"]  # Add a new column for reviews
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            # Construct query string from row data
            query = f"{row['LocationName']} {row['Address']} {row['City']} {row['State']} {row['Postcode']} {row['Country']}"
            reviews = scrape_google_reviews(query)
            row["Reviews"] = "; ".join(reviews) if isinstance(reviews, list) else reviews
            writer.writerow(row)
            print(f"[INFO] Reviews written for: {row['StationID']}")

if __name__ == "__main__":
    input_csv = "input.csv"  # Input file containing address data
    output_csv = "output_reviews.csv"  # Output file for results
    process_csv(input_csv, output_csv)