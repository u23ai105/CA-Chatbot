# import os
# import faiss
# import numpy as np
# from sentence_transformers import SentenceTransformer
# from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline

# # 1) Paths to your data + models
# doc_paths = [
#     r"C:\Users\LENOVO\Desktop\monday-mid\project3\project\server\text_data\text1.txt",
#     r"C:\Users\LENOVO\Desktop\monday-mid\project3\project\server\text_data\text3.txt",
#     r"C:\Users\LENOVO\Desktop\monday-mid\project3\project\server\text_data\text4.txt",
#     r"C:\Users\LENOVO\Desktop\monday-mid\project3\project\server\text_data\text5.txt",
#     r"C:\Users\LENOVO\Desktop\monday-mid\project3\project\server\text_data\text6.txt",
#     r"C:\Users\LENOVO\Desktop\monday-mid\project3\project\server\text_data\text7.txt",
#     r"C:\Users\LENOVO\Desktop\monday-mid\project3\project\server\text_data\text8.txt"
# ]
# MODEL_DIR = r"C:\Users\LENOVO\Desktop\monday-mid\project3\project\server\models"

# # 2) Load your retrieval model (for embeddings) and FAISS index
# retriever = SentenceTransformer('all-MiniLM-L6-v2')
# paragraphs = []
# for path in doc_paths:
#     with open(path, 'r', encoding='utf-8') as f:
#         for para in f.read().split('\n\n'):
#             if para.strip(): paragraphs.append(para.strip())

# embs = retriever.encode(paragraphs, convert_to_numpy=True)
# embs = embs / np.linalg.norm(embs, axis=1, keepdims=True)
# dim = embs.shape[1]
# index = faiss.IndexFlatIP(dim)
# index.add(embs)

# def get_top_contexts(query, k=3):
#     q_emb = retriever.encode([query], convert_to_numpy=True)
#     q_emb = q_emb / np.linalg.norm(q_emb, axis=1, keepdims=True)
#     scores, ids = index.search(q_emb, k)
#     return [(paragraphs[i], float(scores[0][j])) for j,i in enumerate(ids[0])]

# # 3) Load your fine-tuned QA model & create a pipeline
# tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
# model = AutoModelForQuestionAnswering.from_pretrained(MODEL_DIR)
# qa = pipeline("question-answering", model=model, tokenizer=tokenizer, device=0)  # or device=-1 for CPU

# # 4) A helper to pick the “best” answer
# def choose_best_answer(question, contexts):
#     """
#     contexts: list of (text, retrieval_score)
#     returns: best_answer, all_answers
#     """
#     answers = []
#     # produce an answer+model_score for each context
#     for ctx, ret_score in contexts:
#         out = qa(question=question, context=ctx)
#         answers.append({
#             "answer": out["answer"],
#             "qa_score": out["score"],
#             "ret_score": ret_score
#         })

#     # encode question + answers to pick by embedding-similarity
#     texts = [question] + [a["answer"] for a in answers]
#     emb_batch = retriever.encode(texts, convert_to_numpy=True)
#     emb_batch /= np.linalg.norm(emb_batch, axis=1, keepdims=True)

#     q_emb, ans_embs = emb_batch[0], emb_batch[1:]
#     sims = np.dot(ans_embs, q_emb)
#     for a, sim in zip(answers, sims):
#         a["sim_score"] = float(sim)

#     # sort by sim_score (or you could blend sim_score & qa_score+ret_score)
#     answers.sort(key=lambda a: a["sim_score"], reverse=True)
#     return answers[0], answers

# # 5) Putting it all together
# if __name__ == "__main__":
#     user_q = input("Enter your question: ").strip()
#     top_ctxs = get_top_contexts(user_q, k=3)
#     best, all_cands = choose_best_answer(user_q, top_ctxs)

#     print("\n=== Candidate Answers ===")
#     for i,a in enumerate(all_cands, 1):
#         print(f"[{i}] Answer: {a['answer']}")
#         print(f"    QA score: {a['qa_score']:.4f}, Retrieval score: {a['ret_score']:.4f}, Similarity: {a['sim_score']:.4f}")
#         print()

#     print("=== Selected Best Answer ===")
#     print(best["answer"])

import os
import sys
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline

def main(user_question, model_dir, text_data_dir):
    doc_paths = [os.path.join(text_data_dir, file) for file in os.listdir(text_data_dir) if file.endswith('.txt')]

    paragraphs = []
    for path in doc_paths:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            for para in content.split('\n\n'):
                if para.strip():
                    paragraphs.append(para.strip())

    if len(paragraphs) == 0:
        print("No answer found.")
        return

    retriever = SentenceTransformer('all-MiniLM-L6-v2')
    embs = retriever.encode(paragraphs, convert_to_numpy=True)
    embs = embs / np.linalg.norm(embs, axis=1, keepdims=True)
    index = faiss.IndexFlatIP(embs.shape[1])
    index.add(embs)

    def get_top_contexts(query, k=3):
        q_emb = retriever.encode([query], convert_to_numpy=True)
        q_emb = q_emb / np.linalg.norm(q_emb, axis=1, keepdims=True)
        scores, ids = index.search(q_emb, k)
        return [(paragraphs[i], float(scores[0][j])) for j, i in enumerate(ids[0])]

    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForQuestionAnswering.from_pretrained(model_dir)
    qa = pipeline("question-answering", model=model, tokenizer=tokenizer, device=-1)

    def choose_best_answer(question, contexts):
        answers = []
        for ctx, ret_score in contexts:
            try:
                out = qa(question=question, context=ctx)
                answers.append({
                    "answer": out["answer"],
                    "qa_score": out["score"],
                    "ret_score": ret_score
                })
            except:
                continue

        if not answers:
            return "No answer found."

        texts = [question] + [a["answer"] for a in answers]
        emb_batch = retriever.encode(texts, convert_to_numpy=True)
        emb_batch /= np.linalg.norm(emb_batch, axis=1, keepdims=True)

        q_emb, ans_embs = emb_batch[0], emb_batch[1:]
        sims = np.dot(ans_embs, q_emb)

        for a, sim in zip(answers, sims):
            a["sim_score"] = float(sim)

        answers.sort(key=lambda a: a["sim_score"], reverse=True)
        return answers[0]["answer"]

    top_ctxs = get_top_contexts(user_question, k=3)
    return choose_best_answer(user_question, top_ctxs)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python main.py <user_question> <model_dir> <text_data_dir>")
        sys.exit(1)

    user_question = sys.argv[1]
    model_dir = sys.argv[2]
    text_data_dir = sys.argv[3]

    final_answer = main(user_question, model_dir, text_data_dir)
    print(final_answer)
