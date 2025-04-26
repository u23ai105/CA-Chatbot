import faiss
import json
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load FAISS index
index = faiss.read_index("/Users/muzammilmohammad/Desktop/CA chatbot/Answers_cos/fixed_CGST-Act-Updated/cosin_ans.faiss")

# Load questions and answers from JSON
with open('/Users/muzammilmohammad/Desktop/CA chatbot/Answers_cos/fixed_CGST-Act-Updated/cosine_similarity_answers.json', 'r') as f:
    qa_list = json.load(f)

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')


def search_best_answer(user_question):
    # Embed user question
    user_embedding = model.encode([user_question], convert_to_numpy=True)

    # Search in FAISS
    D, I = index.search(np.array(user_embedding), k=5)

    best_similarity = 0
    best_idx = -1

    for idx in I[0]:
        if idx == -1:
            continue

        matched_question = qa_list[idx]['question']
        matched_embedding = model.encode([matched_question], convert_to_numpy=True)

        sim = cosine_similarity(user_embedding, matched_embedding)[0][0]

        if sim > best_similarity:
            best_similarity = sim
            best_idx = idx

    if best_similarity >= 0.40 and best_idx != -1:
        return qa_list[best_idx]['answer']
    else:
        return "No matching question found."


# Interactive loop
while True:
    user_input = input("\nAsk your question (or type 'exit' to quit): ")
    if user_input.lower() == 'exit':
        break
    answer = search_best_answer(user_input)
    print("\nAnswer:", answer)
