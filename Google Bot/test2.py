import csv
import time
import requests
from bs4 import BeautifulSoup
from googlesearch import search

def scrape_page(url):
    """Fetch page content from the URL and return text."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/98.0.4758.102 Safari/537.36"
        )
    }
    try:
        # Small delay to avoid rapid-fire requests
        time.sleep(3)
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.body.get_text(separator=' ', strip=True) if soup.body else ''
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

def main():
    input_csv = "input.csv"
    output_csv = "output_with_scraped_data.csv"
    
    # Read first 5 rows
    rows = []
    with open(input_csv, mode="r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i == 5:
                break
            rows.append(row)
    
    # Prepare new CSV columns
    fieldnames = list(rows[0].keys()) + ["ScrapedContent"]
    
    # Write output
    with open(output_csv, mode="w", encoding="utf-8", newline="") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in rows:
            # Build your search query from whichever field(s) you like
            # Example: row["Name_English"] or row["Name_source"], etc.
            query_str = row["Name_source"] or "Example fallback query"
            
            # Pause between each Google query (be polite, reduce blocking)
            time.sleep(2)
            
            # Get top 3 search results
            urls = list(search(query_str, num_results=3))
            
            # Debug: print the URLs
            print(f"Query: {query_str}")
            print("URLs found:", urls)
            
            # Scrape each URL for text
            scraped_texts = []
            for url in urls:
                page_content = scrape_page(url)
                scraped_texts.append(page_content)
            
            combined_text = "\n\n".join(scraped_texts)
            row["ScrapedContent"] = combined_text
            
            writer.writerow(row)
            print("Scraped content (truncated):", combined_text[:200], "...\n")

if __name__ == "__main__":
    main()
