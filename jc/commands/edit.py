"""
Ticket editing and transition commands
"""

import click
from jc.client import client


@click.command('edit')
@click.argument('issue_key')
@click.option('--summary', help='Update summary')
@click.option('--description', help='Update description')
@click.option('--assignee', help='Update assignee')
@click.option('--priority', help='Update priority')
def edit(issue_key, summary, description, assignee, priority):
    """Edit ticket fields"""
    fields = {}

    if summary:
        fields['summary'] = summary
    if description:
        fields['description'] = description
    if priority:
        fields['priority'] = {'name': priority}

    if not fields and not assignee:
        click.echo(click.style('No fields to update', fg='yellow'))
        return

    try:
        issue = client.jira.issue(issue_key)

        if fields:
            issue.update(fields=fields)
            click.echo(click.style(f'[OK] Updated {issue_key}', fg='green'))

        if assignee:
            client.jira.assign_issue(issue_key, assignee)
            click.echo(click.style(f'[OK] Assigned to {assignee}', fg='green'))

    except Exception as e:
        click.echo(click.style(f'Error: {e}', fg='red'))


@click.command('transition')
@click.argument('issue_key')
@click.argument('status', required=False)
def transition(issue_key, status):
    """Change ticket status"""
    try:
        transitions = client.jira.transitions(issue_key)

        if not status:
            click.echo(click.style(f'\nAvailable transitions for {issue_key}:', fg='cyan'))
            for t in transitions:
                click.echo(f"  - {t['name']}")
            return

        transition_id = None
        for t in transitions:
            if t['name'].lower() == status.lower():
                transition_id = t['id']
                break

        if not transition_id:
            click.echo(click.style(f'Transition "{status}" not found', fg='red'))
            return

        client.jira.transition_issue(issue_key, transition_id)
        click.echo(click.style(f'[OK] Transitioned {issue_key} to {status}', fg='green'))

    except Exception as e:
        click.echo(click.style(f'Error: {e}', fg='red'))
