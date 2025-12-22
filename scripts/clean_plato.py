import os

def clean_gutenberg_text(text):
    """
    Removes Project Gutenberg headers and footers.
    """
    lines = text.splitlines()
    start_idx = 0
    end_idx = len(lines)

    # Find start
    for i, line in enumerate(lines):
        if "*** START OF THE PROJECT GUTENBERG EBOOK" in line or "*** START OF THIS PROJECT GUTENBERG EBOOK" in line:
            start_idx = i + 1
            break

    # Find end
    for i, line in enumerate(lines):
        if "*** END OF THE PROJECT GUTENBERG EBOOK" in line or "*** END OF THIS PROJECT GUTENBERG EBOOK" in line:
            end_idx = i
            break

    if start_idx == 0 and end_idx == len(lines):
         # Try slightly different markers just in case, or look for copyright notices
         pass

    # Slice content
    content = lines[start_idx:end_idx]

    # Remove leading/trailing whitespace lines
    cleaned_lines = []
    started = False
    for line in content:
        if line.strip():
            started = True
        if started:
            cleaned_lines.append(line)

    # Trim trailing
    while cleaned_lines and not cleaned_lines[-1].strip():
        cleaned_lines.pop()

    return "\n".join(cleaned_lines)

def process_file(filepath):
    print(f"Cleaning {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    cleaned = clean_gutenberg_text(content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned)
    print(f"Cleaned {filepath} (len: {len(content)} -> {len(cleaned)})")

if __name__ == "__main__":
    base_dir = "socials_data/personalities/plato/raw"
    files = ["republic.txt", "symposium.txt", "phaedo.txt"]

    for filename in files:
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            process_file(filepath)
        else:
            print(f"File not found: {filepath}")
