import os
import re

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the start and end markers
    start_match = re.search(r'\*\*\* START OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*', content)
    end_match = re.search(r'\*\*\* END OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*', content)

    if start_match and end_match:
        start_index = start_match.end()
        end_index = end_match.start()
        cleaned_content = content[start_index:end_index].strip()

        # Write the cleaned content back to the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        print(f"Cleaned {filepath}")
    else:
        print(f"Could not find markers in {filepath}")

def main():
    base_dir = 'socials_data/personalities/david_hume/raw'
    files = [
        'treatise_human_nature.txt',
        'enquiry_human_understanding.txt'
    ]

    for filename in files:
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            clean_file(filepath)
        else:
            print(f"File not found: {filepath}")

if __name__ == '__main__':
    main()
