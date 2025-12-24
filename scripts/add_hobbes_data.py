import requests
import os

def download_and_clean():
    url = "https://www.gutenberg.org/cache/epub/3207/pg3207.txt"
    print(f"Downloading from {url}...")
    response = requests.get(url)
    response.encoding = 'utf-8-sig'
    text = response.text
    print(f"Downloaded {len(text)} characters.")

    # Start marker
    # The Dedication seems to be the start of the content we want.
    start_marker = "TO MY MOST HONOR’D FRIEND Mr. FRANCIS GODOLPHIN"
    start_idx = text.find(start_marker)

    if start_idx == -1:
        print("Start marker not found! Searching for alternatives...")
        # Debug: print first few lines of potential interest
        # Maybe the apostrophe is different?
        start_marker_alt = "TO MY MOST HONOR"
        start_idx = text.find(start_marker_alt)

    if start_idx == -1:
         print("Still not found. Dumping head for inspection.")
         print(text[:2000])
         return

    print(f"Found start marker at index {start_idx}")

    # End marker
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK LEVIATHAN ***"
    end_idx = text.find(end_marker)

    if end_idx == -1:
        print("Specific end marker not found! Trying generic marker.")
        end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
        end_idx = text.find(end_marker)

    if end_idx == -1:
        print("End marker not found! checking tail.")
        print(text[-2000:])
        return

    print(f"Found end marker at index {end_idx}")

    content = text[start_idx:end_idx]

    # Verify content isn't empty
    if not content.strip():
        print("Warning: Content is empty!")
        return

    # Save
    output_path = "socials_data/personalities/thomas_hobbes/raw/leviathan.txt"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully saved to {output_path}")
    print(f"Content length: {len(content)}")

if __name__ == "__main__":
    download_and_clean()
