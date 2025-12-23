import os
import re

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the start of the book content
    # Gutenberg usually has "*** START OF THE PROJECT GUTENBERG EBOOK ..."
    start_match = re.search(r'\*\*\* START OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*', content)
    if start_match:
        content = content[start_match.end():]

    # Find the end of the book content
    # Gutenberg usually has "*** END OF THE PROJECT GUTENBERG EBOOK ..."
    # But sometimes just license stuff at the end.
    # Looking at the tail output, it ends with legalese.
    # A common marker is "END OF THE PROJECT GUTENBERG EBOOK" or just before the license.
    # We can look for the license section.

    end_match = re.search(r'\*\*\* END OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*', content)
    if end_match:
        content = content[:end_match.start()]
    else:
        # Fallback if the explicit end marker isn't found, look for license block start
        # Usually "End of Project Gutenberg's" or "End of the Project Gutenberg"
        # Or look for "Section 1. General Terms of Use" or similar if needed.
        # But often there is "End of the Project Gutenberg EBook..." line.
        # Let's try to find "End of the Project Gutenberg"
        end_match = re.search(r'End of.*?Project Gutenberg', content, re.IGNORECASE)
        if end_match:
             content = content[:end_match.start()]

    # Further cleaning for Plato specifics (Jowett translations often have long intros)

    # For The Republic
    if 'the_republic.txt' in filepath:
        # Jowett's Republic has "INTRODUCTION AND ANALYSIS." and then "THE REPUBLIC."
        # We want to skip the introduction if possible.
        # It seems "BOOK I." is a good start marker for the actual text.
        book_i_match = re.search(r'\nBOOK I\.\s*\n', content)
        if book_i_match:
             content = content[book_i_match.start():]

    # For Symposium
    if 'symposium.txt' in filepath:
        # Has "INTRODUCTION."
        # The dialogue usually starts after the persons list or just starts.
        # Looking at the file, it has "SYMPOSIUM" and then "INTRODUCTION."
        # Jowett's intros are long.
        # Actual text often starts with the dialogue.
        # In Symposium, the dialogue starts with "I believe that I am not ill-prepared..." or "PERSONS OF THE DIALOGUE"
        # Let's check if we can find "PERSONS OF THE DIALOGUE"
        persons_match = re.search(r'PERSONS OF THE DIALOGUE', content)
        if persons_match:
             content = content[persons_match.start():]
        else:
             # If not found, maybe look for the start text "I believe that I am not ill-prepared"
             # But that's specific.
             # Let's try to look for the end of the Introduction.
             pass

    # Trim whitespace
    content = content.strip()

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Cleaned {filepath}")

if __name__ == "__main__":
    clean_file('socials_data/personalities/plato/raw/the_republic.txt')
    clean_file('socials_data/personalities/plato/raw/symposium.txt')
