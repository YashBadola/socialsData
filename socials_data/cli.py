import click
from socials_data.core.manager import PersonalityManager
from socials_data.core.processor import TextDataProcessor
from socials_data.core.database import SocialsDatabase
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

@main.group()
def db():
    """Database management commands."""
    pass

@db.command()
def init():
    """Initialize the database."""
    db = SocialsDatabase()
    db.init_db()
    click.echo("Database initialized.")

@db.command()
@click.argument("personality_id", required=False)
def sync(personality_id):
    """Sync personality data to database. If no ID provided, syncs all."""
    manager = PersonalityManager()
    db = SocialsDatabase()
    db.init_db() # Ensure DB exists

    if personality_id:
        try:
            manager.get_metadata(personality_id) # Verify existence
            personality_dir = manager.base_dir / personality_id
            click.echo(f"Syncing {personality_id}...")
            db.sync_personality(personality_id, personality_dir)
        except FileNotFoundError:
            click.echo(f"Error: Personality '{personality_id}' not found.")
    else:
        personalities = manager.list_personalities()
        for pid in personalities:
            personality_dir = manager.base_dir / pid
            click.echo(f"Syncing {pid}...")
            db.sync_personality(pid, personality_dir)
    click.echo("Sync complete.")

@db.command()
@click.argument("query_text")
def query(query_text):
    """Search the database."""
    db = SocialsDatabase()
    results = db.query(query_text)
    if not results:
        click.echo("No results found.")
    else:
        for row in results:
            # sqlite3.Row allows access by column name
            click.echo(f"[{row['name']}] ({row['source']}): {row['text'][:100]}...")

if __name__ == "__main__":
    main()
