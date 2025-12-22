import re
import os

def clean_plato_text(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Find the start and end markers
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK THE REPUBLIC ***"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK THE REPUBLIC ***"

    start_index = text.find(start_marker)
    end_index = text.find(end_marker)

    if start_index != -1 and end_index != -1:
        # Extract content between markers
        text = text[start_index + len(start_marker):end_index]
    else:
        print("Warning: Start or end markers not found. Cleaning might be incomplete.")

    # Remove extra whitespace and newlines
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    cleaned_text = "\n".join(lines)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)

if __name__ == "__main__":
    input_file = "socials_data/personalities/plato/raw/republic.txt"
    output_file = "socials_data/personalities/plato/raw/republic_cleaned.txt"

    if os.path.exists(input_file):
        clean_plato_text(input_file, output_file)
        print(f"Cleaned text saved to {output_file}")
        # Optionally replace the original file
        os.replace(output_file, input_file)
        print(f"Original file replaced with cleaned text.")
    else:
        print(f"Input file {input_file} not found.")
