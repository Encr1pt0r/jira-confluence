"""
Jira ticket operation commands
"""

import click
from jc.client import client
from jc.formatters import extract_text_from_adf


@click.group()
def ticket():
    """Jira ticket operations"""
    pass


@ticket.command('get')
@click.argument('issue_key')
@click.option('--comments', is_flag=True, help='Show comments')
@click.option('--full', is_flag=True, help='Show full details')
def ticket_get(issue_key, comments, full):
    """Get ticket details"""
    try:
        issue = client.jira.issue(issue_key)

        click.echo(click.style(f'\n{issue.key}: {issue.fields.summary}', fg='cyan', bold=True))
        click.echo(f"Status: {click.style(issue.fields.status.name, fg='yellow')}")
        click.echo(f"Type: {issue.fields.issuetype.name}")

        if hasattr(issue.fields, 'priority') and issue.fields.priority:
            click.echo(f"Priority: {issue.fields.priority.name}")

        if hasattr(issue.fields, 'assignee') and issue.fields.assignee:
            click.echo(f"Assignee: {issue.fields.assignee.displayName}")
        else:
            click.echo("Assignee: Unassigned")

        if hasattr(issue.fields, 'labels') and issue.fields.labels:
            click.echo(f"Labels: {', '.join(issue.fields.labels)}")

        click.echo(f"Created: {issue.fields.created}")
        click.echo(f"Updated: {issue.fields.updated}")

        if full:
            # Access raw description data to avoid PropertyHolder wrapping issues
            raw_description = issue.raw.get('fields', {}).get('description')
            if raw_description:
                click.echo(f"\n{click.style('Description:', bold=True)}")
                description_text = extract_text_from_adf(raw_description)
                if description_text:
                    # Show first 1000 characters
                    if len(description_text) > 1000:
                        click.echo(description_text[:1000] + "\n... (truncated)")
                    else:
                        click.echo(description_text)
                else:
                    click.echo("(No description text available)")

        click.echo(f"\nLink: {client.config['server']}/browse/{issue.key}")

        if comments:
            # Need to fetch with raw data for comments too
            issue_with_comments = client.jira.issue(issue_key, expand='comments')
            raw_comments = issue_with_comments.raw.get('fields', {}).get('comment', {}).get('comments', [])

            if raw_comments:
                click.echo(f"\n{click.style('Comments:', bold=True)}")
                for i, comment in enumerate(raw_comments, 1):
                    author = comment.get('author', {}).get('displayName', 'Unknown')
                    created = comment.get('created', '')
                    click.echo(f"\n{i}. {author} - {created}")
                    comment_body = comment.get('body', {})
                    comment_text = extract_text_from_adf(comment_body)
                    click.echo(f"   {comment_text[:200]}")

    except Exception as e:
        click.echo(click.style(f'Error: {e}', fg='red'))


@ticket.command('search')
@click.argument('jql')
@click.option('--limit', default=10, help='Maximum results')
def ticket_search(jql, limit):
    """Search tickets using JQL"""
    try:
        issues = client.jira.search_issues(jql, maxResults=limit)

        if not issues:
            click.echo(click.style('No issues found', fg='yellow'))
            return

        click.echo(click.style(f'\nFound {len(issues)} issue(s):\n', fg='green'))

        for issue in issues:
            click.echo(click.style(f'{issue.key}:', fg='cyan', bold=True), nl=False)
            click.echo(f' {issue.fields.summary}')
            click.echo(f"  Status: {click.style(issue.fields.status.name, fg='yellow')}")
            assignee = issue.fields.assignee.displayName if issue.fields.assignee else 'Unassigned'
            click.echo(f"  Assignee: {assignee}\n")

    except Exception as e:
        click.echo(click.style(f'Error: {e}', fg='red'))


@ticket.command('mine')
@click.option('--limit', default=10, help='Maximum results')
def ticket_mine(limit):
    """Show your tickets"""
    try:
        issues = client.jira.search_issues('assignee = currentUser() ORDER BY updated DESC', maxResults=limit)

        if not issues:
            click.echo(click.style('No issues assigned to you', fg='yellow'))
            return

        click.echo(click.style(f'\n{len(issues)} ticket(s) assigned to you:\n', fg='green'))

        for issue in issues:
            status_color = 'green' if issue.fields.status.name in ['Done', 'Closed'] else 'yellow'
            click.echo(f"{click.style(issue.key, fg='cyan')}: {issue.fields.summary}")
            click.echo(f"  Status: {click.style(issue.fields.status.name, fg=status_color)}\n")

    except Exception as e:
        click.echo(click.style(f'Error: {e}', fg='red'))
