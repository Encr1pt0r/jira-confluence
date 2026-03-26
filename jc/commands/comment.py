"""
Comment management commands
"""

import click
from jc.client import client
from jc.formatters import extract_text_from_adf


@click.group()
def comment():
    """Manage ticket comments"""
    pass


@comment.command('add')
@click.argument('issue_key')
@click.argument('text', required=False)
@click.option('--file', type=click.File('r'), help='Read from file')
def comment_add(issue_key, text, file):
    """Add comment to ticket"""
    if file:
        text = file.read()
    elif not text:
        text = click.edit('# Enter your comment here')

    if not text or text.startswith('#'):
        click.echo(click.style('No comment provided', fg='red'))
        return

    try:
        client.jira.add_comment(issue_key, text)
        click.echo(click.style(f'[OK] Comment added to {issue_key}', fg='green'))
    except Exception as e:
        click.echo(click.style(f'Error: {e}', fg='red'))


@comment.command('list')
@click.argument('issue_key')
@click.option('--limit', default=10, help='Maximum comments')
def comment_list(issue_key, limit):
    """List ticket comments"""
    try:
        # Fetch issue with raw comment data
        issue = client.jira.issue(issue_key, expand='comments')
        raw_comments = issue.raw.get('fields', {}).get('comment', {}).get('comments', [])

        if not raw_comments:
            click.echo(click.style('No comments found', fg='yellow'))
            return

        click.echo(click.style(f'\n{len(raw_comments)} comment(s) on {issue_key}:\n', fg='green'))

        for i, comment in enumerate(raw_comments[:limit], 1):
            author = comment.get('author', {}).get('displayName', 'Unknown')
            created = comment.get('created', '')
            click.echo(click.style(f'{i}. {author}', fg='cyan'))
            click.echo(f'   {created}')
            comment_body = comment.get('body', {})
            comment_text = extract_text_from_adf(comment_body)
            click.echo(f'   {comment_text[:300]}\n')

    except Exception as e:
        click.echo(click.style(f'Error: {e}', fg='red'))
