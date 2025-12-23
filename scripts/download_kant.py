import requests
import re
import os

# Define the sources for Immanuel Kant's works
sources = [
    {
        "title": "Critique of Pure Reason",
        "url": "https://www.gutenberg.org/cache/epub/4280/pg4280.txt",
        "filename": "critique_of_pure_reason.txt",
        "start_marker": r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK THE CRITIQUE OF PURE REASON \*\*\*",
        "end_marker": r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK THE CRITIQUE OF PURE REASON \*\*\*",
        "text_start_marker": "The Critique of Pure Reason" # Just the title
    },
    {
        "title": "The Critique of Practical Reason",
        "url": "https://www.gutenberg.org/cache/epub/5683/pg5683.txt",
        "filename": "critique_of_practical_reason.txt",
        "start_marker": r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK THE CRITIQUE OF PRACTICAL REASON \*\*\*",
        "end_marker": r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK THE CRITIQUE OF PRACTICAL REASON \*\*\*",
        "text_start_marker": "THE CRITIQUE OF PRACTICAL REASON"
    },
    {
        "title": "Fundamental Principles of the Metaphysic of Morals",
        "url": "https://www.gutenberg.org/cache/epub/5682/pg5682.txt",
        "filename": "fundamental_principles_of_the_metaphysic_of_morals.txt",
        "start_marker": r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK FUNDAMENTAL PRINCIPLES OF THE METAPHYSIC OF MORALS \*\*\*",
        "end_marker": r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK FUNDAMENTAL PRINCIPLES OF THE METAPHYSIC OF MORALS \*\*\*",
        "text_start_marker": "FUNDAMENTAL PRINCIPLES OF THE METAPHYSIC OF MORALS"
    }
]

output_dir = "socials_data/personalities/immanuel_kant/raw"
os.makedirs(output_dir, exist_ok=True)

def download_and_clean(source):
    print(f"Processing {source['title']}...")
    try:
        response = requests.get(source['url'])
        response.raise_for_status()
        content = response.text

        # Check markers roughly to see if they exist
        if not re.search(source['start_marker'], content, re.IGNORECASE):
             print(f"Warning: Start marker not found for {source['title']}.")

        # Extract text between markers
        pattern = f"({source['start_marker']})(.*?)({source['end_marker']})"
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)

        if match:
            clean_text = match.group(2).strip()

            # Refine start if text_start_marker is provided
            if "text_start_marker" in source:
                start_index = clean_text.find(source["text_start_marker"])
                if start_index != -1:
                    clean_text = clean_text[start_index:]
                    print(f"Refined start to '{source['text_start_marker']}'")
                else:
                    print(f"Warning: text_start_marker '{source['text_start_marker']}' not found.")

            output_path = os.path.join(output_dir, source['filename'])
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(clean_text)
            print(f"Saved to {output_path}")

            print("First 200 chars:")
            print(clean_text[:200])
            print("Last 200 chars:")
            print(clean_text[-200:])

        else:
            print(f"Error: Could not extract text for {source['title']} using markers.")

    except Exception as e:
        print(f"Failed to process {source['title']}: {e}")

if __name__ == "__main__":
    for source in sources:
        download_and_clean(source)
