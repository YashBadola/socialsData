import requests
import os

# IDs to download
# 66048: Interpretation of Dreams
# 15489: Dream Psychology
# 14969: Three Contributions to the Theory of Sex
# 67332: Psychopathology of Everyday Life
ids = {
    66048: "the_interpretation_of_dreams.txt",
    15489: "dream_psychology.txt",
    14969: "three_contributions_theory_of_sex.txt",
    67332: "psychopathology_of_everyday_life.txt"
}

output_dir = "socials_data/personalities/sigmund_freud/raw/"

for id, filename in ids.items():
    url = f"https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt"
    filepath = os.path.join(output_dir, filename)
    print(f"Downloading {filename} from {url}...")

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {filename}.")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
