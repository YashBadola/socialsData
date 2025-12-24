import json
import os
from pathlib import Path

def clean_text(text, start_markers, end_markers):
    """
    Cleans text by removing Gutenberg headers and footers based on markers.
    """
    start_idx = 0
    end_idx = len(text)

    # Find start
    for marker in start_markers:
        idx = text.find(marker)
        if idx != -1:
            # Check if there is another occurrence (sometimes title appears in header)
            # We want the one after the header. But usually the header ends with *** START OF ... ***
            # So if we search for the Title, we might find it early.
            # Best strategy: Find "*** START OF THE PROJECT" first, then search for content start after that.
            gutenberg_start = text.find("*** START OF THE PROJECT")
            if gutenberg_start != -1:
                 idx = text.find(marker, gutenberg_start + len("*** START OF THE PROJECT"))

            if idx != -1:
                start_idx = idx
                break

    # Find end
    for marker in end_markers:
        idx = text.find(marker, start_idx)
        if idx != -1:
            end_idx = idx
            break

    return text[start_idx:end_idx].strip()

def process_rousseau():
    base_dir = Path("socials_data/personalities/jean_jacques_rousseau")
    raw_dir = base_dir / "raw"
    processed_dir = base_dir / "processed"
    processed_dir.mkdir(exist_ok=True)

    output_file = processed_dir / "data.jsonl"

    files_config = [
        {
            "filename": "social_contract_and_discourses.txt",
            "start_markers": ["THE SOCIAL CONTRACT & DISCOURSES\n\nby\n\nJEAN JACQUES ROUSSEAU"], # Specific enough
            # Fallback if exact newline format differs
            "start_markers_backup": ["THE SOCIAL CONTRACT & DISCOURSES"],
            "end_markers": ["*** END OF THE PROJECT GUTENBERG"]
        },
        {
            "filename": "confessions.txt",
            "start_markers": ["THE CONFESSIONS OF JEAN JACQUES ROUSSEAU"],
            "end_markers": ["*** END OF THE PROJECT GUTENBERG"]
        },
        {
            "filename": "emile.txt",
            "start_markers": ["EMILE\n\nBy Jean-Jacques Rousseau"],
            "start_markers_backup": ["EMILE"],
            "end_markers": ["*** END OF THE PROJECT GUTENBERG"]
        }
    ]

    with open(output_file, 'w', encoding='utf-8') as out_f:
        for config in files_config:
            filepath = raw_dir / config["filename"]
            if not filepath.exists():
                print(f"Skipping {config['filename']}, file not found.")
                continue

            print(f"Processing {config['filename']}...")
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Try primary markers
            cleaned_content = clean_text(content, config["start_markers"], config["end_markers"])

            # If that failed to chop off header (start_idx still 0 or close), try backup
            # Actually clean_text returns stripped text. If it contains the header, we failed.
            if "*** START OF THE PROJECT" in cleaned_content and "start_markers_backup" in config:
                 cleaned_content = clean_text(content, config["start_markers_backup"], config["end_markers"])

            # Double check we removed the header
            if "*** START OF THE PROJECT" in cleaned_content:
                 # Fallback: just look for the header end
                 guten_end = content.find("*** START OF THE PROJECT")
                 if guten_end != -1:
                     # Find the end of that line
                     line_end = content.find("\n", guten_end)
                     cleaned_content = content[line_end:].strip()
                     # Also cut footer
                     end_idx = cleaned_content.find("*** END OF THE PROJECT")
                     if end_idx != -1:
                         cleaned_content = cleaned_content[:end_idx].strip()

            # Final sanity check for license
            if "PROJECT GUTENBERG LICENSE" in cleaned_content[-5000:]:
                 # The footer marker might have been missed
                 idx = cleaned_content.find("*** END OF THE PROJECT")
                 if idx != -1:
                     cleaned_content = cleaned_content[:idx].strip()

            # Write to jsonl
            # We can split by paragraphs or keep large chunks.
            # The standard seems to be one entry per file? Or split?
            # Looking at other personalities, it seems they often have one large text or split by reasonable chunks.
            # But the memory says "Raw text chunks go to processed/data.jsonl".
            # Often it is better to chunk it to avoid context window limits later, but the `process` command might handle chunking?
            # Memory says "The `process` command... converts raw text files into the `processed/data.jsonl` format".
            # This implies I am writing the logic for `process`?
            # Wait, the prompt asked me to "develop an elaborate new database".
            # The standard flow is `python -m socials_data.cli process <name>`.
            # That command uses `socials_data.core.processor.DataProcessor`.
            # Does that processor know how to clean?
            # Memory: "The standard `DataProcessor` does not automatically strip Project Gutenberg headers or footers; this must be handled via cleaning scripts before running the `process` command."
            # So I should overwrite the raw files with cleaned versions? Or write directly to processed?
            # Memory: "Cleaning scripts... overwrite raw files in-place cannot be re-run safely... raw files must be re-downloaded".
            # Memory: "Processed data is stored in JSONL format: raw text chunks go to processed/data.jsonl".

            # Let's verify what `clean_rousseau.py` should do.
            # If I write to `processed/data.jsonl` directly, I bypass the `process` CLI command for the initial data creation.
            # But the `process` command also does Q&A generation.
            # If I provide `processed/data.jsonl`, maybe `process` will skip creation and go to QA?
            # Or maybe I should clean the raw files *in place* (or to a `clean/` dir) and then run `process`?
            # Memory says "Cleaning scripts... overwrite raw files in-place...".
            # This suggests the standard practice is to modify the raw files to remove headers, THEN run `process`.

            # Let's adjust: The script will Read raw, Clean, Write back to raw (or a temp raw).
            # Actually, overwriting raw is destructive.
            # If I write to `processed/data.jsonl`, I am doing the job of the `process` command's first step.

            # Let's look at `socials_data/cli.py` or `processor.py` if possible.
            # But based on memory "The `process` command ... converts raw text files into the `processed/data.jsonl`".
            # So `process` takes `raw/*.txt` -> `processed/data.jsonl`.
            # If `raw/*.txt` still has headers, `processed/data.jsonl` will have headers.
            # So I must clean `raw/*.txt`.

            # Revised plan for script: Overwrite `raw/*.txt` with cleaned content.

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            print(f"Cleaned {config['filename']}")

if __name__ == "__main__":
    process_rousseau()
