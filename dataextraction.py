import requests
from bs4 import BeautifulSoup

# Sitemap URL
sitemap_url = "https://www.incometax.gov.in/iec/foportal/sitemap.xml"

# Fetch and parse the sitemap
response = requests.get(sitemap_url)
soup = BeautifulSoup(response.content, 'xml')

# Extract URLs from <loc> tags
urls = [url.text for url in soup.find_all('loc')]

# Refined keywords for broader coverage
keywords = [
    '/acts/', '/exemptions/', '/deductions/', '/circulars/',
    '/notifications/', '/forms/', '/returns/', '/guidelines/',
    '/services/', '/faq/', '/resources/', '/income-tax/',
    '/downloads/', '/publications/', '/tax-payer/', '/help/',
    '/all-topics/', '/statutory-forms/', '/popular-form/',
    '/individual/', '/e-filing-services/', '/how-to-file-tax-returns/'
]

# Filter URLs using improved keywords
filtered_urls = [url for url in urls if any(keyword in url.lower() for keyword in keywords)]

print(f"\nTotal URLs Found: {len(urls)}")
print(f"Filtered URLs (Relevant Links): {len(filtered_urls)}")

# Display filtered URLs
for url in filtered_urls:
    print(url)

# Optional: Save filtered URLs to a file
with open('useful_tax_urls.txt', 'w') as file:
    file.write('\n'.join(filtered_urls))
