import os
import re

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Normalize line endings
    content = content.replace('\r\n', '\n')

    # 2. Identify start and end markers
    # Project Gutenberg texts often start with "*** START OF THE PROJECT..."
    # or "Produced by..." if the header is missing/custom.

    start_markers = [
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* START OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"START OF THE PROJECT GUTENBERG EBOOK",
    ]

    end_markers = [
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* END OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"END OF THE PROJECT GUTENBERG EBOOK",
    ]

    start_pos = 0
    end_pos = len(content)

    # Find start
    found_start = False
    for marker in start_markers:
        match = re.search(marker, content, re.IGNORECASE)
        if match:
            start_pos = match.end()
            found_start = True
            break

    if not found_start:
        # Fallback for "ethics.txt" which starts with "Produced by..."
        # We look for the title "The Ethics" or "Theologico-Political Treatise"
        # However, looking for "Produced by" is risky if it appears elsewhere.
        # Let's try to cut off metadata headers.

        # Heuristic: Scan first 200 lines for "Produced by" or "Title:" and skip past them?
        # Better: Look for the first meaningful line.

        # Specific fix for Ethics (starts with "Produced by Tom Sharpe...")
        # We want to keep "The Ethics..."
        match = re.search(r"Produced by .*", content[:500])
        if match:
            # Check if "The Ethics" follows
            ethics_match = re.search(r"The Ethics", content)
            if ethics_match and ethics_match.start() > match.start():
                start_pos = ethics_match.start()
            else:
                 start_pos = match.end()

        # Specific fix for Tractatus (starts with standard header but might have been concatenated)
        # Since we concatenated 4 files, we might have 4 headers and 4 footers.
        # We need to clean EACH PART if we were doing it right, or clean the whole thing aggressively.
        # But wait, I concatenated them into one file. The headers/footers are now embedded in the middle too!
        # This approach of cleaning the single file is tricky if I don't remove internal headers.

        # Strategy: Remove all Gutenberg boilerplate everywhere in the file.
        pass

    # Generic removal of Gutenberg license text blocks if markers fail or for internal blocks
    # This regex attempts to find the standard license intro and removing it.

    # Actually, simpler approach for the concatenated file:
    # Split by standard header/footer markers and keep the middle parts.
    # But for "ethics.txt", it didn't have standard markers.

    # Let's try to just strip the specific "Produced by" header for Ethics.
    if "ethics.txt" in filepath:
        match = re.search(r"Produced by Tom Sharpe.*", content)
        if match and match.start() < 500:
             # Find where the actual text starts. "The Ethics"
             start_match = re.search(r"The Ethics", content)
             if start_match:
                 start_pos = start_match.start()

    # Find end
    for marker in end_markers:
        match = re.search(marker, content, re.IGNORECASE)
        if match:
            end_pos = match.start()
            break # Assume the first "End" is the end of the book?
            # Wait, if we concatenated, we have multiple ends.
            # We want the text content between headers and footers.

    # COMPLEX CASE: concatenated files.
    # If we see multiple headers/footers, we should process them as segments.
    # But 'ethics.txt' is single file. 'tractatus.txt' is concatenated.

    # Let's handle Tractatus specially since we know its structure.
    if "tractatus.txt" in filepath:
        # It has standard markers.
        # We want to keep everything BETWEEN "START OF..." and "END OF..."
        # There are 4 such blocks.

        pattern = r"(\*\*\* START OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*)(.*?)(\*\*\* END OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*)"
        parts = []
        for match in re.finditer(pattern, content, re.DOTALL | re.IGNORECASE):
            parts.append(match.group(2))

        if parts:
            content = "\n\n".join(parts)
            # Reset start/end pos because we just extracted the content
            start_pos = 0
            end_pos = len(content)
        else:
             # Fallback if regex failed (maybe slightly different markers)
             pass

    content = content[start_pos:end_pos]

    # Additional cleanup
    # Remove "Produced by" lines if any remain
    content = re.sub(r"Produced by .*", "", content)

    content = content.strip()

    # Normalize multiple newlines
    content = re.sub(r'\n{3,}', '\n\n', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Cleaned {filepath}")

if __name__ == "__main__":
    base_dir = "socials_data/personalities/baruch_spinoza/raw"
    files = ["ethics.txt", "tractatus.txt"]

    for file in files:
        filepath = os.path.join(base_dir, file)
        if os.path.exists(filepath):
            clean_file(filepath)
        else:
            print(f"File not found: {filepath}")
