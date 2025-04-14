from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def test_eight_components():
    # Set up the WebDriver
    driver = webdriver.Chrome()


    # Navigate to the page
    driver.get("https://www.tianyancha.com/company/26149090")

    # Wait for the page to load. Increase the wait time if necessary.
    time.sleep(5)

    # Find the table by CSS selector (update this selector to match the table's CSS on the actual page)
    table = driver.find_element(By.CSS_SELECTOR, 'table.table-wrap')

    # Find all the rows in the table body
    rows = table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

    # Loop over the rows and print the text content of each cell
    for row in rows:
        # Find all the cells in the row
        cells = row.find_elements(By.TAG_NAME, 'td')
        # Extract and print the text from each cell
        for cell in cells:
            print(cell.text)

    # Close the browser when done
    driver.quit()

# Run the function
test_eight_components()
