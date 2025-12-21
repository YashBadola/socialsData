import click
import os
from socials_data.core.processing import process_personality

@click.group()
def cli():
    """Socials Data CLI"""
    pass

@cli.command(name="list")
def list_personalities():
    """List available personalities"""
    base_dir = os.path.join(os.path.dirname(__file__), "personalities")
    if not os.path.exists(base_dir):
        click.echo("No personalities found.")
        return

    personalities = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    for p in sorted(personalities):
        click.echo(p)

@cli.command()
@click.argument("name")
@click.option("--skip-qa", is_flag=True, help="Skip Q&A generation")
def process(name, skip_qa):
    """Process raw data for a personality"""
    click.echo(f"Processing {name}...")
    process_personality(name, skip_qa)

@cli.command()
@click.argument("name")
def add(name):
    """Add a new personality"""
    click.echo(f"Adding {name} (not implemented yet)")

@cli.command()
@click.argument("name")
def generate_qa(name):
    """Generate Q&A for a personality"""
    click.echo(f"Generating Q&A for {name} (not implemented yet)")

if __name__ == "__main__":
    cli()
