import os
import re

RAW_DIR = "socials_data/personalities/aristotle/raw"

CONFIG = {
    "nicomachean_ethics.txt": {
        "start_marker": "ARISTOTLE’S ETHICS",
        "start_offset": "BOOK I",
        "end_marker": "END OF THE PROJECT GUTENBERG EBOOK"
    },
    "politics.txt": {
        "start_marker": "A TREATISE ON GOVERNMENT",
        "start_offset": "BOOK I",
        "end_marker": "END OF THE PROJECT GUTENBERG EBOOK"
    },
    "poetics.txt": {
        "start_marker": "ARISTOTLE'S POETICS",
        "start_offset": "I",
        "end_marker": "END OF THE PROJECT GUTENBERG EBOOK"
    },
    "categories.txt": {
        "start_marker": "The Categories",
        "start_offset": "Section 1",
        "end_marker": "END OF THE PROJECT GUTENBERG EBOOK"
    }
}

def clean_file(filepath, config):
    print(f"Cleaning {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start_idx = 0
    end_idx = len(lines)

    # 1. Find Start
    found_start = False

    for i, line in enumerate(lines):
        # Loose check for start marker
        if config["start_marker"] in line:
             # Look for offset in next 2000 lines (increased range)
             sub_search_limit = min(i + 2000, len(lines))
             for j in range(i, sub_search_limit):
                 stripped = lines[j].strip()
                 # Exact match for short offsets
                 if config["start_offset"] == stripped:
                      start_idx = j
                      found_start = True
                      break
                 # Substring match for longer offsets
                 if len(config["start_offset"]) > 5 and config["start_offset"] in lines[j]:
                      start_idx = j
                      found_start = True
                      break
             if found_start:
                 break

    # Fallback for Poetics if exact 'I' match fails or visual inspection needed
    if not found_start and "poetics.txt" in filepath:
        # Hardcode fallback for Poetics if logic failed
        for i, line in enumerate(lines):
             if "ARISTOTLE'S POETICS" in line:
                 start_idx = i + 5 # Skip a few lines
                 found_start = True
                 break

    if not found_start:
        print(f"Warning: Start marker not found for {filepath}. Using beginning of file.")

    # 2. Find End
    for i in range(len(lines) - 1, 0, -1):
        if config["end_marker"] in lines[i] or "*** END OF THE PROJECT" in lines[i]:
            end_idx = i
            break

    # Slicing
    content = lines[start_idx:end_idx]

    # Save back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(content)
    print(f"Cleaned {filepath}. Lines: {len(content)}")

def main():
    for filename, conf in CONFIG.items():
        filepath = os.path.join(RAW_DIR, filename)
        if os.path.exists(filepath):
            clean_file(filepath, conf)
        else:
            print(f"File {filepath} not found.")

if __name__ == "__main__":
    main()
