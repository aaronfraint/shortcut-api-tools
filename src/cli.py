import click
from .stories import get_stories_for_user, print_stories_to_update


@click.group()
def main():
    "'sc' provides command-line access to the shortcut-api-tools library"
    pass


@click.command()
def stories():
    """Show all stories that haven't been updated recently"""
    df = get_stories_for_user()
    print_stories_to_update(df)


all_commands = [stories]

for cmd in all_commands:
    main.add_command(cmd)
