import os

# Provide the path to your test file
TEST_FILE = "/Users/muzammilmohammad/Desktop/CA chatbot/cleaned_data_1/www.incometax.gov.in_iec_foportal_help_verifyservicerequestofERIs.txt"

def remove_duplicate_lines_from_file(file_path):
    """Removes duplicate lines while preserving one instance of each."""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Remove duplicates while keeping the first occurrence
        seen = set()
        unique_lines = []
        for line in lines:
            if line.strip() and line not in seen:  # Keep first occurrence
                seen.add(line)
                unique_lines.append(line)

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(unique_lines)

        print(f"✅ Duplicate lines removed, keeping one instance in: {file_path}")

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")

# Run the cleaning process on the test file
remove_duplicate_lines_from_file(TEST_FILE)
