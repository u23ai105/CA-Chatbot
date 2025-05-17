import nltk
from nltk.tokenize import sent_tokenize

def split_sentences_to_lines(file_path):
    """Reads a text file, splits it into sentences, and saves one sentence per line."""
    # Ensure NLTK punkt is downloaded
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading 'punkt' tokenizer...")
        nltk.download('punkt')

    # Read the file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Split into sentences
    sentences = sent_tokenize(text)

    # Write back to the same file, one sentence per line
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(sentences))

    print(f"✅ File updated: {file_path}")
    print(f"Total sentences: {len(sentences)}")

# Example Usage
if __name__ == "__main__":
    file_path = "/Users/muzammilmohammad/Desktop/CA chatbot/cleaned_data_1/www.incometax.gov.in_iec_foportal_help_verifyservicerequestofERIs.txt"
    split_sentences_to_lines(file_path)