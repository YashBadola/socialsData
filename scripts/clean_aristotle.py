
import os

def clean_file(filepath, start_marker, end_marker, precise_start=None):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    start_idx = content.find(start_marker)
    if start_idx == -1:
        print(f"Warning: Start marker not found in {filepath}")
        return

    end_idx = content.find(end_marker)
    if end_idx == -1:
        print(f"Warning: End marker not found in {filepath}")
        # Fallback to look for license header if needed, but usually this is reliable
        return

    # Extract the main content
    text = content[start_idx + len(start_marker):end_idx]

    # Precise trimming
    if precise_start:
        p_start_idx = text.find(precise_start)
        if p_start_idx != -1:
            text = text[p_start_idx:]
        else:
             print(f"Warning: Precise start marker '{precise_start}' not found in {filepath}")

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text.strip())
    print(f"Cleaned {filepath}")

def main():
    base_dir = "socials_data/personalities/aristotle/raw"

    # Nicomachean Ethics
    clean_file(
        os.path.join(base_dir, "nicomachean_ethics.txt"),
        "*** START OF THE PROJECT GUTENBERG EBOOK THE ETHICS OF ARISTOTLE ***",
        "*** END OF THE PROJECT GUTENBERG EBOOK THE ETHICS OF ARISTOTLE ***",
        precise_start="BOOK I"
    )

    # Politics
    clean_file(
        os.path.join(base_dir, "politics.txt"),
        "*** START OF THE PROJECT GUTENBERG EBOOK POLITICS: A TREATISE ON GOVERNMENT ***",
        "*** END OF THE PROJECT GUTENBERG EBOOK POLITICS: A TREATISE ON GOVERNMENT ***",
        precise_start="BOOK I"
    )

if __name__ == "__main__":
    main()
