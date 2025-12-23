import os

def clean_file(filepath, start_marker, end_marker):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start_index = -1
    end_index = -1

    for i, line in enumerate(lines):
        if start_marker in line:
            start_index = i
        if end_marker in line:
            end_index = i

    if start_index != -1 and end_index != -1:
        # Keep content strictly between markers
        content = lines[start_index + 1 : end_index]
        cleaned_text = "".join(content).strip()

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        print(f"Cleaned {filepath}")
    else:
        print(f"Markers not found in {filepath}. Start: {start_index}, End: {end_index}")

base_path = "socials_data/personalities/david_hume/raw"

clean_file(
    os.path.join(base_path, "enquiry.txt"),
    "*** START OF THE PROJECT GUTENBERG EBOOK AN ENQUIRY CONCERNING HUMAN UNDERSTANDING ***",
    "*** END OF THE PROJECT GUTENBERG EBOOK AN ENQUIRY CONCERNING HUMAN UNDERSTANDING ***"
)

clean_file(
    os.path.join(base_path, "treatise.txt"),
    "*** START OF THE PROJECT GUTENBERG EBOOK A TREATISE OF HUMAN NATURE ***",
    "*** END OF THE PROJECT GUTENBERG EBOOK A TREATISE OF HUMAN NATURE ***"
)
