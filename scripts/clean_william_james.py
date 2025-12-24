import os
import re

def clean_text(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start_idx = 0
    end_idx = len(lines)

    # Find start and end markers
    for i, line in enumerate(lines):
        if "*** START OF THE PROJECT GUTENBERG EBOOK" in line:
            start_idx = i + 1
        if "*** END OF THE PROJECT GUTENBERG EBOOK" in line:
            end_idx = i
            break

    # Extract content
    content_lines = lines[start_idx:end_idx]

    # Further cleaning:
    # We want to skip the "Produced by", title page, etc., and start at the first Chapter or Preface.
    # We will look for "CHAPTER I" or "PREFACE" or "LECTURE I" or "CHAPTER XVII" (for vol 2).
    # To be safe, we will look for a line starting with "CHAPTER" or "PREFACE" or "LECTURE" followed by a Roman Numeral or just start.

    refined_start_idx = 0
    for i, line in enumerate(content_lines):
        # Check for standard chapter headings
        # Allow Volume 2 to start at Chapter XVII
        if re.match(r'^\s*(PREFACE|CHAPTER [IVXLCDM]+|LECTURE [IVXLCDM]+)', line.strip(), re.IGNORECASE):
             # But wait, the Table of Contents often lists chapters.
             # We want the ACTUAL start of the content.
             # In Gutenberg texts, the TOC usually comes before the text.
             # But identifying the TOC vs the text is hard programmatically without visual cues.
             # However, usually the TOC lines are short or followed by page numbers.
             # Or they are just a list.

             # Let's look at the file content I just cat'ed.
             # It has "CONTENTS." then "CHAPTER XVII." then "SENSATION".
             # This looks like the TOC.
             # The real text probably starts later.
             pass

    # Actually, for the purpose of LLM training data, the Table of Contents is not terrible to include,
    # but ideally we skip it.
    # However, making a robust TOC skipper is hard.
    # The previous script failed because it skipped TOO MUCH (until Chapter XX).
    # The safest bet is to just strip the Gutenberg header/footer and maybe the "Produced by" block.
    # And let the model handle the Title/TOC.

    # Let's try to skip the "Produced by" block.
    # Usually it's the first few lines after the marker.

    # We will just rely on the Gutenberg markers, but skip the first 20 lines if they are empty or contain "Produced by" or "Title:"
    # Actually, let's just stick to the Gutenberg markers. It's better to have a bit of metadata (Title/Author) than to lose chapters.

    cleaned_content = "".join(content_lines)

    # Remove excessive newlines
    cleaned_content = re.sub(r'\n{3,}', '\n\n', cleaned_content)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)

    print(f"Cleaned {input_path} -> {output_path}")

base_raw_dir = "socials_data/personalities/william_james/raw"

files = [
    "principles_psychology_vol1.txt",
    "principles_psychology_vol2.txt",
    "varieties_religious_experience.txt",
    "pragmatism.txt",
    "meaning_of_truth.txt"
]

for filename in files:
    filepath = os.path.join(base_raw_dir, filename)
    if os.path.exists(filepath):
        # Read, clean, write back
        clean_text(filepath, filepath)
