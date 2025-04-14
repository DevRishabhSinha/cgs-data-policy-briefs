import csv
import time
import random
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
]

def get_session():
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, 
                   status_forcelist=[429, 500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session

def clean_text(text):
    """Enhanced text cleaning with multiple processing steps"""
    if not text:
        return ""
        
    # Remove HTML elements
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    
    # Remove special patterns and excessive whitespace
    clean_patterns = [
        r'<!--.*?-->', r'\{.*?\}', r'\[.*?\]', 
        r'+', r'\t', r'\xa0', r'\r', r'\n'
    ]
    
    for pattern in clean_patterns:
        text = re.sub(pattern, ' ', text)
    
    # Remove common footer/navigation phrases
    footer_phrases = [
        'all rights reserved', 'copyright', 'privacy policy',
        'terms of service', 'contact us', 'follow us'
    ]
    text = re.sub(
        r'(?i)\b(' + '|'.join(footer_phrases) + r')\b.*', 
        '', 
        text
    )
    
    # Final cleanup
    text = ' '.join(text.split())
    return text.strip()[:500000]  # Limit to 500KB per page

def clean_url(url):
    """Sanitize and validate URLs from sources"""
    if not url:
        return None
        
    # Remove annotations and invalid parts
    url = re.sub(r'\(.*?\)', '', url)  # Remove (Broken) type annotations
    url = url.split('#')[0].split('?')[0].strip()
    
    # Validate URL format
    if re.match(r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', url):
        return url
    return None

def scrape_page(session, url):
    """Robust page scraping with content validation"""
    if not url:
        return ""
        
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        response = session.get(
            url,
            headers=headers,
            timeout=15,
            allow_redirects=False,
            stream=True
        )
        
        response.raise_for_status()
        
        # Validate content type
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' not in content_type:
            return ""
            
        return clean_text(response.text)
        
    except Exception as e:
        print(f"Error scraping {url[:50]}: {str(e)[:200]}")
        return ""

def safe_google_search(query):
    """Google search with comprehensive error handling"""
    try:
        results = search(
            query,
            num_results=3,
            advanced=True,
            pause=random.uniform(2, 5)
        )
        return [result.url for result in results if result.url]
    except Exception as e:
        print(f"Search failed for '{query[:30]}': {str(e)[:200]}")
        return []

def main():
    input_csv = "input.csv"
    output_csv = "output_final.csv"
    
    session = get_session()
    
    with open(input_csv, mode="r", encoding="utf-8") as f_in:
        reader = csv.DictReader(f_in)
        rows = [row for idx, row in enumerate(reader) if idx < 5]
    
    fieldnames = reader.fieldnames + ["ScrapedContent"]
    
    with open(output_csv, mode="w", encoding="utf-8", newline="") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames, 
                              quoting=csv.QUOTE_ALL)
        writer.writeheader()
        
        for row in rows:
            query_str = row.get("Name_source") or \
                      f"{row.get('Name_English')} {row.get('Name_Indo')}"
            if not query_str:
                continue
                
            try:
                # Google search with random delay
                time.sleep(random.uniform(1, 3))
                urls = safe_google_search(query_str)
                
                # Clean and validate URLs
                valid_urls = [clean_url(u) for u in urls if clean_url(u)]
                print(f"Processing: {query_str}")
                print(f"Valid URLs: {valid_urls}")
                
                # Scrape content with rate limiting
                scraped_content = []
                for url in valid_urls:
                    content = scrape_page(session, url)
                    if content:
                        scraped_content.append(content)
                    time.sleep(random.uniform(1, 2))
                        
                row["ScrapedContent"] = "\n\n".join(scraped_content)
                writer.writerow(row)
                
            except Exception as e:
                print(f"Critical error: {str(e)[:200]}")
                row["ScrapedContent"] = ""
                writer.writerow(row)

if __name__ == "__main__":
    main()
