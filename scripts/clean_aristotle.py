import os
import re

def clean_text(content, start_markers, end_markers):
    """
    Cleans the text by removing content before the start markers and after the end markers.
    """
    start_idx = -1
    for marker in start_markers:
        idx = content.find(marker)
        if idx != -1:
            start_idx = idx
            # If the marker acts as a header we want to keep, we keep it.
            # If we want to skip it, we add len(marker).
            # Here, the markers are like "BOOK I", which is good to keep as a header.
            # But the previous logic was `start_idx = idx + len(marker)`.
            # Let's verify what we want. If marker is "BOOK I", we probably want to start reading FROM "BOOK I".
            break

    if start_idx == -1:
        # Fallback to standard Gutenberg start
        print("Warning: Specific start marker not found. Using standard Gutenberg start.")
        standard_start = "*** START OF THE PROJECT GUTENBERG EBOOK"
        idx = content.find(standard_start)
        if idx != -1:
             # Find the end of this line
             newline_idx = content.find('\n', idx)
             if newline_idx != -1:
                 start_idx = newline_idx + 1
             else:
                 start_idx = idx + len(standard_start)

    if start_idx == -1:
        print("Error: Could not find start of text.")
        return content

    end_idx = -1
    for marker in end_markers:
        idx = content.find(marker)
        if idx != -1:
            end_idx = idx
            break

    if end_idx == -1:
         # Fallback to standard Gutenberg end
        print("Warning: Specific end marker not found. Using standard Gutenberg end.")
        standard_end = "*** END OF THE PROJECT GUTENBERG EBOOK"
        idx = content.find(standard_end)
        if idx != -1:
            end_idx = idx

    if end_idx != -1:
        content = content[start_idx:end_idx]
    else:
        content = content[start_idx:]

    return content.strip()

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # We need to re-download raw files because they were overwritten in place
    # Or, we can just process them again if we are careful, but re-downloading is safer
    # since we might have chopped off the marker we are looking for.
    # To be safe, let's just re-run the download script first.

    raw_dir = os.path.join(base_dir, "socials_data", "personalities", "aristotle", "raw")

    files_to_clean = [
        {
            "filename": "nicomachean_ethics.txt",
            "start_markers": ["ARISTOTLE’S ETHICS\n BOOK I"],
            "end_markers": ["*** END OF THE PROJECT GUTENBERG EBOOK"]
        },
        {
            "filename": "politics.txt",
            "start_markers": ["BOOK I"], # Found via grep
            "end_markers": ["INDEX", "*** END OF THE PROJECT GUTENBERG EBOOK"]
        },
        {
            "filename": "poetics.txt",
            "start_markers": ["ARISTOTLE'S POETICS"],
            "end_markers": ["*** END OF THE PROJECT GUTENBERG EBOOK"]
        }
    ]

    for item in files_to_clean:
        filepath = os.path.join(raw_dir, item["filename"])
        if os.path.exists(filepath):
            print(f"Cleaning {item['filename']}...")
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            cleaned_content = clean_text(content, item["start_markers"], item["end_markers"])

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            print("Done.")
        else:
            print(f"File {item['filename']} not found.")

if __name__ == "__main__":
    main()
