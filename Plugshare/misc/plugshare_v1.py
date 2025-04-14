from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

url = 'https://www.plugshare.com/location/38443'  # Replace with the actual URL

# Initialize a WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get(url)

# Wait for JavaScript to load
time.sleep(5)  # Adjust time as necessary

# Now use BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

checkins = soup.select('#checkins .checkin')

for checkin in checkins:
    date = checkin.select_one('.date').text if checkin.select_one('.date') else 'No Date'
    user = checkin.select_one('.user').text if checkin.select_one('.user') else 'No User'
    comment = checkin.select_one('.comment').text if checkin.select_one('.comment') else 'No Comment'
    print(f"Date: {date}, User: {user}, Comment: {comment}")
