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
        print("[INFO] Opening Google...")
        driver.get("https://www.google.com")
        
        print("[INFO] Searching for query...")
        search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
        
        # Refine query by adding "reviews" explicitly
        search_query = f"{query} reviews"
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)

        print("[INFO] Waiting for search results...")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search")))

        print("[DEBUG] Page title: ", driver.title)
        print("[DEBUG] Page URL: ", driver.current_url)
        
        # Save the current page source for manual inspection
        with open("debug_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("[INFO] Page source saved as 'debug_page_source.html'")
        
        # Take a screenshot if running in headless mode
        driver.save_screenshot("debug_screenshot.png")
        print("[INFO] Screenshot saved as 'debug_screenshot.png'")
        
        print("[INFO] Searching for review divs...")
        # Attempt to locate divs containing reviews
        review_divs = driver.find_elements(By.CSS_SELECTOR, "div.RfWLue")
        
        if not review_divs:
            print("[DEBUG] No review divs found.")
            return "No reviews found."
        
        print(f"[DEBUG] Found {len(review_divs)} review div(s). Extracting text...")
        reviews = []
        for idx, div in enumerate(review_divs):
            try:
                review_text = div.text.strip()
                reviews.append(review_text)
                print(f"[DEBUG] Review {idx + 1}: {review_text}")
            except Exception as e:
                print(f"[ERROR] Failed to extract review from div {idx + 1}: {e}")
        
        return reviews if reviews else "No reviews found."

    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")
        return None
    
    finally:
        driver.quit()
        print("[INFO] Driver closed.")

# Example usage
if __name__ == "__main__":
    # Refine query: Ensure it's user-friendly and includes "reviews"
    query = "Westar Energy Independence Service Center 1101 E Main Independence KS"
    result = scrape_google_reviews(query)
    print(f"[RESULT] Reviews: {result}")