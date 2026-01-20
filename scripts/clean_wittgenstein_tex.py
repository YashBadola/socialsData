import sys
import re
import os

def remove_balanced_command(text, command_name):
    """
    Removes \command{...} blocks handling nested braces.
    """
    while True:
        pattern = r'\\' + re.escape(command_name) + r'\s*\{'
        match = re.search(pattern, text)
        if not match:
            break

        start_idx = match.start()
        open_brace_idx = match.end() - 1

        brace_count = 0
        end_idx = -1

        for i in range(open_brace_idx, len(text)):
            if text[i] == '{':
                brace_count += 1
            elif text[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_idx = i
                    break

        if end_idx != -1:
            text = text[:start_idx] + text[end_idx+1:]
        else:
            break

    return text

def clean_latex_text(text):
    # Remove comments (content from % to end of line)
    # Be careful not to remove \% which is a literal percent
    # But for this text it seems unlikely to have \%.
    text = re.sub(r'(?<!\\)%.*', '', text)

    # Remove footnotes properly
    text = remove_balanced_command(text, "footnote")

    # Replace \emph{...} with *...*
    text = re.sub(r'\\emph\{(.*?)\}', r'*\1*', text)
    text = re.sub(r'\\textit\{(.*?)\}', r'*\1*', text)
    text = re.sub(r'\\textbf\{(.*?)\}', r'**\1**', text)

    # Remove labels
    text = re.sub(r'\\label\{.*?\}', '', text)

    # Remove \vspace{...}
    text = re.sub(r'\\vspace\{.*?\}', '', text)

    # Remove commands without arguments but with trailing space like \idEst\
    # Or just \idEst
    # The backslash after the command (e.g. \idEst\ ) escapes the space?
    # In LaTeX, `\command\` is not standard unless `\` is a command (like `\ `).
    # `\idEst\` usually means `\idEst` then a space.
    # So we should match `\command` and remove it.

    # Remove all words starting with backslash
    text = re.sub(r'\\[a-zA-Z]+', '', text)

    # Remove explicit backslash space `\ ` if any, or just single backslashes
    text = text.replace('\\ ', ' ')
    text = text.replace('\\', '')

    # Collapse whitespace
    text = ' '.join(text.split())
    return text

def extract_propositions(filepath, output_path):
    with open(filepath, 'r', encoding='iso-8859-1') as f:
        content = f.read()

    propositions = []

    parts = content.split('\\PropositionE')

    for part in parts[1:]:
        idx = 0
        while idx < len(part) and part[idx].isspace():
            idx += 1

        if idx < len(part) and part[idx] == '{':
            brace_count = 0
            num_start = idx
            num_end = -1
            for i in range(num_start, len(part)):
                if part[i] == '{':
                    brace_count += 1
                elif part[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        num_end = i
                        break

            if num_end != -1:
                num = part[num_start+1 : num_end]

                idx = num_end + 1
                while idx < len(part) and part[idx].isspace():
                    idx += 1

                if idx < len(part) and part[idx] == '{':
                    text_start = idx
                    text_end = -1
                    brace_count = 0
                    for i in range(text_start, len(part)):
                        if part[i] == '{':
                            brace_count += 1
                        elif part[i] == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                text_end = i
                                break

                    if text_end != -1:
                        raw_text = part[text_start+1 : text_end]
                        clean_text = clean_latex_text(raw_text)
                        propositions.append(f"{num} {clean_text}")

    with open(output_path, 'w', encoding='utf-8') as f:
        for p in propositions:
            f.write(p + "\n\n")

    print(f"Extracted {len(propositions)} propositions to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scripts/clean_wittgenstein_tex.py <input_tex> <output_txt>")
        sys.exit(1)

    extract_propositions(sys.argv[1], sys.argv[2])
