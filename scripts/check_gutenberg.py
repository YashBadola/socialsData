import requests

ids = [4116, 15489, 14969, 35528, 66048]

for id in ids:
    url = f"https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt"
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            content = response.iter_content(chunk_size=1024)
            first_chunk = next(content).decode('utf-8', errors='ignore')
            print(f"ID {id}: Found. First 100 chars: {first_chunk[:100]}")
            # Try to find title
            for line in first_chunk.split('\n')[:20]:
                if "Title:" in line:
                    print(f"  Title: {line.strip()}")
        else:
            print(f"ID {id}: Not found (status {response.status_code})")
    except Exception as e:
        print(f"ID {id}: Error {e}")
