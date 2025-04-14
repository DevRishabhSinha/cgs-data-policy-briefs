from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.chrome.options import Options


def fetch_and_extract_data(location_id):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-images")
    chrome_options.add_argument("--disable-css")

    driver = webdriver.Chrome(options=chrome_options)
    url = f"https://www.plugshare.com/location/{location_id}"
    driver.get(url)
    time.sleep(5)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Scraping general information
    try:
        address = soup.find('a', {'property': 'v:address'}).text
    except AttributeError:
        address = "Not found"

    try:
        phone = soup.find('a', {'property': 'v:tel'}).text
    except AttributeError:
        phone = "Not found"

    try:
        cost = soup.find('div', {'title': 'Cost'}).find_next_sibling('div').text
    except AttributeError:
        cost = "Not found"

    try:
        parking = soup.find('div', {'title': 'Parking'}).find_next_sibling('div').text
    except AttributeError:
        parking = "Not found"

    try:
        station_name = soup.find('h1', {'property': 'v:name'}).text
    except AttributeError:
        station_name = "Not found"

    # Scraping plug information
    connector_div = soup.find('div', class_='connector')
    if connector_div:
        plug_name = connector_div.find('span', class_='plug-name').text if connector_div.find('span', class_='plug-name') else "Not found"
        plug_count = connector_div.find('span', class_='plug-count').text if connector_div.find('span', class_='plug-count') else "Not found"
        plug_power = connector_div.find('span', class_='plug-power').text if connector_div.find('span', class_='plug-power') else "Not found"
        stations_count = connector_div.find('span', class_='station-count').text if connector_div.find('span', class_='station-count') else "Not found"
        availability = connector_div.find('span', class_='status').text if connector_div.find('span', class_='status') else "Not found"
    else:
        plug_name = plug_count = plug_power = stations_count = availability = "Not found"

    # Scraping check-ins
    check_ins = []
    try:
        check_in_divs = soup.find_all('div', class_='checkin')
        for check_in_div in check_in_divs:
            check_in_text = check_in_div.find('div', class_='message').text if check_in_div.find('div', class_='message') else "No message"
            check_in_date = check_in_div.find('div', class_='date').text if check_in_div.find('div', class_='date') else "No date"
            check_ins.append({
                "message": check_in_text,
                "date": check_in_date
            })
    except AttributeError:
        check_ins = "Not found"

    driver.quit()

    return {
        "location_id": location_id,
        "station_name": station_name,
        "address": address,
        "phone": phone,
        "cost": cost,
        "parking": parking,
        "plug_name": plug_name,
        "plug_count": plug_count,
        "plug_power": plug_power,
        "stations_count": stations_count,
        "availability": availability,
        "check_ins": check_ins
    }


# Initialize an empty list to hold scraped data
all_data = []

# Scrape data for IDs starting from 15151, incrementing by 1
for i in range(15151, 15161):  # Change the range as needed
    data = fetch_and_extract_data(i)
    all_data.append(data)

# Convert list to DataFrame and save as CSV
df = pd.DataFrame(all_data)
df.to_csv('plugshare_data.csv', index=False)

print("Data saved to 'plugshare_data.csv'")
