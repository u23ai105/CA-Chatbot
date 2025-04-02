# from urllib.parse import urlparse
# from collections import defaultdict
#
# # Load URLs from file
# with open('urllist.txt', 'r') as file:
#     urls = [line.strip() for line in file.readlines()]
#
# # Identify common URL patterns
# url_patterns = defaultdict(int)
# for url in urls:
#     path_segments = urlparse(url).path.split('/')
#     for segment in path_segments:
#         if segment:
#             url_patterns[segment] += 1
#
# # Display URL patterns for analysis
# print("URL Patterns Found:")
# for pattern, count in sorted(url_patterns.items(), key=lambda x: x[1], reverse=True)[:20]:
#     print(f"{pattern}: {count}")
#
# # Select meaningful keywords
# important_keywords = [
#     'acts', 'rules', 'circulars', 'notifications', 'exemptions', 'deductions',
#     'forms', 'downloads', 'taxpayer', 'guidelines', 'how-to-file'
# ]
#
# # Filter URLs based on meaningful keywords
# filtered_urls = list(set([url for url in urls if any(keyword in url.lower() for keyword in important_keywords)]))
#
# print(f"\nTotal URLs Found: {len(urls)}")
# print(f"Filtered URLs (Relevant Links): {len(filtered_urls)}")
#
# # Display filtered URLs
# for url in filtered_urls:
#     print(url)

from urllib.parse import urlparse

# Load URLs from file
with open('urllist.txt', 'r') as file:
    urls = [line.strip() for line in file.readlines()]

# Define keywords relevant to tax-related information for chatbot
important_keywords = [
    'acts', 'rules', 'circulars', 'notifications', 'exemptions', 'deductions',
    'forms', 'downloads', 'guidelines', 'how-to-file', 'charts-and-tables',
    'income-tax-return', 'faqs', 'utilities', 'statutory-forms', 'popular-form'
]

# Filter URLs using meaningful keywords
filtered_urls = list(set([url for url in urls if any(keyword in url.lower() for keyword in important_keywords)]))

# Write filtered URLs back to the text file
with open('filtered_urls.txt', 'w') as file:
    file.write('\n'.join(filtered_urls))

print(f"Total URLs Found: {len(urls)}")
print(f"Filtered URLs (Relevant Links): {len(filtered_urls)}")
print("Filtered URLs have been saved in 'filtered_urls.txt'.")

