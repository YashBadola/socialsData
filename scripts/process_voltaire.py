import re
import os

def process_candide():
    input_file = "candide_full.txt"
    output_dir = "socials_data/personalities/voltaire/raw"

    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Remove header
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK CANDIDE ***"
    start_pos = text.find(start_marker)
    if start_pos != -1:
        text = text[start_pos + len(start_marker):]

    # Remove footer
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK CANDIDE ***"
    end_pos = text.find(end_marker)
    if end_pos != -1:
        text = text[:end_pos]

    # Find the start of the first chapter
    # Looking for "I" followed by "HOW CANDIDE"
    # But there is a table of contents before.
    # The TOC has "I. How Candide..."
    # The chapter title is:
    # I
    #
    # HOW CANDIDE WAS BROUGHT UP...

    # Let's find the first chapter.
    # We can split by Roman numerals on their own line.

    chapters = re.split(r'\n\s*([IVXL]+)\n', text)

    # The first element is the preamble/introduction/TOC
    preamble = chapters[0]

    # Saving preamble (Introduction) as well, it might be useful or I can discard it.
    # The introduction by Philip Littell is not by Voltaire.
    # I should try to detect where the actual book starts.
    # The book starts after "CANDIDE" and then "I".

    # Let's iterate and save chapters.
    # chapters[1] is "I", chapters[2] is the content of I.
    # chapters[3] is "II", chapters[4] is the content of II.

    count = 0
    if len(chapters) > 1:
        # We start from index 1.
        for i in range(1, len(chapters), 2):
            chap_num = chapters[i].strip()
            chap_content = chapters[i+1]

            # Check if this is really a chapter.
            # The Introduction might have Roman numerals? No, typically not like this.
            # However, the TOC has lines like "I. How Candide..." which might not be split if I strictly match `\n[IVX]+\n`.
            # My regex `\n\s*([IVXL]+)\n` matches a line containing only Roman numerals.

            filename = f"candide_chap{count+1:02d}.txt"
            filepath = os.path.join(output_dir, filename)

            # Clean up content
            chap_content = chap_content.strip()

            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Chapter {chap_num}\n\n{chap_content}")

            print(f"Saved {filepath}")
            count += 1

    print(f"Total chapters processed: {count}")

if __name__ == "__main__":
    process_candide()
