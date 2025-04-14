import csv
import requests
from bs4 import BeautifulSoup
from googlesearch import search

def scrape_page(url):
    """Fetch page content from a URL and return text from the <body> tag."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError if the request returned an unsuccessful status code
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract all text from the body. You could refine this to extract only relevant parts.
        return soup.body.get_text(separator=' ', strip=True) if soup.body else ''
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

def main():
    input_csv = "input.csv"
    output_csv = "output_with_scraped_data.csv"
    
    # Read input CSV rows
    rows = []
    with open(input_csv, mode="r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i == 5:  # Only take 5 rows for testing
                break
            rows.append(row)
    
    # Prepare to write new CSV with an extra column
    fieldnames = rows[0].keys()
    # Convert fieldnames to a list to append "ScrapedContent"
    fieldnames = list(fieldnames) + ["ScrapedContent"]
    
    with open(output_csv, mode="w", encoding="utf-8", newline="") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in rows:
            # Construct your search query using whichever fields you want:
            # For example, if the CSV has a column named "query"
            query_str = row["query"] if "query" in row else "example search"
            
            # Use googlesearch to get top 3 URLs
            urls = list(search(query_str, num_results=3))
            
            # Scrape each URL’s content
            scraped_texts = []
            for url in urls:
                text = scrape_page(url)
                scraped_texts.append(text)
            
            # Combine all scraped data
            combined_text = "\n\n".join(scraped_texts)
            
            # Add a new column to the row data
            row["ScrapedContent"] = combined_text
            
            # Write updated row to new CSV
            writer.writerow(row)
            
            # For debugging/verification
            print("Search Query:", query_str)
            print("Scraped URLs:", urls)
            print("Scraped Content (truncated):", combined_text[:200], "...\n")

if __name__ == "__main__":
    main()
