import requests
from bs4 import BeautifulSoup

# URL of the page to scrape
url = 'https://www.plugshare.com/location/552975'

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, 'html.parser')

# Find the specific HTML element by its ID
element = soup.find('md-card')

# Check if the element was found and print it
if element:
    print(element)
else:
    print("Element not found")
