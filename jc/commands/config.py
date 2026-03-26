"""
Configuration management commands
"""

import click
from jc.client import client, CONFIG_FILE


@click.group()
def config():
    """Manage configuration"""
    pass


@config.command('set')
@click.option('--server', prompt='Atlassian Server URL', help='Server URL (e.g., https://company.atlassian.net)')
@click.option('--email', prompt='Email', help='Your Atlassian email')
@click.option('--api-token', prompt='API Token', hide_input=True, help='Your API token')
def config_set(server, email, api_token):
    """Set credentials"""
    client.save_config(server, email, api_token)
    click.echo(click.style('[OK] Configuration saved successfully!', fg='green'))


@config.command('show')
def config_show():
    """Show current configuration"""
    config = client.config
    if not config:
        click.echo(click.style('No configuration found', fg='yellow'))
        return

    click.echo(click.style('\nCurrent Configuration:', fg='cyan', bold=True))
    click.echo(f"Server: {config.get('server', 'Not set')}")
    click.echo(f"Email: {config.get('email', 'Not set')}")
    click.echo(f"API Token: {'*' * 20 if config.get('api_token') else 'Not set'}")
    click.echo(f"\nConfig file: {CONFIG_FILE}")


@config.command('clear')
@click.confirmation_option(prompt='Clear configuration?')
def config_clear():
    """Clear stored configuration"""
    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()
        click.echo(click.style('[OK] Configuration cleared', fg='green'))
    else:
        click.echo(click.style('No configuration to clear', fg='yellow'))
