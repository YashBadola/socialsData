import click
from socials_data.core.manager import PersonalityManager
from socials_data.core.processor import TextDataProcessor
from socials_data.core.db import DatabaseManager
import os
import json
from pathlib import Path

@click.group()
def main():
    """socials-data CLI tool."""
    pass

@main.command()
def list():
    """List all available personalities."""
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    if not personalities:
        click.echo("No personalities found.")
    else:
        for p in personalities:
            click.echo(f"- {p}")

@main.command()
@click.argument("name")
def add(name):
    """Add a new personality."""
    manager = PersonalityManager()
    try:
        pid = manager.create_personality(name)
        click.echo(f"Created personality '{name}' with ID '{pid}'")
    except Exception as e:
        click.echo(f"Error: {e}")

@main.command()
@click.argument("personality_id")
@click.option("--skip-qa", is_flag=True, help="Skip Q&A generation to save costs.")
def process(personality_id, skip_qa):
    """Process raw data for a personality."""
    manager = PersonalityManager()
    # Check if exists
    try:
        manager.get_metadata(personality_id)
    except FileNotFoundError:
        click.echo(f"Error: Personality '{personality_id}' not found.")
        return

    processor = TextDataProcessor()
    # We construct the path manually or ask manager for it.
    # Manager knows the base dir.
    personality_dir = manager.base_dir / personality_id

    click.echo(f"Processing data for {personality_id}...")
    processor.process(personality_dir, skip_qa=skip_qa)
    click.echo(f"Done. Data saved to {personality_dir}/processed/data.jsonl")

    # Check if QA file was created and notify user
    qa_file = personality_dir / "processed" / "qa.jsonl"
    if qa_file.exists() and qa_file.stat().st_size > 0:
        click.echo(f"Done. Q&A data saved to {qa_file}")
    elif not skip_qa and processor.llm_processor.client is None and os.environ.get("OPENAI_API_KEY"):
         # If key is present but client is None, it means import failed.
         click.echo("Warning: OPENAI_API_KEY present but 'openai' package issues prevented Q&A generation.")
    elif not skip_qa and processor.llm_processor.client is None:
         click.echo("Info: No Q&A generated (OPENAI_API_KEY not found).")

@main.command(name="generate-qa")
@click.argument("personality_id")
def generate_qa(personality_id):
    """Generate Q&A pairs for an existing processed dataset."""
    manager = PersonalityManager()
    try:
        manager.get_metadata(personality_id)
    except FileNotFoundError:
        click.echo(f"Error: Personality '{personality_id}' not found.")
        return

    processor = TextDataProcessor()
    personality_dir = manager.base_dir / personality_id

    click.echo(f"Generating Q&A for {personality_id}...")
    processor.generate_qa_only(personality_dir)

@main.command(name="populate-db")
@click.argument("personality_id", required=False)
def populate_db(personality_id):
    """Populate the SQLite database from file system."""
    db = DatabaseManager()
    manager = PersonalityManager()

    if personality_id:
        p_ids = [personality_id]
    else:
        p_ids = manager.list_personalities()

    for p_id in p_ids:
        click.echo(f"Populating {p_id}...")
        try:
            # clear existing data to prevent duplicates
            db.clear_personality_data(p_id)

            p_dir = manager.base_dir / p_id
            metadata_path = p_dir / "metadata.json"

            if not metadata_path.exists():
                click.echo(f"Skipping {p_id}: No metadata.json")
                continue

            with open(metadata_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)

            db.add_personality(
                meta.get('id', p_id),
                meta['name'],
                meta.get('description', ''),
                meta.get('system_prompt', '')
            )

            # Add works
            works_map = {}
            if 'sources' in meta:
                for source in meta['sources']:
                    w_id = db.add_work(
                        meta.get('id', p_id),
                        source.get('title', 'Unknown'),
                        source.get('type', 'unknown'),
                        source.get('url', '')
                    )
                    works_map[source.get('title')] = w_id

            # Add raw data as excerpts
            raw_dir = p_dir / "raw"
            if raw_dir.exists():
                for raw_file in raw_dir.iterdir():
                    if raw_file.is_file() and raw_file.suffix == '.txt':
                        work_title = raw_file.stem.replace("_", " ").title()
                        w_id = db.add_work(
                            meta.get('id', p_id),
                            work_title,
                            "raw_file",
                            ""
                        )

                        try:
                            with open(raw_file, 'r', encoding='utf-8') as f:
                                content = f.read()

                            parts = content.split('\n\n')
                            for part in parts:
                                if part.strip():
                                    db.add_excerpt(w_id, part.strip(), source_filename=raw_file.name)
                        except Exception as e:
                            click.echo(f"Failed to read {raw_file}: {e}")

        except Exception as e:
            click.echo(f"Error processing {p_id}: {e}")

    db.close()
    click.echo("Database population complete.")

if __name__ == "__main__":
    main()
