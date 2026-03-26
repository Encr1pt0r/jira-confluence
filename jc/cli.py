"""
Main CLI entry point for JC - Jira & Confluence CLI tool
"""

import click
from jc.commands import (
    config,
    ticket,
    comment,
    edit,
    transition,
    confluence,
    projects,
    sprint
)


@click.group()
@click.version_option(version='2.0.0')
def cli():
    """Atlassian CLI - Jira & Confluence command-line interface"""
    pass


# Register command groups
cli.add_command(config)
cli.add_command(ticket)
cli.add_command(comment)
cli.add_command(confluence)

# Register standalone commands
cli.add_command(edit)
cli.add_command(transition)
cli.add_command(projects)
cli.add_command(sprint)


if __name__ == '__main__':
    cli()
