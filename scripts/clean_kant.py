import os
import re

PERSONALITY_DIR = "socials_data/personalities/immanuel_kant/raw"

# Define start and end markers for each file
MARKERS = {
    "critique_of_pure_reason.txt": {
        "start": "PREFACE TO THE FIRST EDITION 1781",
        "end": "End of Project Gutenberg's The Critique of Pure Reason"
    },
    "critique_of_practical_reason.txt": {
        "start": "PREFACE.",
        "end": "End of Project Gutenberg's The Critique of Practical Reason"
    },
    "critique_of_judgement.txt": {
        "start": "PREFACE",
        "end": "End of Project Gutenberg's Kant's Critique of Judgement"
    },
    "metaphysic_of_morals.txt": {
        "start": "PREFACE",
        "end": "End of the Project Gutenberg EBook of Fundamental Principles of the Metaphysic"
    },
    "prolegomena.txt": {
        "start": "INTRODUCTION.",
        "end": "End of the Project Gutenberg EBook of Kant's Prolegomena"
    }
}

def clean_file(filename, markers):
    filepath = os.path.join(PERSONALITY_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    start_marker = markers["start"]
    end_marker = markers["end"]

    # Try to find markers
    start_idx = content.find(start_marker)
    if start_idx == -1:
        # Fallback to standard Gutenberg start if specific not found
        start_idx = content.find("*** START OF THIS PROJECT GUTENBERG EBOOK")
        if start_idx == -1:
             start_idx = content.find("*** START OF THE PROJECT GUTENBERG EBOOK")

        if start_idx != -1:
            # Move past the marker line
            newline_idx = content.find('\n', start_idx)
            start_idx = newline_idx + 1
        else:
            print(f"Warning: Start marker not found for {filename}")
            start_idx = 0

    else:
        # Keep the start marker (often it's a chapter title)
        pass

    end_idx = content.find(end_marker)
    if end_idx == -1:
        # Fallback to standard Gutenberg end
        end_idx = content.find("*** END OF THIS PROJECT GUTENBERG EBOOK")
        if end_idx == -1:
             end_idx = content.find("*** END OF THE PROJECT GUTENBERG EBOOK")

        if end_idx == -1:
             print(f"Warning: End marker not found for {filename}")
             end_idx = len(content)

    cleaned_content = content[start_idx:end_idx].strip()

    # Remove license text if it slipped in
    if "Project Gutenberg License" in cleaned_content[:1000]:
        print(f"License text detected in {filename}, attempting to trim...")
        # Simple heuristic: look for double newlines after the license block
        # Or just find the start marker again if we fell back to generic start
        pass

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)

    print(f"Cleaned {filename}: {len(content)} -> {len(cleaned_content)} chars")

if __name__ == "__main__":
    for filename, markers in MARKERS.items():
        clean_file(filename, markers)
