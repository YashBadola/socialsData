import urllib.request
import re
import html
import os

URLS = {
    "letter_1.txt": "https://www.lettersfromastoic.net/letter-1/",
    "letter_7.txt": "https://www.lettersfromastoic.net/letter-7-on-crowds/",
    "letter_13.txt": "https://www.lettersfromastoic.net/letter-13-on-groundless-fears/"
}

OUTPUT_DIR = "socials_data/personalities/seneca/raw"

def clean_text(text):
    # Decode HTML entities
    text = html.unescape(text)

    # Remove script and style tags
    text = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.DOTALL)
    text = re.sub(r'<style.*?>.*?</style>', '', text, flags=re.DOTALL)

    # Remove tags
    text = re.sub(r'<[^>]+>', '', text)

    # Remove whitespace
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    text = "\n".join(lines)

    # Specific cleanup for the site artifacts
    clean_lines = []
    skip = False
    for line in text.splitlines():
        # Normalize non-breaking spaces
        line = line.replace('\xa0', ' ')

        # Heuristics to skip navigation/podcast info
        if "Podcast:" in line: continue
        if "Subscribe:" in line: continue
        if "PowerPress" in line: continue
        if "Play in new window" in line: continue
        if "Seneca, Lucius Annaeus" in line and len(line) < 50: continue
        if "By Lucius Annaeus Seneca" in line: continue

        # Stop at footer
        if line == "Related" or line == "About Seneca, Lucius Annaeus":
            break

        clean_lines.append(line)

    return "\n".join(clean_lines)

def extract_content(html_content):
    # Find entry-content
    # The class might vary slightly but usually includes entry-content
    start_marker = 'class="entry-content"'
    end_marker = 'id=\'jp-relatedposts\''

    start_idx = html_content.find(start_marker)
    if start_idx == -1:
        # Try finding the first h6 heading which usually starts the article "By Lucius..."
        start_idx = html_content.find('<h6 class="wp-block-heading">')

    if start_idx == -1:
        return None

    end_idx = html_content.find(end_marker, start_idx)

    if end_idx == -1:
        # Fallback to footer
        end_idx = html_content.find('<footer', start_idx)

    if end_idx == -1:
        content = html_content[start_idx:]
    else:
        # We found the ID inside a tag. We want the start of that tag.
        # Scan backwards from end_idx to find '<'
        tag_start = html_content.rfind('<', start_idx, end_idx)
        if tag_start != -1:
            content = html_content[start_idx:tag_start]
        else:
            content = html_content[start_idx:end_idx]

    return content

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for filename, url in URLS.items():
        print(f"Fetching {url}...")
        try:
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5'
                }
            )
            with urllib.request.urlopen(req) as response:
                html_content = response.read().decode('utf-8')

            content = extract_content(html_content)
            if content:
                text = clean_text(content)

                filepath = os.path.join(OUTPUT_DIR, filename)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"Saved to {filepath}")
            else:
                print(f"Could not extract content from {url}")

        except Exception as e:
            print(f"Error fetching {url}: {e}")

if __name__ == "__main__":
    main()
