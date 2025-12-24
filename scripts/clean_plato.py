import os
import re

RAW_DIR = "socials_data/personalities/plato/raw"

def clean_file(filename, start_marker, end_marker):
    filepath = os.path.join(RAW_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # Generic Gutenberg cleanup first (strip license headers/footers)
    # Most have "*** START OF THE PROJECT GUTENBERG..."
    # and "*** END OF THE PROJECT GUTENBERG..."

    # We will use the specific markers passed in, which are tailored to the content start
    # to avoid Jowett's long introductions.

    # But first, let's just make sure we have the full text loaded.

    start_idx = text.find(start_marker)
    if start_idx == -1:
        print(f"Warning: Start marker '{start_marker}' not found in {filename}.")
        # Fallback to standard Gutenberg start if specific one fails,
        # though likely we want the specific one to skip intro.
        start_idx = text.find("*** START OF THE PROJECT GUTENBERG")
        if start_idx != -1:
             # Move past the marker line
             start_idx = text.find("\n", start_idx) + 1

    end_idx = text.find(end_marker)
    if end_idx == -1:
        print(f"Warning: End marker '{end_marker}' not found in {filename}.")
        end_idx = text.find("*** END OF THE PROJECT GUTENBERG")

    if start_idx != -1 and end_idx != -1:
        content = text[start_idx:end_idx].strip()

        # Overwrite with cleaned content
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Cleaned {filename}")
    else:
        print(f"Could not fully clean {filename} due to missing markers.")

# Based on grep analysis:
# The Republic: Content starts around line 8601 "THE REPUBLIC." or "PERSONS OF THE DIALOGUE."
# But wait, there is an "INTRODUCTION AND ANALYSIS" at the beginning.
# The actual dialogue starts later.
# Line 8601 seems to be the start of the actual text after the analysis.
# Let's use "THE REPUBLIC.\n\n\n PERSONS OF THE DIALOGUE." as a marker context?
# Actually, looking at grep output:
# 8601: THE REPUBLIC.
# 8606: PERSONS OF THE DIALOGUE.
# So if we search for "THE REPUBLIC." and find the last occurrence before the end?
# Or just search for the block "PERSONS OF THE DIALOGUE." that appears late in the file?
# 43: PERSONS OF THE DIALOGUE. (In Table of Contents or Intro)
# 8606: PERSONS OF THE DIALOGUE. (Actual start)
# So we can use the second occurrence.

# Symposium:
# 973: SYMPOSIUM
# followed by PERSONS OF THE DIALOGUE.
# Marker: "SYMPOSIUM\n\n\nPERSONS OF THE DIALOGUE" (normalized whitespace)

# Apology:
# 484: APOLOGY
# followed by "How you, O Athenians..."
# Marker: "APOLOGY\n\n\nHow you, O Athenians"

# Phaedo:
# 1374: PHAEDO
# followed by "PERSONS OF THE DIALOGUE:"
# Marker: "PHAEDO\n\n\nPERSONS OF THE DIALOGUE:"

# Let's write the script to handle these specific cleanups.

def clean_plato():
    # The Republic
    # We want to skip the huge Introduction/Analysis.
    # The actual text starts with "THE REPUBLIC." followed closely by "PERSONS OF THE DIALOGUE."
    # But note that "THE REPUBLIC." also appears at the top.
    # We'll search for the specific block of text.

    clean_file("the_republic.txt",
               start_marker="THE REPUBLIC.\n\n\n PERSONS OF THE DIALOGUE.",
               end_marker="*** END OF THE PROJECT GUTENBERG")

    # Symposium
    clean_file("symposium.txt",
               start_marker="SYMPOSIUM\n\n\nPERSONS OF THE DIALOGUE",
               end_marker="*** END OF THE PROJECT GUTENBERG")

    # Apology
    clean_file("apology.txt",
               start_marker="APOLOGY\n\n\nHow you, O Athenians",
               end_marker="*** END OF THE PROJECT GUTENBERG")

    # Phaedo
    clean_file("phaedo.txt",
               start_marker="PHAEDO\n\n\nPERSONS OF THE DIALOGUE:",
               end_marker="*** END OF THE PROJECT GUTENBERG")

if __name__ == "__main__":
    clean_plato()
