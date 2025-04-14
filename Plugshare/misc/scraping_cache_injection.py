from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
import time

# Function to initialize Chrome WebDriver
def init_driver(chrome_driver_path):
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Function to scrape a single PlugShare location
def scrape_location(url):
    driver = init_driver('/Users/a12345/Downloads/chromedriver-mac-arm64/chromedriver')  # Update this path
    driver.get(url)
    time.sleep(3)  # Wait for the page to load
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'display-title'))
        )
        title_text = driver.find_element(By.CLASS_NAME, 'display-title').text
        print(title_text)
    except Exception as e:
        print(f"Error extracting data from {url}: ", e)
    finally:
        driver.quit()

# Main function to run scrapers in parallel
def main():
    base_url = 'https://www.plugshare.com/location/4816'
    urls = [f"{base_url}{11+i}" for i in range(10)]  # Generate URLs with incremented last number

    # Use ThreadPoolExecutor to run multiple instances of the scraper in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(scrape_location, urls)

if __name__ == "__main__":
    main()
