import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time


def fetch_and_extract_data(vin_number):
    url = f"https://www.faxvin.com/vin-decoder/result?vin={vin_number}"
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(10)  # wait for 5 seconds

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    def extract_data(attribute_text):
        try:
            return soup.find('td', text=attribute_text).find_next_sibling('td').text
        except AttributeError:
            return "Not found"

    data = {
        "make": extract_data('Make'),
        "year": extract_data('Model Year'),
        "model": extract_data('Model'),
        "vin": extract_data('VIN'),
        "fuel_economy_city": extract_data('Fuel Economy-city'),
        "msrp": extract_data('MSRP')

    }

    driver.quit()  # Close the browser
    return data


# Load and shuffle the data
filtered_df = pd.read_csv('filtered_df.csv').sample(frac=1, random_state=42).reset_index(drop=True)
filtered_df = filtered_df[0:5]

# Collect data
all_data = [fetch_and_extract_data(row['VIN']) for _, row in filtered_df.iterrows()]

# Save data
df = pd.DataFrame(all_data)
df.to_csv('vin_data.csv', index=False)

print("Data saved to 'vin_data.csv'")