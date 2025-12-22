import re
from pathlib import Path

def clean_gutenberg_text(text):
    # Standardize line endings
    text = text.replace('\r\n', '\n')

    # Remove Gutenberg Header
    # Look for "START OF THE PROJECT GUTENBERG EBOOK" or similar
    header_pattern = r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .*? \*\*\*"
    match = re.search(header_pattern, text, re.IGNORECASE)
    if match:
        text = text[match.end():]

    # Remove Gutenberg Footer
    # Look for "END OF THE PROJECT GUTENBERG EBOOK"
    footer_pattern = r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK .*? \*\*\*"
    match = re.search(footer_pattern, text, re.IGNORECASE)
    if match:
        text = text[:match.start()]

    # Remove common translator intros (Specific to Meiklejohn/Kant if identifiable, but generic clean is safer for now)
    # Often there is a long intro. For Critique of Pure Reason, actual text starts often after a Preface.
    # But doing this programmatically without risk of cutting content is hard.
    # Gutenberg texts often have "Produced by..." at the start which the header cut handles.

    return text.strip()

def main():
    base_dir = Path("socials_data/personalities/immanuel_kant/raw")
    files = list(base_dir.glob("*.txt"))

    for file_path in files:
        print(f"Cleaning {file_path}...")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            cleaned_content = clean_gutenberg_text(content)

            # Write back to the same file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)

            print(f"Cleaned {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    main()
