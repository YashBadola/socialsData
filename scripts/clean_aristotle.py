import os

def clean_file(filepath, start_marker, end_marker):
    print(f"Cleaning {filepath}...")
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()

    start_idx = -1
    end_idx = -1

    for i, line in enumerate(lines):
        if start_marker in line:
            start_idx = i
        if end_marker in line:
            end_idx = i
            break # Stop after finding the first end marker

    if start_idx != -1 and end_idx != -1:
        # Keep content between markers, excluding the markers themselves
        cleaned_content = "".join(lines[start_idx + 1:end_idx])
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        print(f"Cleaned {filepath} (kept lines {start_idx+1} to {end_idx})")
    else:
        print(f"Markers not found in {filepath}. Start: {start_idx}, End: {end_idx}")

base_path = "socials_data/personalities/aristotle/raw/"

files_config = [
    {
        "filename": "nicomachean_ethics.txt",
        "start": "*** START OF THE PROJECT GUTENBERG EBOOK THE ETHICS OF ARISTOTLE ***",
        "end": "*** END OF THE PROJECT GUTENBERG EBOOK THE ETHICS OF ARISTOTLE ***"
    },
    {
        "filename": "politics.txt",
        "start": "*** START OF THE PROJECT GUTENBERG EBOOK POLITICS: A TREATISE ON GOVERNMENT ***",
        "end": "*** END OF THE PROJECT GUTENBERG EBOOK POLITICS: A TREATISE ON GOVERNMENT ***"
    },
    {
        "filename": "poetics.txt",
        "start": "*** START OF THE PROJECT GUTENBERG EBOOK THE POETICS OF ARISTOTLE ***",
        "end": "*** END OF THE PROJECT GUTENBERG EBOOK THE POETICS OF ARISTOTLE ***"
    }
]

for config in files_config:
    filepath = os.path.join(base_path, config["filename"])
    clean_file(filepath, config["start"], config["end"])
