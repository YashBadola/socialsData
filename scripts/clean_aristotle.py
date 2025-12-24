import os

def clean_file(filepath, start_marker, end_marker):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    start_idx = content.find(start_marker)
    if start_idx == -1:
        print(f"Warning: Start marker '{start_marker}' not found in {filepath}")
        return

    end_idx = content.find(end_marker)
    if end_idx == -1:
        print(f"Warning: End marker '{end_marker}' not found in {filepath}")
        return

    cleaned_content = content[start_idx + len(start_marker):end_idx].strip()

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    print(f"Cleaned {filepath}")

def main():
    base_dir = os.path.join("socials_data", "personalities", "aristotle", "raw")

    # Nicomachean Ethics
    clean_file(
        os.path.join(base_dir, "nicomachean_ethics.txt"),
        "*** START OF THE PROJECT GUTENBERG EBOOK THE ETHICS OF ARISTOTLE ***",
        "*** END OF THE PROJECT GUTENBERG EBOOK THE ETHICS OF ARISTOTLE ***"
    )

    # Politics
    clean_file(
        os.path.join(base_dir, "politics.txt"),
        "*** START OF THE PROJECT GUTENBERG EBOOK POLITICS: A TREATISE ON GOVERNMENT ***",
        "*** END OF THE PROJECT GUTENBERG EBOOK POLITICS: A TREATISE ON GOVERNMENT ***"
    )

    # Poetics
    clean_file(
        os.path.join(base_dir, "poetics.txt"),
        "*** START OF THE PROJECT GUTENBERG EBOOK THE POETICS OF ARISTOTLE ***",
        "*** END OF THE PROJECT GUTENBERG EBOOK THE POETICS OF ARISTOTLE ***"
    )

if __name__ == "__main__":
    main()
