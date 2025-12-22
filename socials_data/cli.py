import click
from pathlib import Path
from .core.manager import PersonalityManager
import json

@click.group()
def main():
    """Socials Data CLI"""
    pass

@main.command(name="list")
def list_personalities():
    """List all available personalities."""
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    for p in personalities:
        click.echo(f"- {p}")

@main.command()
@click.argument("name")
def add(name):
    """Add a new personality."""
    manager = PersonalityManager()
    path = manager.add_personality(name)
    click.echo(f"Created personality structure at {path}")

@main.command()
@click.argument("name")
@click.option("--skip-qa", is_flag=True, help="Skip Q&A generation.")
def process(name, skip_qa):
    """Process data for a personality."""
    manager = PersonalityManager()
    manager.process_personality(name, skip_qa=skip_qa)
    click.echo(f"Processed data for {name}")

if __name__ == "__main__":
    main()
