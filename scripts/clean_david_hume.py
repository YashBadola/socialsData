import os

def clean_file(filepath, start_marker, end_marker):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start_index = 0
    end_index = len(lines)

    for i, line in enumerate(lines):
        if start_marker in line:
            start_index = i + 1
        if end_marker in line:
            end_index = i
            break

    content = lines[start_index:end_index]

    # Remove extra whitespace at the beginning and end
    cleaned_content = "".join(content).strip()

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    print(f"Cleaned {filepath}")

base_dir = "socials_data/personalities/david_hume/raw"
files = [
    ("treatise_human_nature.txt", "*** START OF THE PROJECT GUTENBERG EBOOK A TREATISE OF HUMAN NATURE ***", "*** END OF THE PROJECT GUTENBERG EBOOK A TREATISE OF HUMAN NATURE ***"),
    ("enquiry_human_understanding.txt", "*** START OF THE PROJECT GUTENBERG EBOOK AN ENQUIRY CONCERNING HUMAN UNDERSTANDING ***", "*** END OF THE PROJECT GUTENBERG EBOOK AN ENQUIRY CONCERNING HUMAN UNDERSTANDING ***")
]

for filename, start, end in files:
    clean_file(os.path.join(base_dir, filename), start, end)
