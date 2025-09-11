import requests
from bs4 import BeautifulSoup

# Step 1: Get the main page
url = "https://oif.gov.hu/factsheets"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Step 2: Find all links with the target class
links = soup.find_all("a", class_="btn btn-primary px-4 mt-3")
link_urls = [link['href'] for link in links if link.get('href')]

print(f"Found {len(link_urls)} links.")

# Step 3: Scrape MsoNormal paragraphs from each link
all_text = []

for i, link in enumerate(link_urls, 1):
    # Make absolute URL if necessary
    if not link.startswith("http"):
        link = f"https://oif.gov.hu{link}"
    
    resp = requests.get(link)
    page_soup = BeautifulSoup(resp.text, 'html.parser')
    
    # Get all paragraphs with class MsoNormal
    paragraphs = page_soup.find_all("p", class_="MsoNormal")
    page_text = " ".join(p.get_text(strip=True) for p in paragraphs)
    
    all_text.append(page_text)
    
    print(f"\nContent from link {i}: {link}\n")
    print(page_text[:800], "...")  # preview first 800 chars

# Combine all pages into one string
full_text = "\n\n".join(all_text)
