import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Path to your text file with URLs (replace with your file path)
url_file = "useful_tax_urls.txt"

# Directory to save the PDFs
save_folder = "downloaded_pdfs"
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# Headers to mimic a browser
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# Function to download a PDF
def download_pdf(pdf_url, folder):
    try:
        pdf_name = os.path.basename(pdf_url.split("?")[0])  # Remove query params from filename
        if not pdf_name.endswith(".pdf"):
            pdf_name += ".pdf"  # Ensure it has .pdf extension
        file_path = os.path.join(folder, pdf_name)

        # Skip if file already exists to avoid duplicates
        if os.path.exists(file_path):
            print(f"Skipping (already downloaded): {pdf_name}")
            return

        pdf_response = requests.get(pdf_url, headers=headers, stream=True)
        pdf_response.raise_for_status()
        with open(file_path, "wb") as pdf_file:
            for chunk in pdf_response.iter_content(chunk_size=8192):
                if chunk:
                    pdf_file.write(chunk)
        print(f"Saved: {pdf_name}")
    except Exception as e:
        print(f"Error downloading {pdf_url}: {e}")

# Read URLs from the text file
with open(url_file, "r") as file:
    urls = [line.strip() for line in file if line.strip()]  # Remove empty lines

print(f"Found {len(urls)} URLs in the file")

# Visit each URL and download PDFs
for url in urls:
    try:
        print(f"Scraping: {url}")
        page_response = requests.get(url, headers=headers)
        page_response.raise_for_status()
        soup = BeautifulSoup(page_response.text, "html.parser")

        # Find all links on the page
        links = soup.find_all("a")
        for link in links:
            href = link.get("href")
            if href and href.lower().endswith(".pdf"):
                pdf_url = urljoin(url, href)  # Convert relative URLs to absolute
                download_pdf(pdf_url, save_folder)
    except Exception as e:
        print(f"Error scraping {url}: {e}")

print("Download process complete!")