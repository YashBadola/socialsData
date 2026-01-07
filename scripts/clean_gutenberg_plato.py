import os

def clean_gutenberg_text(text):
    """
    Crude but effective cleaner for Gutenberg headers/footers.
    It looks for standard markers.
    """
    lines = text.split('\n')
    start_idx = 0
    end_idx = len(lines)

    # Common start markers
    start_markers = [
        "*** START OF THE PROJECT GUTENBERG EBOOK",
        "*** START OF THIS PROJECT GUTENBERG EBOOK",
        "***START OF THE PROJECT GUTENBERG EBOOK",
    ]

    # Common end markers
    end_markers = [
        "*** END OF THE PROJECT GUTENBERG EBOOK",
        "*** END OF THIS PROJECT GUTENBERG EBOOK",
        "***END OF THE PROJECT GUTENBERG EBOOK",
        "End of the Project Gutenberg EBook",
        "End of Project Gutenberg's",
    ]

    for i, line in enumerate(lines):
        for marker in start_markers:
            if marker in line:
                start_idx = i + 1
                break
        if start_idx > 0:
            break

    for i, line in enumerate(lines):
        for marker in end_markers:
            if marker in line:
                end_idx = i
                break
        if end_idx < len(lines):
            break

    # If we didn't find clear markers, we might just be safer returning original or doing something else.
    # But usually these markers exist.

    if start_idx == 0:
        print("Warning: Start marker not found.")

    if end_idx == len(lines):
        print("Warning: End marker not found.")

    return '\n'.join(lines[start_idx:end_idx]).strip()

def main():
    base_dir = "socials_data/personalities/plato/raw"
    for filename in os.listdir(base_dir):
        filepath = os.path.join(base_dir, filename)
        if not filename.endswith(".txt"):
            continue

        print(f"Cleaning {filename}...")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            cleaned_content = clean_gutenberg_text(content)

            # Simple check to see if we actually removed something
            if len(cleaned_content) < len(content):
                print(f"Reduced size from {len(content)} to {len(cleaned_content)} chars.")
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)
            else:
                print("No content removed (markers not found?).")

        except Exception as e:
            print(f"Error cleaning {filename}: {e}")

if __name__ == "__main__":
    main()
