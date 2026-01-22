import json
import os

def process_beauvoir():
    base_dir = "socials_data/personalities/simone_de_beauvoir"
    raw_path = os.path.join(base_dir, "raw", "knowledge_base.json")
    processed_path = os.path.join(base_dir, "processed", "data.jsonl")

    with open(raw_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    entries = []

    # Process Biography
    bio_text = f"Biography of Simone de Beauvoir:\n\nEarly Life: {data['biography']['early_life']}\n\nCareer: {data['biography']['career']}\n\nLater Years: {data['biography']['later_years']}"
    entries.append({
        "text": bio_text,
        "source": "Wikipedia (structured)",
        "category": "biography"
    })

    # Process Concepts
    for concept in data['concepts']:
        concept_text = f"Philosophical Concept: {concept['name']}\n\nDefinition: {concept['definition']}"
        entries.append({
            "text": concept_text,
            "source": "Wikipedia (structured)",
            "category": "concept",
            "concept_name": concept['name']
        })

    # Process Works
    for work in data['works']:
        work_text = f"Work: {work['title']} ({work['year']})\n\nDescription: {work['description']}"
        entries.append({
            "text": work_text,
            "source": "Wikipedia (structured)",
            "category": "work",
            "work_title": work['title'],
            "year": work['year']
        })

    # Process Quotes
    for quote in data['quotes']:
        quote_text = f"Quote by Simone de Beauvoir:\n\n\"{quote}\""
        entries.append({
            "text": quote_text,
            "source": "Wikipedia (structured)",
            "category": "quote"
        })

    # Write to JSONL
    with open(processed_path, 'w', encoding='utf-8') as f:
        for entry in entries:
            f.write(json.dumps(entry) + '\n')

    print(f"Successfully wrote {len(entries)} entries to {processed_path}")

if __name__ == "__main__":
    process_beauvoir()
