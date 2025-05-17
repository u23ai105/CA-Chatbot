import requests
from bs4 import BeautifulSoup
import os

# Input: File containing URLs
input_file = "urllist.txt"  # Change this to your file containing URLs
output_file = "faq_data.txt"


def read_urls(file_path):
    """Reads URLs from a text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines() if line.strip()]


def extract_faqs(url):
    """Extracts FAQs from a webpage."""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"⚠️ Skipping {url} (HTTP {response.status_code})")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find FAQ sections - Modify these selectors based on the website's structure
        faq_sections = soup.find_all(lambda tag: tag.name in ["div", "section"] and "faq" in tag.get("class", []))

        faqs = []
        for section in faq_sections:
            questions = section.find_all(["h2", "h3", "h4", "p"], string=lambda text: text and "?" in text)
            answers = section.find_all("p")

            for q in questions:
                answer = q.find_next_sibling("p")
                if answer:
                    faqs.append(f"Q: {q.text.strip()}\nA: {answer.text.strip()}\n")

        return faqs if faqs else None

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching {url}: {e}")
        return None


def save_faqs(faqs, output_path):
    """Saves extracted FAQs to a text file."""
    with open(output_path, 'w', encoding='utf-8') as file:
        file.writelines(faq + "\n" for faq in faqs)
    print(f"\n✅ FAQs saved to {output_path}")


def main():
    urls = read_urls(input_file)
    all_faqs = []

    for url in urls:
        print(f"🔍 Processing: {url}")
        faqs = extract_faqs(url)
        if faqs:
            all_faqs.extend(faqs)

    if all_faqs:
        save_faqs(all_faqs, output_file)
    else:
        print("❌ No FAQs found!")


if __name__ == "__main__":
    main()
