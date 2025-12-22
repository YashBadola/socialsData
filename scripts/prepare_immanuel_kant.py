import os
import requests

def download_file(url, output_path):
    print(f"Downloading {url} to {output_path}...")
    response = requests.get(url)
    response.raise_for_status()
    with open(output_path, 'wb') as f:
        f.write(response.content)
    print("Done.")

def main():
    base_dir = "socials_data/personalities/immanuel_kant/raw"
    os.makedirs(base_dir, exist_ok=True)

    sources = [
        ("https://www.gutenberg.org/cache/epub/4280/pg4280.txt", "critique_of_pure_reason.txt"),
        ("https://www.gutenberg.org/cache/epub/5683/pg5683.txt", "critique_of_practical_reason.txt")
    ]

    for url, filename in sources:
        filepath = os.path.join(base_dir, filename)
        download_file(url, filepath)

    # Run the cleaner
    try:
        from clean_gutenberg import clean_gutenberg_text

        for _, filename in sources:
            filepath = os.path.join(base_dir, filename)
            print(f"Cleaning {filepath}...")
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            cleaned = clean_gutenberg_text(content)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(cleaned)
            print(f"Cleaned {filepath}")

    except ImportError:
        print("Warning: clean_gutenberg module not found. Files are downloaded but not cleaned.")

if __name__ == "__main__":
    main()
