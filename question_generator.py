import os
import nltk
import requests
import re
from nltk.tree import ParentedTree
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.parse.corenlp import CoreNLPParser
from nltk.corpus import wordnet as wn
from copy import deepcopy
import re
from copy import deepcopy


# def download_nltk_resources():
#     try:
#         nltk.data.find('tokenizers/punkt')
#         nltk.data.find('tokenizers/punkt_tab')
#         nltk.data.find('corpora/wordnet')
#     except LookupError:
#         print("Downloading 'punkt', 'punkt_tab', and 'wordnet' resources...")
#         nltk.download('punkt')
#         nltk.download('punkt_tab')
#         nltk.download('wordnet')


# Stanford CoreNLP Server settings
PARSER_URL = "http://localhost:9000"
parser = CoreNLPParser(url=PARSER_URL)

def check_server():
    try:
        response = requests.get(PARSER_URL, timeout=5)
        if response.status_code != 200:
            raise Exception("CoreNLP server not responding.")
    except requests.exceptions.RequestException:
        print("⚠️ CoreNLP server is not running! Start it with:")
        print("java -Xmx16g -cp \"*\" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 60000")
        exit(1)

def preprocess_file(file_path):
    """Cleans and preprocesses the file into sentences."""
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    sentences = sent_tokenize(text)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(sentences))

    print(f"✅ Preprocessed {file_path}: Cleaned and split into sentences.")
    return sentences

def parse_sentence(sentence):
    try:
        response = requests.post(
            f"{PARSER_URL}",
            params={"annotators": "tokenize,ssplit,pos,lemma,ner,parse,depparse", "outputFormat": "json"},
            data=sentence.encode("utf-8"),
            timeout=60
        )
        response.raise_for_status()
        parse_tree = next(parser.raw_parse(sentence))
        return ParentedTree.convert(parse_tree)
    except requests.exceptions.Timeout:
        print("⏳ Timeout: CoreNLP took too long! Skipping sentence.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"🚨 Error parsing sentence: {e}")
        return None

def remove_sbar(tree):
    if not isinstance(tree, ParentedTree):
        return tree
    stack = [tree]
    while stack:
        current = stack.pop()
        i = 0
        while i < len(current):
            subtree = current[i]
            if isinstance(subtree, ParentedTree) and subtree.label() == 'SBAR':
                current[i] = ''
            elif isinstance(subtree, ParentedTree):
                stack.append(subtree)
            i += 1
    return tree

def find_verb_index(tree):
    for i, pos in enumerate(tree.pos()):
        if pos[1].startswith('VB'):
            return i
    return None

def is_valid_question(question):
    words = question.split()
    return len(words) > 3 and words[0] in ['Who', 'What', 'Whose'] and question.endswith('?')


def generate_questions(tree):
    """Generates refined and contextually specific questions from tax or legal documents."""
    questions = set()  # Using a set to avoid duplicate questions
    leaves = tree.leaves()
    text = ' '.join(leaves)  # Convert parse tree to text

    # 🔹 Handle specific treaty references
    treaty_match = re.findall(r'(Article\s*\d+|Treaty|Indo-USA\s*DTAA)', text)
    for treaty in treaty_match:
        questions.add(f"What is the significance of {treaty} in the context of international taxation?")

    # 🔹 Handle Fees for Included Services (FIS) and Fees for Technical Services (FTS)
    if 'Fees for Included Services' in text:
        questions.add("How are Fees for Included Services (FIS) defined in the Indo-USA DTAA?")
    if 'Fees for Technical Services' in text:
        questions.add("How are Fees for Technical Services (FTS) treated in international tax agreements?")

    # 🔹 Handle Royalty and Taxation Rules (Pay Rule, Use Rule)
    if 'Royalty' in text:
        questions.add("How is Royalty taxed in different countries as per international tax agreements?")
    if 'Pay Rule' in text:
        questions.add("What is the 'Pay Rule' for taxing Royalty in international taxation?")
    if 'Use Rule' in text:
        questions.add("What is the 'Use Rule' for taxing Royalty in international taxation?")

    # 🔹 Handle specific countries or jurisdictions mentioned
    countries = ['Australia', 'Germany', 'Japan', 'United States', 'South Africa', 'Argentina', 'EC']
    for country in countries:
        if country in text:
            questions.add(f"What is the tax treatment of royalties in {country}?")

    # 🔹 Handle definitions of terms like 'Fees', 'Royalties', 'Income', etc.
    terms = ['Fees', 'Royalties', 'Income', 'Taxation', 'System', 'Directive']
    for term in terms:
        if term in text:
            questions.add(f"What is the definition of {term} in the context of international taxation?")

    # 🔹 Handling specific examples (like South Africa, Argentina, etc.)
    examples = ['South Africa', 'Argentina']
    for example in examples:
        if example in text:
            questions.add(f"How is royalty taxed in {example} as per international tax law?")

    # 🔹 Handle the role of the OECD and EU in international taxation
    if 'OECD' in text:
        questions.add("What role does the OECD play in shaping international tax rules?")
    if 'EC Directive' in text:
        questions.add("What is the significance of the EC Directive on royalties in international tax law?")

    return list(questions)


def process_text_file(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"⚠️ Error: Input file {input_path} does not exist!")
        return

    sentences = preprocess_file(input_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    all_questions = []
    for i, sentence in enumerate(sentences):
        print(f"\nProcessing Sentence {i + 1}:\n{sentence}...")

        parse_tree = parse_sentence(sentence)
        if parse_tree is None:
            print("❌ Skipping sentence due to parse failure...")
            continue

        questions = generate_questions(parse_tree)
        all_questions.extend(questions)

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write("\n".join(all_questions))

    print(f"\n✅ Questions saved in: {output_path}")
    print("\nGenerated Questions:")
    for q in all_questions:
        print(q)


if __name__ == "__main__":
    # download_nltk_resources()
    check_server()
    input_folder = "/Users/muzammilmohammad/Desktop/CA chatbot/pdf_data/fixed___Ssg4_d_DAVP 2015_DAVP 2014_Vi"
    output_folder = "/Users/muzammilmohammad/Desktop/CA chatbot/Parse_Data_1/fixed___Ssg4_d_DAVP 2015_DAVP 2014_Vi"
    os.makedirs(output_folder, exist_ok=True)

    txt_files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]

    for txt_file in txt_files:
        input_text = os.path.join(input_folder, txt_file)
        output_text = os.path.join(output_folder, txt_file)

        print(f"\n🔹 Processing: {txt_file}")
        process_text_file(input_text, output_text)
