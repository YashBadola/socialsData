import click
from socials_data.core.manager import PersonalityManager
from socials_data.core.processor import TextDataProcessor
from socials_data.core.db import SocialsDatabase
import os

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

@main.command(name="init-db")
@click.option("--db-path", default="socials.db", help="Path to the SQLite database.")
def init_db(db_path):
    """Initialize the socials database."""
    db = SocialsDatabase(db_path)
    db.init_db()
    click.echo(f"Database initialized at {db_path}")

@main.command(name="ingest-db")
@click.option("--db-path", default="socials.db", help="Path to the SQLite database.")
@click.option("--all", "ingest_all", is_flag=True, help="Ingest all personalities.")
@click.argument("personality_id", required=False)
def ingest_db(db_path, ingest_all, personality_id):
    """Ingest personality data into the database."""
    if not ingest_all and not personality_id:
        click.echo("Error: Please specify a personality ID or use --all.")
        return

    db = SocialsDatabase(db_path)
    manager = PersonalityManager()

    # Ensure DB is initialized
    db.init_db()

    if ingest_all:
        personalities = manager.list_personalities()
    else:
        personalities = [personality_id]

    for pid in personalities:
        try:
            click.echo(f"Ingesting {pid}...")
            db.ingest_personality(pid, manager.base_dir)
        except Exception as e:
            click.echo(f"Failed to ingest {pid}: {e}")

    click.echo("Ingestion complete.")

@main.command(name="search")
@click.argument("query")
@click.option("--db-path", default="socials.db", help="Path to the SQLite database.")
def search(query, db_path):
    """Search the database."""
    db = SocialsDatabase(db_path)
    results = db.search(query)

    if not results:
        click.echo("No results found.")
        return

    for res in results:
        click.echo(f"--- {res['personality_id']} ({res['source']}) ---")
        click.echo(res['text'][:200] + "...")
        click.echo()

if __name__ == "__main__":
    main()
