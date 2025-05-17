import os
from datetime import datetime


def count_file_stats(filepath):
    """Count statistics for a single file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        words = len(content.split())
        chars_total = len(content)
        chars_no_space = len(content.replace(" ", ""))
        lines = len(content.split('\n'))
        return {
            'filename': os.path.basename(filepath),
            'words': words,
            'chars_total': chars_total,
            'chars_no_space': chars_no_space,
            'lines': lines
        }


def generate_report(folder_path, output_file):
    """Generate a well-formatted report"""
    # Get all text files
    text_files = [f for f in os.listdir(folder_path)
                  if f.endswith('.txt') and os.path.isfile(os.path.join(folder_path, f))]

    if not text_files:
        print("No text files found in the folder.")
        return

    # Process files and collect data
    all_stats = []
    for filename in text_files:
        try:
            stats = count_file_stats(os.path.join(folder_path, filename))
            all_stats.append(stats)
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    # Determine column widths
    max_filename = max(len(s['filename']) for s in all_stats) + 2
    max_filename = max(max_filename, 20)  # Minimum width for filename

    # Write to output file with proper formatting
    with open(output_file, 'w', encoding='utf-8') as f:
        # Header
        f.write("TEXT FILE ANALYSIS REPORT\n".center(80))
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Folder: {os.path.abspath(folder_path)}\n\n")

        # Column headers
        headers = {
            'filename': 'FILENAME',
            'lines': 'LINES',
            'words': 'WORDS',
            'chars_total': 'CHARS (TOTAL)',
            'chars_no_space': 'CHARS (NO SPACES)'
        }

        # Format string for rows
        row_format = (f"| {{filename:<{max_filename}}} "
                      f"| {{lines:>8}} "
                      f"| {{words:>8}} "
                      f"| {{chars_total:>12}} "
                      f"| {{chars_no_space:>16}} |\n")

        # Divider line
        divider = ("+" + "-" * (max_filename + 2) +
                   "+" + "-" * 30 +
                   "+" + "-" * 30 +
                   "+" + "-" * 34 +
                   "+" + "-" * 38 + "+\n")

        f.write(divider)
        f.write(row_format.format(**headers))
        f.write(divider)

        # Data rows
        for stats in all_stats:
            f.write(row_format.format(**stats))
        f.write(divider)

        # Summary
        total_files = len(all_stats)
        total_words = sum(s['words'] for s in all_stats)
        total_chars = sum(s['chars_total'] for s in all_stats)

        f.write(f"\nSUMMARY:\n")
        f.write(f"Files analyzed: {total_files}\n")
        f.write(f"Total words: {total_words}\n")
        f.write(f"Total characters: {total_chars}\n")


if __name__ == "__main__":
    folder = input("Enter folder path: ").strip()
    if not os.path.isdir(folder):
        print("Invalid folder path")
        exit()

    output = "file_analysis_report_0.txt"
    generate_report(folder, output)
    print(f"Report generated: {os.path.abspath(output)}")