import re

def strip_headers(text):
    """
    Strips the standard Project Gutenberg headers and footers from the text.
    """
    lines = text.splitlines()
    start_idx = 0
    end_idx = len(lines)

    # Standard Gutenberg markers
    start_markers = [
        "START OF THE PROJECT GUTENBERG EBOOK",
        "START OF THIS PROJECT GUTENBERG EBOOK",
        "*** START OF THIS PROJECT GUTENBERG EBOOK",
        "***START OF THE PROJECT GUTENBERG EBOOK",
    ]

    end_markers = [
        "END OF THE PROJECT GUTENBERG EBOOK",
        "END OF THIS PROJECT GUTENBERG EBOOK",
        "*** END OF THIS PROJECT GUTENBERG EBOOK",
        "***END OF THE PROJECT GUTENBERG EBOOK",
    ]

    # Find start
    for i, line in enumerate(lines):
        if any(marker in line for marker in start_markers):
            start_idx = i + 1
            break

    # Find end (search from bottom up)
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i]
        if any(marker in line for marker in end_markers):
            end_idx = i
            break

    if start_idx == 0 and end_idx == len(lines):
        # Fallback for some texts that have different markers or if it failed
        # Just return mostly as is, maybe trimming empty start/end
        pass

    # Some texts have a preamble after the START marker (like 'Produced by ...')
    # We can try to skip a bit more if we see empty lines or metadata.
    # But usually the START marker is good enough for a rough cut.

    return "\n".join(lines[start_idx:end_idx]).strip()

def clean_file(input_path, output_path=None):
    if output_path is None:
        output_path = input_path

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    cleaned = strip_headers(content)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned)

    print(f"Cleaned {input_path} -> {output_path}")
