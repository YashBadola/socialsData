import requests
import re
import os

def clean_hobbes():
    url = "https://www.gutenberg.org/cache/epub/3207/pg3207.txt"
    raw_path = "socials_data/personalities/thomas_hobbes/raw/leviathan.txt"

    print(f"Downloading Leviathan from {url}...")
    response = requests.get(url)
    response.raise_for_status()
    # Use utf-8-sig to handle BOM
    text = response.content.decode('utf-8-sig')

    print("Download complete. Cleaning text...")

    # Identify start and end markers
    # Based on typical Gutenberg markers or specific text inspection
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK LEVIATHAN ***"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK LEVIATHAN ***"

    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker)

    if start_idx == -1:
        # Fallback or try case insensitive
        print("Standard start marker not found. Searching case-insensitive...")
        start_match = re.search(r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*", text, re.IGNORECASE)
        if start_match:
            start_idx = start_match.start()
            start_marker = start_match.group(0)
        else:
            print("Start marker not found! Dumping first 500 chars:")
            print(text[:500])
            raise ValueError("Start marker not found")

    if end_idx == -1:
         print("Standard end marker not found. Searching case-insensitive...")
         end_match = re.search(r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*", text, re.IGNORECASE)
         if end_match:
             end_idx = end_match.start()
         else:
             print("End marker not found!")
             # Maybe we can just go to the end if not found, or raise error
             # raise ValueError("End marker not found")
             # Actually, let's try to be robust. If no end marker, maybe it's fine to just take the rest?
             # But Gutenberg usually has a license footer.
             # Let's look for "END OF THE PROJECT GUTENBERG EBOOK" part
             end_match = re.search(r"END OF THE PROJECT GUTENBERG EBOOK", text, re.IGNORECASE)
             if end_match:
                 end_idx = end_match.start()
             else:
                 raise ValueError("End marker not found")

    # Extract content
    content = text[start_idx + len(start_marker):end_idx]

    # Further cleaning: Remove the intro by the transcriber if present?
    # The snippet showed "TRANSCRIBER'S NOTES ON THE E-TEXT".
    # Let's see if we can find the real start of the text.
    # Usually "LEVIATHAN" or "THE INTRODUCTION".
    # Or "The First Part".

    # Let's look for "THE INTRODUCTION" as a reliable start of the actual content
    real_start = content.find("THE INTRODUCTION")
    if real_start != -1:
        print("Found 'THE INTRODUCTION', trimming preamble...")
        content = content[real_start:]
    else:
        # Maybe "The First Part"
        real_start = content.find("PART I.")
        if real_start != -1:
             print("Found 'PART I.', trimming preamble...")
             # But Introduction is before Part I.
             # If we missed Introduction, maybe we cut too much.
             pass

    # Save
    with open(raw_path, 'w', encoding='utf-8') as f:
        f.write(content.strip())

    print(f"Cleaned text saved to {raw_path}")

if __name__ == "__main__":
    clean_hobbes()
