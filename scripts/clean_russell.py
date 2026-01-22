import os
import re

def clean_gutenberg_text(filepath):
    print(f"Cleaning {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    start_idx = 0
    end_idx = len(content)

    filename = os.path.basename(filepath)

    if filename == "problems_of_philosophy.txt":
        # Standard cleaning
        start_match = re.search(r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*", content, re.IGNORECASE)
        if start_match:
            start_idx = start_match.end()
        end_match = re.search(r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*", content, re.IGNORECASE)
        if end_match:
            end_idx = end_match.start()

    elif filename == "analysis_of_mind.txt":
        # Start at Title, ensuring we match the line strictly to avoid the header
        m = re.search(r"^THE ANALYSIS OF MIND\s*$", content, re.MULTILINE)
        if m:
            start_idx = m.start()
        # End at "End of Project Gutenberg's"
        m_end = re.search(r"End of Project Gutenberg's", content)
        if m_end:
            end_idx = m_end.start()

    elif filename == "mysticism_and_logic.txt":
        # Start at Title
        m = re.search(r"^MYSTICISM AND LOGIC AND OTHER ESSAYS\s*$", content, re.MULTILINE)
        if m:
            start_idx = m.start()

        # End before Transcriber's Note at the end
        m_end = re.search(r"Typographical errors corrected in text:", content)
        if m_end:
             # Find the preceding +---- line
             subset = content[:m_end.start()]
             last_plus = subset.rfind("+--")
             if last_plus != -1:
                 end_idx = last_plus

                 # And the stars before that?
                 subset2 = content[:end_idx]
                 last_stars = subset2.rfind("*       *")
                 if last_stars != -1:
                     end_idx = last_stars

    text = content[start_idx:end_idx].strip()

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Cleaned {filepath}")

def main():
    base_dir = "socials_data/personalities/bertrand_russell/raw"
    if not os.path.exists(base_dir):
        print(f"Directory not found: {base_dir}")
        return

    files = os.listdir(base_dir)

    for filename in files:
        if filename.endswith(".txt"):
            filepath = os.path.join(base_dir, filename)
            clean_gutenberg_text(filepath)

if __name__ == "__main__":
    main()
