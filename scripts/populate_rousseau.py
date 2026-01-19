import os
import re
import requests

def clean_gutenberg_text(content):
    # Patterns to identify start and end of Gutenberg text
    start_patterns = [
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* START OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
    ]
    end_patterns = [
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* END OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
    ]

    start_idx = 0
    for pattern in start_patterns:
        match = re.search(pattern, content)
        if match:
            start_idx = match.end()
            break

    end_idx = len(content)
    for pattern in end_patterns:
        match = re.search(pattern, content)
        if match:
            end_idx = match.start()
            break

    # Clean text
    text = content[start_idx:end_idx].strip()
    return text

def populate():
    base_dir = "socials_data/personalities/jean_jacques_rousseau/raw"
    os.makedirs(base_dir, exist_ok=True)

    sources = [
        {
            "title": "The Social Contract",
            "url": "https://www.gutenberg.org/cache/epub/46333/pg46333.txt",
            "filename": "the_social_contract.txt"
        },
        {
            "title": "Confessions",
            "url": "https://www.gutenberg.org/cache/epub/3913/pg3913.txt",
            "filename": "confessions.txt"
        },
        {
            "title": "Emile",
            "url": "https://www.gutenberg.org/cache/epub/5427/pg5427.txt",
            "filename": "emile.txt"
        }
    ]

    for source in sources:
        print(f"Downloading {source['title']}...")
        try:
            response = requests.get(source['url'])
            response.raise_for_status()
            # Handle potential encoding issues, usually Gutenberg uses UTF-8 but sometimes ISO-8859-1
            response.encoding = 'utf-8'
            content = response.text

            print(f"Cleaning {source['title']}...")
            cleaned_text = clean_gutenberg_text(content)

            filepath = os.path.join(base_dir, source['filename'])
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(cleaned_text)

            print(f"Saved to {filepath}")

        except Exception as e:
            print(f"Failed to process {source['title']}: {e}")

if __name__ == "__main__":
    populate()
