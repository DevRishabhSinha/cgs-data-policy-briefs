from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_google_reviews(address):
    # Setup WebDriver
    print("[INFO] Setting up the WebDriver...")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode for speed
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Open Google Search
        print("[INFO] Navigating to Google homepage...")
        driver.get("https://www.google.com/")
        
        print("[INFO] Locating the Google search bar...")
        search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
        
        print(f"[INFO] Searching for '{address} reviews'...")
        search_box.send_keys(f"{address} reviews")
        search_box.send_keys(Keys.RETURN)
        
        # Wait for search results to load
        print("[INFO] Waiting for search results to load...")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search")))
        
        # Find and click on the reviews link
        print("[INFO] Locating review links in search results...")
        links = driver.find_elements(By.XPATH, "//a[contains(@href, '/maps/place/')]")
        
        if links:
            print("[INFO] Review link found. Navigating to the reviews page...")
            links[0].click()
        else:
            print("[ERROR] No review link found in search results.")
            return None
        
        # Wait for reviews section to load
        print("[INFO] Waiting for the reviews section to load...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "review-dialog-list"))
        )
        
        # Scrape reviews
        print("[INFO] Extracting reviews from the reviews section...")
        reviews = []
        review_elements = driver.find_elements(By.CSS_SELECTOR, ".review-snippet")
        for element in review_elements:
            print(f"[DEBUG] Found review: {element.text}")
            reviews.append(element.text)
        
        if not reviews:
            print("[WARNING] No reviews were found.")
        return reviews
    
    except Exception as e:
        print(f"[ERROR] An exception occurred: {e}")
        return None
    
    finally:
        print("[INFO] Closing the WebDriver...")
        driver.quit()

# Example Usage
if __name__ == "__main__":
    address = "1600 Amphitheatre Parkway, Mountain View, CA"
    print(f"[INFO] Starting review extraction for: {address}")
    reviews = get_google_reviews(address)
    if reviews:
        print("[SUCCESS] Reviews Found:")
        for review in reviews:
            print("-", review)
    else:
        print("[INFO] No reviews found or an error occurred.")
