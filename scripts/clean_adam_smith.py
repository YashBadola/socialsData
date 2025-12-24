import re
from pathlib import Path

def clean_file(filepath, start_markers, end_markers):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start_idx = 0
    end_idx = len(lines)

    # 1. Find START
    # We look for the FIRST occurrence of any marker in start_markers
    # But we want to ensure we are skipping TOC if needed.
    # The markers I chose are unique enough or positioned after TOC.

    found_start = False
    for i, line in enumerate(lines):
        line_strip = line.strip()
        for marker in start_markers:
            if marker in line_strip: # Using 'in' to be robust
                start_idx = i
                found_start = True
                break
        if found_start:
            break

    if not found_start:
        print(f"Warning: Start marker not found for {filepath}. Using beginning.")
        start_idx = 0 # Fallback

    # 2. Find END
    for i in range(start_idx, len(lines)):
        for marker in end_markers:
            if marker in lines[i]:
                end_idx = i
                found_start = True # reusing flag for end
                break
        if end_idx != len(lines):
            break

    # 3. Write back
    content = "".join(lines[start_idx:end_idx])

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Cleaned {filepath} (lines {start_idx} to {end_idx})")

base_dir = Path("socials_data/personalities/adam_smith/raw")

# Wealth of Nations
# The actual text starts with "INTRODUCTION AND PLAN OF THE WORK." after the TOC.
# The text "The annual labour of every nation" follows it.
# If I use "The annual labour of every nation", I skip the title "INTRODUCTION...".
# But that's acceptable. Or I can use "INTRODUCTION AND PLAN OF THE WORK." and skip the first one.
# But `clean_file` finds the first one.
# So I will use "The annual labour of every nation" which appears only in the text body (likely).
# Let's verify "The annual labour of every nation" isn't in TOC. TOC usually has Chapter titles.
clean_file(base_dir / "wealth_of_nations.txt",
           ["The annual labour of every nation is the fund"],
           ["*** END OF THE PROJECT"])

# Moral Sentiments
# Actual text starts at "Of the PROPRIETY of ACTION." (line 276 approx) or "Of the SENSE of PROPRIETY." (line 284).
# And "How selfish soever man may be supposed" (line 292).
# "How selfish soever man may be supposed" is the first sentence of Chap 1.
# I will use that to be safe.
clean_file(base_dir / "moral_sentiments.txt",
           ["How selfish soever man may be supposed"],
           ["*** END OF THE PROJECT"])

# Essays
# Starts with "BIOGRAPHICAL NOTICE."
clean_file(base_dir / "essays.txt",
           ["BIOGRAPHICAL NOTICE."],
           ["*** END OF THE PROJECT"])
