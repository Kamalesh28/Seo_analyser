import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

def get_html(url):
    """Fetch HTML content from a URL"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

def analyze_seo(url):
    """Analyze SEO elements of a webpage"""
    html = get_html(url)
    if not html:
        return

    soup = BeautifulSoup(html, "html.parser")

    # Extract title
    title = soup.title.string if soup.title else "No Title"

    # Extract meta description
    meta_desc = soup.find("meta", attrs={"name": "description"})
    meta_desc = meta_desc["content"] if meta_desc else "No Meta Description"

    # Extract keywords
    meta_keywords = soup.find("meta", attrs={"name": "keywords"})
    meta_keywords = meta_keywords["content"] if meta_keywords else "No Meta Keywords"

    # Extract headers (H1, H2, H3)
    headers = {f"H{i}": [h.text.strip() for h in soup.find_all(f"h{i}")] for i in range(1, 4)}

    # Extract all links
    links = [a["href"] for a in soup.find_all("a", href=True)]
    broken_links = []

    for link in links:
        if not link.startswith("http"):
            continue
        try:
            res = requests.head(link, timeout=5)
            if res.status_code >= 400:
                broken_links.append(link)
        except requests.exceptions.RequestException:
            broken_links.append(link)

    # Extract word count and keyword density
    text = soup.get_text()
    words = re.findall(r'\b\w+\b', text.lower())
    word_count = len(words)
    keyword_density = Counter(words).most_common(10)

    # Print the SEO report
    print("\nSEO Analysis Report:")
    print("=" * 50)
    print(f"Title: {title}")
    print(f"Meta Description: {meta_desc}")
    print(f"Meta Keywords: {meta_keywords}")
    print("\nHeaders Found:")
    for tag, texts in headers.items():
        print(f"{tag}: {texts if texts else 'None'}")

    print(f"\nTotal Word Count: {word_count}")
    print("\nKeyword Density (Top 10 Words):")
    for word, count in keyword_density:
        print(f"{word}: {count}")

    print(f"\nBroken Links: {len(broken_links)}")
    if broken_links:
        print("Broken Links Found:")
        for link in broken_links:
            print(link)


url = input("Enter a website URL: ")
analyze_seo(url)