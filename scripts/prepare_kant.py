import requests
import re
import os
from pathlib import Path

def clean_text(text):
    # Remove Gutenberg Header
    # Typically ends with "*** START OF THE PROJECT GUTENBERG EBOOK ... ***"
    start_marker = re.search(r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*", text)
    if start_marker:
        text = text[start_marker.end():]

    # Remove Gutenberg Footer
    # Typically starts with "*** END OF THE PROJECT GUTENBERG EBOOK ... ***"
    end_marker = re.search(r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*", text)
    if end_marker:
        text = text[:end_marker.start()]

    # Additional cleanup for Meiklejohn's translation if needed
    # (e.g. removing the translator's preface if it's not part of the core text,
    # but for now we keep it as it adds context or usually falls before the main text
    # and might be interesting. However, let's look for the actual start of Kant's text)

    # Often there is a "PREFACE" or "INTRODUCTION".
    # Let's try to strip just the boilerplate license text which usually follows the header
    # But the regex above usually handles the main Gutenberg license block.

    return text.strip()

def main():
    url = "https://www.gutenberg.org/cache/epub/4280/pg4280.txt"
    output_dir = Path("socials_data/personalities/immanuel_kant/raw")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "critique_of_pure_reason.txt"

    print(f"Downloading from {url}...")
    response = requests.get(url)
    response.raise_for_status()

    print("Cleaning text...")
    raw_text = response.text
    cleaned_text = clean_text(raw_text)

    print(f"Saving to {output_file}...")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(cleaned_text)

    print("Done.")

if __name__ == "__main__":
    main()
