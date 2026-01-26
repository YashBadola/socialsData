import requests
from bs4 import BeautifulSoup
import re
import os

def main():
    url = "https://wittgensteinproject.org/w/index.php/Tractatus_Logico-Philosophicus_(English)"
    print(f"Fetching {url}...")
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    # The content is usually in a div with id="mw-content-text"
    content_div = soup.find('div', id='mw-content-text')

    if not content_div:
        print("Error: Could not find content div")
        return

    # Extract text, but preserving some structure would be nice.
    # get_text() joins everything.
    # Let's clean the soup first.

    # Remove the table of contents if present
    toc = content_div.find('div', id='toc')
    if toc:
        toc.decompose()

    # Remove edit sections
    for span in content_div.find_all('span', class_='mw-editsection'):
        span.decompose()

    text = content_div.get_text()

    # Clean up

    # Find start
    start_marker = "Dedication"
    try:
        start_index = text.index(start_marker)
        text = text[start_index:]
    except ValueError:
        print("Warning: Start marker 'Dedication' not found")

    # Find end
    end_marker = "Retrieved from"
    try:
        end_index = text.index(end_marker)
        text = text[:end_index]
    except ValueError:
        # Try finding the footnote section start
        try:
             end_index = text.index("1. ↑ The decimal figures")
             text = text[:end_index]
        except ValueError:
             print("Warning: End marker not found")

    # Remove [number] references like [72], [1] etc.
    # Note: The website uses [number] for links.
    text = re.sub(r'\[\d+\]', '', text)

    # Also remove the ↑ arrows often seen in footnotes if any remain
    text = text.replace('↑', '')

    # Remove multiple newlines
    lines = [line.strip() for line in text.splitlines()]
    # Reconstruct with double newlines for paragraphs
    cleaned_text = "\n".join([line for line in lines if line])

    # Add some spacing for readability (optional, but good for raw text)
    # The simple join above might merge everything too much if paragraphs were separated by blank lines.
    # Let's try to be smarter: text.splitlines() might be better.

    # Actually, get_text(separator='\n') is better
    text = content_div.get_text(separator='\n')

    # Re-apply slicing on the new text
    try:
        start_index = text.index(start_marker)
        text = text[start_index:]
    except ValueError:
        pass

    try:
        end_index = text.index(end_marker)
        text = text[:end_index]
    except ValueError:
         try:
             end_index = text.index("1. ↑ The decimal figures")
             text = text[:end_index]
         except ValueError:
             pass

    text = re.sub(r'\[\d+\]', '', text)

    # Remove lines that are just whitespace
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    cleaned_text = "\n\n".join(lines)

    output_path = "socials_data/personalities/ludwig_wittgenstein/raw/tractatus.txt"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)

    print(f"Saved to {output_path} ({len(cleaned_text)} chars)")

if __name__ == "__main__":
    main()
