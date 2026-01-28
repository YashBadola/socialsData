import click
from socials_data.core.manager import PersonalityManager
from socials_data.core.processor import TextDataProcessor
from socials_data.core.db import DatabaseManager
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
def init_db():
    """Initialize the SQLite database."""
    db_manager = DatabaseManager()
    db_manager.init_db()
    click.echo("Database initialized.")

@main.command(name="sync-db")
@click.argument("personality_id")
def sync_db(personality_id):
    """Sync a personality's processed data into the database."""
    db_manager = DatabaseManager()
    db_manager.sync_personality(personality_id)
    click.echo(f"Synced {personality_id} to database.")

@main.command(name="query")
@click.argument("sql")
def query(sql):
    """Run a SQL query against the database."""
    db_manager = DatabaseManager()
    columns, results = db_manager.query(sql)
    if columns is None:
        click.echo(results) # Error message
    else:
        # Simple table printing
        if not results:
            click.echo("No results.")
            return

        # Calculate widths
        widths = [len(c) for c in columns]
        for row in results:
            for i, val in enumerate(row):
                widths[i] = max(widths[i], len(str(val)))

        # Print header
        header = " | ".join(c.ljust(w) for c, w in zip(columns, widths))
        click.echo(header)
        click.echo("-" * len(header))

        # Print rows
        for row in results:
            click.echo(" | ".join(str(val).ljust(w) for val, w in zip(row, widths)))

if __name__ == "__main__":
    main()
