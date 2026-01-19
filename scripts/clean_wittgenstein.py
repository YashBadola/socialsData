import sys
import re
import os

def clean_latex_text(text):
    # Remove LaTeX comments
    # Remove from % to end of line
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        if '%' in line:
            # Check if % is escaped
            idx = line.find('%')
            if idx > 0 and line[idx-1] == '\\':
                pass # It's \%
            else:
                line = line[:idx]
        cleaned_lines.append(line)
    text = '\n'.join(cleaned_lines)

    # Remove footnotes
    while "\\footnote" in text:
        start = text.find("\\footnote")
        if start == -1: break
        # Find the opening brace
        brace_start = text.find("{", start)
        if brace_start == -1: break

        # Find the matching closing brace
        count = 1
        i = brace_start + 1
        while i < len(text) and count > 0:
            if text[i] == '{':
                count += 1
            elif text[i] == '}':
                count -= 1
            i += 1

        if count == 0:
            text = text[:start] + text[i:]
        else:
            break # Malformed or end of string

    # Replace common commands
    text = text.replace("\\exempliGratia", "e.g.")
    text = text.replace("\\idEst", "i.e.")
    text = text.replace("\\&", "&")
    text = text.replace("\\%", "%")

    # Specific commands to strip (keep content)
    # We simply remove the command part and the surrounding braces if we can identify them clearly.
    # A simple regex approach for non-nested:
    commands_to_strip = ["emph", "textit", "textsc", "PropERef", "BookTitle", "stretchyspace"]

    # Loop to handle nested simple cases
    for _ in range(3): # Repeated passes
        for cmd in commands_to_strip:
            pattern = r"\\" + cmd + r"\s*\{([^{}]*)\}"
            text = re.sub(pattern, r"\1", text)

    # Commands to remove completely (including content if it's an argument, or just the command)
    # \enlargethispage{...} -> remove
    # \Illustration[...]{...} -> remove

    # Simple regex for removing commands with braces
    text = re.sub(r'\\enlargethispage\{[^{}]*\}', '', text)

    # Illustration might have optional args []
    text = re.sub(r'\\Illustration(?:\[[^\]]*\])?\{[^{}]*\}', '', text)

    # \phantomsection, \label, \PropGRef -> These seem to be inside comments or handled?
    # I saw \phantomsection in the grep output earlier but that was likely the definition line I skipped.

    # Handle \ldots
    text = text.replace("\\ldots", "...")

    # Remove remaining latex commands roughly?
    # Maybe replace `\ ` with ` `
    text = text.replace("\\ ", " ")

    # Remove newline chars that might be inside the text
    text = text.replace("\n", " ")

    # Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

def parse_wittgenstein(input_path, output_path):
    # Try reading with ISO-8859-1 as stated in the file header
    try:
        with open(input_path, 'r', encoding='ISO-8859-1') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    propositions = []

    pos = 0
    while True:
        pos = content.find("\\PropositionE", pos)
        if pos == -1:
            break

        # Found \PropositionE
        # Expect {number}
        brace1_start = content.find("{", pos)
        if brace1_start == -1:
            pos += 1
            continue

        # Extract number
        i = brace1_start + 1
        count = 1
        while i < len(content) and count > 0:
            if content[i] == '{': count += 1
            elif content[i] == '}': count -= 1
            i += 1

        if count != 0:
            pos += 1
            continue

        number_str = content[brace1_start+1 : i-1]

        # Validate number_str is a proposition number (e.g., 1, 1.1, 2.0122)
        if not re.match(r'^[\d\.]+$', number_str):
            pos += 1
            continue

        # Expect {text}
        brace2_start = content.find("{", i)
        # There might be whitespace between } and {
        # Check if there is only whitespace
        intervening = content[i:brace2_start]
        if not intervening.strip() == "":
             # Maybe something else?
             pass

        if brace2_start == -1:
            pos += 1
            continue

        # Extract text
        j = brace2_start + 1
        count = 1
        while j < len(content) and count > 0:
            if content[j] == '{': count += 1
            elif content[j] == '}': count -= 1
            j += 1

        if count != 0:
            pos += 1
            continue

        text_content = content[brace2_start+1 : j-1]

        # Clean the text
        clean_text = clean_latex_text(text_content)

        propositions.append(f"{number_str} {clean_text}")

        pos = j

    with open(output_path, 'w', encoding='utf-8') as f:
        for prop in propositions:
            f.write(prop + "\n")

    print(f"Extracted {len(propositions)} propositions to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scripts/clean_wittgenstein.py <input_tex_path> <output_txt_path>")
        sys.exit(1)

    parse_wittgenstein(sys.argv[1], sys.argv[2])
