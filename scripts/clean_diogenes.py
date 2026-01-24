import re

def clean_text(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Generic cleaner for the link blocks
    # They look like [stuff]-[stuff] or [stuff]

    # First, handle the coupled blocks [..]-[..] to remove the hyphen too
    # Pattern: [content]-[content]
    # We allow newlines inside [] via DOTALL
    text = re.sub(r'\[[^\]]*\]-\[[^\]]*\]', '', text, flags=re.DOTALL)

    # Now remove any remaining square bracket blocks
    text = re.sub(r'\[[^\]]*\]', '', text, flags=re.DOTALL)

    # Remove " p23 " page numbers
    text = re.sub(r'\s+p\d+\s+', ' ', text)

    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            cleaned_lines.append("")
            continue

        if line.startswith("(Vol. II)") or line.startswith("Book VI") or "Chapter 2" in line:
            continue
        if line.startswith("Lives of the Eminent Philosophers"):
            continue
        if line == "Diogenes (404‑323 B.C.)":
            continue
        if "link to original Greek text" in line: # partial match fallback
            continue

        cleaned_lines.append(line)

    text = "\n".join(cleaned_lines)

    paragraphs = re.split(r'\n\s*\n', text)
    final_paragraphs = []

    for p in paragraphs:
        p_clean = p.replace('\n', ' ')
        p_clean = re.sub(r'\s+', ' ', p_clean).strip()
        if p_clean:
            final_paragraphs.append(p_clean)

    final_text = "\n\n".join(final_paragraphs)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_text)

if __name__ == "__main__":
    clean_text("diogenes_raw_scraped.txt", "socials_data/personalities/diogenes_of_sinope/raw/diogenes_laertius_book_vi.txt")
