# import os
# import re
# from collections import Counter
#
# # Path to the extracted data folder
# data_folder = 'main_extracted_data'
#
# # Function to clean text for analysis
# def clean_text(text):
#     return re.sub(r'[^\w\s]', '', text).lower()
#
# # Collect data from files
# all_text = []
# for filename in os.listdir(data_folder):
#     with open(os.path.join(data_folder, filename), 'r', encoding='utf-8') as file:
#         all_text.append(file.read())
#
# # Combine all text
# combined_text = '\n'.join(all_text)
#
# # Identify suspicious patterns
# patterns = {
#     'Repeated Text Blocks': re.findall(r'(.*?)\n\1{3,}', combined_text),  # Lines repeated 3+ times
#     'Suspicious Symbols': re.findall(r'[=>_]{3,}', combined_text),         # Symbols like ==> or ___
#     'Short Lines (<10 chars)': [line for line in combined_text.split('\n') if len(line.strip()) < 10],
#     'Long Lines (>200 chars)': [line for line in combined_text.split('\n') if len(line.strip()) > 200]
# }
#
# # Display results
# for pattern_name, results in patterns.items():
#     print(f"\n{pattern_name} (Found {len(results)} items):")
#     for sample in results[:10]:  # Display only first 10 for preview
#         print(f"- {sample.strip()}")
#
# # Boilerplate Detection: Detect duplicate text blocks
# block_counter = Counter(all_text)
# repeated_blocks = [block for block, count in block_counter.items() if count > 5]
#
# print("\nRepeated Boilerplate Blocks (Preview):")
# for block in repeated_blocks[:5]:
#     print(f"- {block.strip()[:100]}...")  # Show only first 100 chars for preview



import os
import re
import collections
from nltk.tokenize import sent_tokenize

# Define file path
INPUT_FILE = "/Users/muzammilmohammad/Desktop/CA chatbot/cleaned_data_1/www.incometax.gov.in_iec_foportal_help_verifyservicerequestofERIs.txt"
CLEANED_FILE = "/Users/muzammilmohammad/Desktop/CA chatbot/cleaned_data_1/www.incometax.gov.in_iec_foportal_help_verifyservicerequestofERIs.txt"

# Function to detect frequent patterns
def detect_patterns(text, min_length=5, top_n=10):
    """Finds frequently occurring phrases in the text to identify unwanted patterns."""
    words = text.split()
    word_freq = collections.Counter(words)

    # Get most common words (that are longer than min_length)
    common_patterns = [word for word, count in word_freq.most_common(top_n) if len(word) > min_length]
    return common_patterns

# Function to clean detected patterns
def remove_patterns(text, patterns):
    """Removes detected unwanted patterns from the text."""
    for pattern in patterns:
        text = re.sub(re.escape(pattern), "", text, flags=re.IGNORECASE)
    return text

# Read input file
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    raw_text = f.read()

# Detect frequent patterns
detected_patterns = detect_patterns(raw_text, min_length=5, top_n=15)
print(f"🔍 Detected Repetitive Patterns: {detected_patterns}")

# Remove detected patterns
cleaned_text = remove_patterns(raw_text, detected_patterns)

# Save cleaned data
with open(CLEANED_FILE, "w", encoding="utf-8") as f:
    f.write(cleaned_text)

print(f"✅ Cleaned text saved as {CLEANED_FILE}!")

