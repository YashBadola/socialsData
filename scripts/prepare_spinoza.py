import os
import shutil
import subprocess
import requests
import sys

def download_file(url, dest_path):
    print(f"Downloading {url} to {dest_path}...")
    try:
        response = requests.get(url, allow_redirects=True, timeout=30)
        response.raise_for_status()
        with open(dest_path, 'wb') as f:
            f.write(response.content)
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        # Try wget as fallback
        try:
            print("Retrying with wget...")
            subprocess.run(["wget", "-O", dest_path, url], check=True)
        except Exception as e2:
            print(f"Failed to download with wget: {e2}")
            return False
    return True

def prepare_spinoza():
    # Base directory
    base_dir = "socials_data/personalities/baruch_spinoza/raw"
    os.makedirs(base_dir, exist_ok=True)

    # Files to download
    # Ethics
    ethics_url = "https://www.gutenberg.org/ebooks/3800.txt.utf-8"
    ethics_path = os.path.join(base_dir, "ethics.txt")
    download_file(ethics_url, ethics_path)

    # On the Improvement of the Understanding
    improvement_url = "https://www.gutenberg.org/ebooks/1016.txt.utf-8"
    improvement_path = os.path.join(base_dir, "improvement_understanding.txt")
    download_file(improvement_url, improvement_path)

    # Theologico-Political Treatise (Parts 1-4)
    # IDs: 989, 990, 991, 992
    tpt_parts = []
    for i, pid in enumerate([989, 990, 991, 992]):
        url = f"https://www.gutenberg.org/ebooks/{pid}.txt.utf-8"
        path = os.path.join(base_dir, f"tpt_part{i+1}.txt")
        if download_file(url, path):
            tpt_parts.append(path)

    # Concatenate TPT parts
    if tpt_parts:
        tpt_full_path = os.path.join(base_dir, "theologico_political_treatise.txt")
        print("Concatenating Theologico-Political Treatise parts...")
        with open(tpt_full_path, 'w', encoding='utf-8') as outfile:
            for part in tpt_parts:
                try:
                    with open(part, 'r', encoding='utf-8') as infile:
                        # We might want to clean each part individually first to avoid internal headers
                        # But for now let's just cat them and rely on smart cleaning or manual check
                        # Actually, concatenating raw files with headers in between is bad for cleaning.
                        # I should clean them *before* concatenating.
                        pass
                except Exception as e:
                    print(f"Error reading {part}: {e}")

        # Let's clean all downloaded files
        from scripts.clean_gutenberg import clean_gutenberg_text

        # Clean Ethics
        if os.path.exists(ethics_path):
            with open(ethics_path, 'r', encoding='utf-8') as f:
                text = f.read()
            cleaned = clean_gutenberg_text(text)
            with open(ethics_path, 'w', encoding='utf-8') as f:
                f.write(cleaned)
            print("Cleaned Ethics")

        # Clean Improvement
        if os.path.exists(improvement_path):
            with open(improvement_path, 'r', encoding='utf-8') as f:
                text = f.read()
            cleaned = clean_gutenberg_text(text)
            with open(improvement_path, 'w', encoding='utf-8') as f:
                f.write(cleaned)
            print("Cleaned Improvement of Understanding")

        # Clean and Concatenate TPT
        tpt_cleaned_content = []
        for part in tpt_parts:
            if os.path.exists(part):
                with open(part, 'r', encoding='utf-8') as f:
                    text = f.read()
                cleaned = clean_gutenberg_text(text)
                tpt_cleaned_content.append(cleaned)
                # Remove the raw part file after processing
                os.remove(part)

        if tpt_cleaned_content:
            with open(tpt_full_path, 'w', encoding='utf-8') as f:
                f.write("\n\n".join(tpt_cleaned_content))
            print("Created cleaned Theologico-Political Treatise")

if __name__ == "__main__":
    prepare_spinoza()
