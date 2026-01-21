import sys
import re

def clean_tex(text):
    # Remove comments
    text = re.sub(r'%.*', '', text)

    # Replace common TeX commands
    text = re.sub(r'\\emph\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\textit\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\textbf\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\textsc\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\footnote\{([^}]*)\}', '', text)
    text = re.sub(r'\\footnote\{[^}]*\}', '', text)

    # Mathematical/Logical symbols and formatting
    text = text.replace(r'\DotOp', '.')
    text = text.replace(r'\Implies', ' implies ')
    text = text.replace(r'\equiv', ' if and only if ')
    text = text.replace(r'\lor', ' or ')
    text = text.replace(r'\Not', 'not ')
    text = text.replace(r'\exists', 'exists')
    text = text.replace(r'\fourdots', '....')
    text = text.replace(r'\fivedots', '.....')
    text = text.replace(r'\ldots', '...')

    # Remove other commands like \enlargethispage{...}
    text = re.sub(r'\\[a-zA-Z]+(?:\[[^\]]*\])?(?:\{[^}]*\})?', '', text)

    # Remove math mode delimiters $
    text = text.replace('$', '')

    # Remove lingering braces { }
    text = text.replace('{', '').replace('}', '')

    # Clean up multiple spaces and newlines
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_propositions(filepath, output_filepath):
    # Use utf-8 as the file is likely utf-8 despite the header saying ISO-8859-1
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract Preface
    preface_match = re.search(r'\\Preface\{.*?\}\{Preface\}(.*?)\\MainMatter', content, re.DOTALL)
    preface_text = ""
    if preface_match:
        preface_content = preface_match.group(1)
        preface_text = clean_tex(preface_content)

    propositions = []

    # Find all occurrences of \PropositionE
    # We loop manually to handle skipping whitespace

    idx = 0
    while True:
        match = re.search(r'\\PropositionE\{([^}]+)\}', content[idx:])
        if not match:
            break

        num = match.group(1)
        start_idx = idx + match.end()

        # Skip whitespace including newlines
        curr = start_idx
        while curr < len(content) and content[curr].isspace():
            curr += 1

        if curr < len(content) and content[curr] == '{':
            # Parse balanced braces
            brace_count = 1
            i = curr + 1
            while i < len(content) and brace_count > 0:
                if content[i] == '{':
                    brace_count += 1
                elif content[i] == '}':
                    brace_count -= 1
                i += 1

            raw_text = content[curr+1 : i-1]
            clean_text = clean_tex(raw_text)
            propositions.append(f"{num} {clean_text}")

            idx = i
        else:
            # Something is wrong or format is different, skip ahead
            idx = start_idx

    full_text = ""
    if preface_text:
        full_text += "PREFACE\n\n" + preface_text + "\n\n"

    full_text += "TRACTATUS LOGICO-PHILOSOPHICUS\n\n"
    full_text += "\n\n".join(propositions)

    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write(full_text)

    print(f"Extracted {len(propositions)} propositions to {output_filepath}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scripts/clean_wittgenstein.py <input_tex> <output_txt>")
        sys.exit(1)

    extract_propositions(sys.argv[1], sys.argv[2])
