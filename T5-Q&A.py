from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import os
from transformers import T5Tokenizer

# Load model and tokenizer
model_name = "valhalla/t5-small-qg-prepend"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
qg_pipeline = pipeline("text2text-generation", model=model, tokenizer=tokenizer, device=-1)  # CPU

# Input and output file paths
input_folder = "/Users/muzammilmohammad/Desktop/CA chatbot/pdf_data/fixed_Income Tax Act 1961 Amended 2024"
output_folder = "/Users/muzammilmohammad/Desktop/CA chatbot/Parse_Data_2/fixed_Income Tax Act 1961 Amended 2024"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Get all .txt files
txt_files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]

for input_file in txt_files:
    input_path = os.path.join(input_folder, input_file)
    output_path = os.path.join(output_folder, input_file)

    # Read input text
    with open(input_path, "r", encoding="utf-8") as infile:
        lines = [line.strip("–•-• \n\t") for line in infile if line.strip()]

    # Generate questions line-by-line
    generated_questions = []
    for i, line in enumerate(lines):
        # Skip very short lines
        if len(line) < 15:
            continue

        # Add optional context from next line if available and meaningful
        context_line = f"{line} {lines[i + 1]}" if i + 1 < len(lines) and len(lines[i + 1]) > 10 else line
        formatted_input = f"generate question: {context_line}"

        try:
            output = qg_pipeline(formatted_input, max_length=64, num_beams=4, num_return_sequences=1, do_sample=False)
            question = output[0]["generated_text"]
            generated_questions.append(f"{len(generated_questions)+1}. {question}")
        except Exception as e:
            print(f"⚠️ Error generating question for line {i+1}: {e}")
            continue

    # Write questions to output file
    with open(output_path, "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(generated_questions))

    print(f"🔹 Processed: {input_file} | ✅ Questions Generated: {len(generated_questions)}")
