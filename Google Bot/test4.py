import csv
import time
import requests
from bs4 import BeautifulSoup
from readability import Document
from googlesearch import search

def scrape_page(url):
    """
    Fetch the URL, parse it with readability-lxml for main content,
    remove obvious boilerplate tags, and return text.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/98.0.4758.102 Safari/537.36"
        )
    }
    try:
        # Give the site a short pause (helps reduce blocking)
        time.sleep(2)
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Use readability-lxml to isolate main content
        doc = Document(response.text)
        cleaned_html = doc.summary()

        # Parse cleaned HTML with BeautifulSoup
        soup = BeautifulSoup(cleaned_html, 'html.parser')

        # Remove scripts, styles, and common layout elements
        for tag in soup.find_all(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            tag.decompose()

        # Extract text
        text = soup.get_text(separator=' ', strip=True)
        return text

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

def main():
    input_csv = "input.csv"
    output_csv = "output_with_scraped_data.csv"

    # Read at most 5 rows from CSV
    rows = []
    with open(input_csv, mode="r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i == 5:  # stop after 5 data rows
                break
            rows.append(row)

    if not rows:
        print("No rows found in CSV or CSV is empty.")
        return

    # Prepare new CSV columns
    fieldnames = list(rows[0].keys()) + ["ScrapedContent"]

    with open(output_csv, mode="w", encoding="utf-8", newline="") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            # Build a search query from a suitable CSV column.
            # Adjust if your CSV uses different column names.
            # Fallback to "Generic Search Query" if empty.
            query_str = row.get("Name_source") or "Generic Search Query"

            # Pause between Google queries
            time.sleep(2)
            
            # Retrieve up to 3 direct links from Google
            # (googlesearch 'search' does not require a separate parse of SERP)
            try:
                urls = list(search(query_str, num_results=3))
            except Exception as e:
                print(f"Google Search error for '{query_str}': {e}")
                urls = []

            # Debug print
            print(f"Query: {query_str}")
            print("URLs found:", urls)

            # Scrape each URL
            scraped_texts = []
            for url in urls:
                # If a link looks broken or is obviously not a real site, skip it
                if "Broken" in url or not url.startswith("http"):
                    continue
                page_content = scrape_page(url)
                if page_content:
                    scraped_texts.append(page_content)

            # Join all scraped content with some spacing
            combined_text = "\n\n".join(scraped_texts)
            row["ScrapedContent"] = combined_text

            writer.writerow(row)

            # Optional: console output for verification
            snippet = (combined_text[:300] + "...") if len(combined_text) > 300 else combined_text
            print("ScrapedContent snippet:\n", snippet, "\n")

if __name__ == "__main__":
    main()
