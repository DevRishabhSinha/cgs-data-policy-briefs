import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Selenium in headless mode for faster execution
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Read the input CSV
df = pd.read_csv('input.csv')

# Create a new DataFrame for the updated data
new_df = df.copy()

# Function to get reviews from Google search
def get_reviews(query):
    """
    Performs a Google search for the query and extracts reviews from the Knowledge Panel.
    
    Args:
        query (str): The search query string.
    
    Returns:
        list: List of review texts, or empty list if no reviews are found.
    """
    search_url = f"https://www.google.com/search?q={query}+reviews"
    driver.get(search_url)
    time.sleep(2)  # Wait for the page to load
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Find the Knowledge Panel
    knowledge_panel = soup.find('div', {'data-hveid': 'CC8QAQ'})
    if knowledge_panel:
        review_elements = knowledge_panel.find_all('div', class_='RfWLue')
        reviews = []
        for element in review_elements:
            review_text = element.find('a', class_='a-no-hover-decoration').text
            reviews.append(review_text)
        return reviews
    else:
        return []

# Process the first three data rows (indices 0 to 2 in pandas)
for i in range(3):
    row = df.iloc[i]
    # Concatenate location details
    query = ','.join([row['LocationName'], row['Address'], row['City'], row['State'], row['Postcode'], row['Country']])
    reviews = get_reviews(query)
    original_comments = row['Comments']
    
    # Append reviews to existing comments
    if pd.notna(original_comments) and original_comments.strip() != "":
        if reviews:
            new_comments = original_comments + "; Reviews: " + "; ".join(reviews)
        else:
            new_comments = original_comments + "; No reviews found"
    else:
        if reviews:
            new_comments = "Reviews: " + "; ".join(reviews)
        else:
            new_comments = "No reviews found"
    new_df.at[i, 'Comments'] = new_comments

# Print the first three data rows with header
print(new_df.head(3))

# Save the new DataFrame to a new CSV file
new_df.to_csv('output.csv', index=False)

# Close the Selenium driver
driver.quit()