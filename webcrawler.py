# import requests
# from bs4 import BeautifulSoup
# import time
# import random
# import os
#
# # Load URLs from the previously saved file
# with open('urllist.txt', 'r') as file:
#     urls = file.read().strip().split('\n')
#
# # Create a folder for extracted data
# os.makedirs("main_extracted_data", exist_ok=True)
#
#
# # Function to clean extracted text
# def clean_text(text):
#     return ' '.join(text.strip().split())
#
#
# # Tags to extract
# content_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6',
#                 'p', 'li', 'div', 'span', 'strong', 'b',
#                 'table', 'code', 'a']
#
# # Crawl and extract data
# for url in urls:
#     try:
#         response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.content, 'html.parser')
#
#             # Extract text from target tags
#             content = ''
#             for tag in soup.find_all(content_tags):
#                 if tag.name == 'a' and 'href' in tag.attrs:  # Extract document links
#                     content += f"[LINK] {tag['href']} - {clean_text(tag.get_text())}\n"
#                 elif tag.name == 'table':
#                     table_data = []
#                     for row in tag.find_all('tr'):
#                         row_data = [clean_text(cell.get_text()) for cell in row.find_all(['th', 'td'])]
#                         table_data.append(' | '.join(row_data))
#                     content += "\n".join(table_data) + "\n"
#                 else:
#                     content += clean_text(tag.get_text()) + "\n"
#
#             # Save extracted content to a text file
#             filename = url.replace('https://', '').replace('/', '_') + '.txt'
#             with open(f"extracted_data/{filename}", 'w', encoding='utf-8') as file:
#                 file.write(content)
#
#             print(f"✅ Extracted content from: {url}")
#         else:
#             print(f"❌ Failed to access: {url}")
#
#         # Add a delay to avoid overwhelming the server
#         time.sleep(random.uniform(1, 3))
#
#     except Exception as e:
#         print(f"❌ Error scraping {url}: {e}")




from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import os
import random

# Path to ChromeDriver (Ensure this path matches your setup)
CHROME_DRIVER_PATH = "/usr/local/bin/chromedriver"

# Load URLs from the previously saved file
with open('urllist.txt', 'r') as file:
    urls = file.read().strip().split('\n')

# Create folder for extracted data
os.makedirs("main_extracted_data", exist_ok=True)

# Initialize ChromeDriver
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)

# Function to clean text
def clean_text(text):
    return ' '.join(text.strip().split())

# Tags to extract content
content_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'p', 'li', 'div', 'span', 'strong', 'b',
                'table', 'code', 'a']

# Crawl and extract data
for url in urls:
    try:
        driver.get(url)
        time.sleep(random.uniform(2, 4))  # Delay to avoid blocking

        # Extract content with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        content = ''
        for tag in soup.find_all(content_tags):
            if tag.name == 'a' and 'href' in tag.attrs:
                content += f"[LINK] {tag['href']} - {clean_text(tag.get_text())}\n"
            elif tag.name == 'table':
                table_data = []
                for row in tag.find_all('tr'):
                    row_data = [clean_text(cell.get_text()) for cell in row.find_all(['th', 'td'])]
                    table_data.append(' | '.join(row_data))
                content += "\n".join(table_data) + "\n"
            else:
                content += clean_text(tag.get_text()) + "\n"

        # Save content to a file
        filename = url.replace('https://', '').replace('/', '_') + '.txt'
        with open(f"main_extracted_data/{filename}", 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"✅ Extracted content from: {url}")

    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")

# Close the browser
driver.quit()
