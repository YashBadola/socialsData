import re
import json
import os

def main():
    input_file = "temp_seneca.txt"
    output_dir = "socials_data/personalities/seneca/raw"
    metadata_file = "socials_data/personalities/seneca/metadata.json"

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Remove Header/Footer
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK SENECA'S MORALS OF A HAPPY LIFE, BENEFITS, ANGER AND CLEMENCY ***"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK SENECA'S MORALS OF A HAPPY LIFE, BENEFITS, ANGER AND CLEMENCY ***"

    if start_marker in content:
        content = content.split(start_marker)[1]
    if end_marker in content:
        content = content.split(end_marker)[0]

    # 2. Split by Books
    books = [
        ("SENECA OF BENEFITS.", "benefits"),
        ("SENECA OF A HAPPY LIFE.", "happy_life"),
        ("SENECA OF ANGER.", "anger"),
        ("SENECA OF CLEMENCY.", "clemency")
    ]

    # We need to sort by occurrence in text to split correctly
    book_indices = []
    for title, slug in books:
        idx = content.find(title)
        if idx != -1:
            book_indices.append((idx, title, slug))

    book_indices.sort()

    # Save General Intro (everything before the first book)
    if book_indices:
        first_idx = book_indices[0][0]
        general_intro = content[:first_idx].strip()
        if general_intro:
             with open(f"{output_dir}/general_intro.txt", "w", encoding="utf-8") as f:
                 f.write(general_intro)

    # Add end of file sentinel
    book_indices.append((len(content), "END", "end"))

    for i in range(len(book_indices) - 1):
        start_idx, title, slug = book_indices[i]
        end_idx, _, _ = book_indices[i+1]

        book_content = content[start_idx:end_idx]

        # 3. Split by Chapters within book
        # Regex for "CHAPTER I.", "CHAPTER II.", etc.
        # Using capturing group to keep the number
        chapters = re.split(r'\nCHAPTER ([IVXLCDM]+)\.?', book_content)

        # chapters[0] is preamble (Title etc)
        preamble = chapters[0].strip()
        if preamble:
             with open(f"{output_dir}/{slug}_intro.txt", "w", encoding="utf-8") as f:
                 f.write(preamble)

        for j in range(1, len(chapters), 2):
            chap_num = chapters[j]
            chap_text = chapters[j+1].strip()

            filename = f"{slug}_chapter_{chap_num}.txt"
            with open(f"{output_dir}/{filename}", "w", encoding="utf-8") as f:
                f.write(chap_text)

    # 4. Update Metadata
    metadata = {
        "name": "Lucius Annaeus Seneca",
        "id": "seneca",
        "description": "Roman Stoic philosopher, statesman, dramatist, and in some works, satirist, from the Silver Age of Latin literature.",
        "system_prompt": "You are Seneca, a Stoic philosopher. Speak with wisdom, gravity, and a focus on virtue, reason, and living in accordance with nature. Offer counsel on how to manage emotions, face adversity, and cultivate a tranquil mind.",
        "sources": [
            {
                "type": "book",
                "title": "Seneca's Morals of a Happy Life, Benefits, Anger and Clemency",
                "url": "https://www.gutenberg.org/ebooks/56075"
            }
        ],
        "license": "Project Gutenberg License"
    }

    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=2)

    print("Seneca preparation complete.")

if __name__ == "__main__":
    main()
