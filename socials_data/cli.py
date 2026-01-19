import click
from socials_data.core.manager import PersonalityManager
from socials_data.core.processor import TextDataProcessor
from socials_data.core.db import SocialsDatabase
import os
import json

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

@main.command(name="sync-db")
def sync_db():
    """Sync file-based datasets into the SQLite database."""
    db = SocialsDatabase()
    db.init_db()

    manager = PersonalityManager()
    personalities = manager.list_personalities()

    click.echo(f"Syncing {len(personalities)} personalities to database...")

    for p_id in personalities:
        try:
            meta = manager.get_metadata(p_id)
            click.echo(f"Syncing {p_id}...")

            # Upsert personality
            db.upsert_personality(
                p_id,
                meta.get("name"),
                meta.get("description"),
                meta.get("system_prompt"),
                meta
            )

            # Clear old content
            db.clear_personality_content(p_id)

            # Sources
            sources_map = {} # title -> id
            for src in meta.get("sources", []):
                s_id = db.add_source(p_id, src.get("title"), src.get("url"), src.get("type"))
                sources_map[src.get("title")] = s_id

            # Processed Data
            processed_file = manager.base_dir / p_id / "processed" / "data.jsonl"
            if processed_file.exists():
                with open(processed_file, "r") as f:
                    for line in f:
                        try:
                            record = json.loads(line)
                            text = record.get("text")
                            source_name = record.get("source") # This might be filename, not title

                            # Try to match source
                            s_id = None
                            # Simple heuristic: if source name is in title or vice versa
                            # Ideally, processed data should link back to source defined in metadata
                            # But currently it just uses filename.
                            # We'll just store it as content without strict source link if not found,
                            # or create a source for the filename.

                            db.add_content(p_id, text, "text", source_id=s_id, meta={"original_source": source_name})
                        except json.JSONDecodeError:
                            pass

            # QA Data
            qa_file = manager.base_dir / p_id / "processed" / "qa.jsonl"
            if qa_file.exists():
                with open(qa_file, "r") as f:
                    for line in f:
                        try:
                            record = json.loads(line)
                            # QA record: instruction, response
                            # We'll store it as a JSON string or combined text?
                            # Let's store as text for searchability: "Q: ... A: ..."
                            text = f"Q: {record.get('instruction')}\nA: {record.get('response')}"
                            db.add_content(p_id, text, "qa", meta=record)
                        except json.JSONDecodeError:
                            pass

        except Exception as e:
            click.echo(f"Error syncing {p_id}: {e}")

    db.close()
    click.echo("Database sync complete.")

@main.command(name="search")
@click.argument("query")
def search(query):
    """Search the database for content."""
    db = SocialsDatabase()
    results = db.search(query)
    if not results:
        click.echo("No results found.")
    else:
        for text, name, c_type in results:
            click.echo(f"[{name}] ({c_type}): {text[:200]}...")
            click.echo("-" * 40)

if __name__ == "__main__":
    main()
