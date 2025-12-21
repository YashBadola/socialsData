import click
import os
import json
from socials_data.core.processing import process_personality

@click.group()
def cli():
    pass

@cli.command()
def list():
    """List all available personalities."""
    base_dir = os.path.join(os.path.dirname(__file__), 'personalities')
    if not os.path.exists(base_dir):
        click.echo("No personalities found.")
        return

    personalities = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    for p in sorted(personalities):
        click.echo(p)

@cli.command()
@click.argument('personality_id')
@click.option('--skip-qa', is_flag=True, help='Skip Q&A generation using LLM.')
def process(personality_id, skip_qa):
    """Process raw data for a personality."""
    try:
        process_personality(personality_id, skip_qa)
        click.echo(f"Successfully processed {personality_id}")
    except Exception as e:
        click.echo(f"Error processing {personality_id}: {e}")

@cli.command()
def add():
    """Add a new personality."""
    click.echo("Not implemented yet.")

@cli.command()
def generate_qa():
    """Generate Q&A pairs."""
    click.echo("Not implemented yet.")

if __name__ == '__main__':
    cli()
