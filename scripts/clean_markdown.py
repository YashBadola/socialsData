import sys
import re

def clean_markdown(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Remove YAML frontmatter
    # Matches --- at start of file, content, then ---
    text = re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL)

    # Remove attributes like {.unnumbered} or {#label}
    text = re.sub(r'\{#[^}]+\}', '', text)
    text = re.sub(r'\{\.[^}]+\}', '', text)

    # Simple LaTeX cleanup
    # Replace $n.1$ with n.1
    text = re.sub(r'\$(.*?)\$', r'\1', text)

    # Remove LaTeX footnotes markers if they are annoying, e.g. ^[...]
    # But wait, ^[...] is Pandoc markdown footnote.
    # Let's keep the content inside but remove the brackets and carrot if it makes sense.
    # Actually, let's just leave footnotes as is, they are readable enough.
    # Or maybe convert `^[note]` to `(note)`.
    text = re.sub(r'\^\[(.*?)\]', r'(\1)', text)

    # Strip extra whitespace
    text = text.strip()

    # Save back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"Cleaned {filepath}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/clean_markdown.py <filepath>")
        sys.exit(1)

    clean_markdown(sys.argv[1])
