from googlesearch import search
import pandas as pd
import time
import csv
from datetime import datetime
import logging
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('google_search.log'),
        logging.StreamHandler()
    ]
)

def scrape_google(queries):
    """
    Scrape Google search results for given queries
    """
    results = []
    
    for query in queries:
        logging.info(f"Processing query: {query}")
        try:
            # Search Google
            search_results = search(query, 
                                 lang='en',     
                                 num_results=10)
            
            # Convert generator to list and add to results
            query_results = list(search_results)
            results.extend(query_results)
            
            # Log results
            for url in query_results:
                logging.info(f"Found URL: {url}")
                
            time.sleep(2)  # Delay between queries
            
        except Exception as e:
            logging.error(f"Error fetching results for '{query}': {str(e)}")
    
    return results

def save_results(results, filename):
    """
    Save results to CSV file
    """
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['URL'])  # Header
            for url in results:
                writer.writerow([url])
        logging.info(f"Results saved to {filename}")
    except Exception as e:
        logging.error(f"Error saving results: {str(e)}")

def main():
    # Create output directory if it doesn't exist
    output_dir = 'search_results'
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Read input file
        df = pd.read_csv('input_queries.csv')
        queries = df['query'].tolist()  # Assuming your CSV has a 'query' column

        # Generate timestamp for output file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(output_dir, f'search_results_{timestamp}.csv')

        # Scrape Google
        logging.info("Starting Google scraping...")
        results = scrape_google(queries)

        # Save results
        save_results(results, output_file)
        
        logging.info("Scraping completed successfully")

    except Exception as e:
        logging.error(f"Main process error: {str(e)}")

if __name__ == "__main__":
    main()