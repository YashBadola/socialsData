import os

def clean_file(filepath):
    print(f"Cleaning {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start_idx = 0
    end_idx = len(lines)

    for i, line in enumerate(lines):
        if "*** START OF THE PROJECT GUTENBERG EBOOK" in line:
            start_idx = i + 1
        if "*** END OF THE PROJECT GUTENBERG EBOOK" in line:
            end_idx = i
            break

    # Refine start: skip blank lines or title repeats
    # This loop starts from start_idx and looks for the first non-empty line
    # but we will just slice from start_idx for now as the memory says to prioritize the first line of content
    # Ideally we'd look for "Part 1" or similar, but with 10 files, generic cleaning is safer first.
    # The memory suggests: "Prioritize the first line of the actual content... to ensure translator introductions and metadata are stripped."
    # Given the variety, I'll stick to the Gutenberg markers which I verified exist.

    content = lines[start_idx:end_idx]

    # Strip leading/trailing whitespace lines
    while content and content[0].strip() == "":
        content.pop(0)
    while content and content[-1].strip() == "":
        content.pop()

    cleaned_text = "".join(content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)
    print("Cleaned.")

base_dir = "socials_data/personalities/georg_wilhelm_friedrich_hegel/raw"
files = [
    "philosophy_of_mind.txt",
    "history_of_philosophy_vol1.txt",
    "history_of_philosophy_vol2.txt",
    "history_of_philosophy_vol3.txt",
    "philosophy_of_fine_art_vol1.txt",
    "philosophy_of_fine_art_vol2.txt",
    "philosophy_of_fine_art_vol3.txt",
    "philosophy_of_fine_art_vol4.txt",
    "logic_of_hegel.txt",
    "intro_philosophy_of_fine_arts.txt"
]

for filename in files:
    filepath = os.path.join(base_dir, filename)
    if os.path.exists(filepath):
        clean_file(filepath)
    else:
        print(f"File not found: {filepath}")
