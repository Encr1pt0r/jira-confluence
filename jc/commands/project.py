"""
Project and sprint commands
"""

import click
from jc.client import client


@click.command('projects')
@click.option('--search', help='Search projects')
def projects(search):
    """List Jira projects"""
    try:
        all_projects = client.jira.projects()

        if search:
            all_projects = [p for p in all_projects if
                          search.lower() in p.key.lower() or search.lower() in p.name.lower()]

        if not all_projects:
            click.echo(click.style('No projects found', fg='yellow'))
            return

        click.echo(click.style(f'\nFound {len(all_projects)} project(s):\n', fg='green'))

        for project in all_projects:
            click.echo(f"{click.style(project.key, fg='cyan')}: {project.name}")

    except Exception as e:
        click.echo(click.style(f'Error: {e}', fg='red'))


@click.command('sprint')
@click.option('--project', default='SD', help='Project key')
@click.option('--component', help='Filter by component (e.g., ProductArea:H&C)')
def sprint(project, component):
    """Show current sprint tickets"""
    jql = f'project = {project} AND sprint in openSprints()'

    if component:
        jql += f' AND component = "{component}"'

    jql += ' ORDER BY priority DESC'

    try:
        issues = client.jira.search_issues(jql, maxResults=50)

        if not issues:
            click.echo(click.style('No issues in current sprint', fg='yellow'))
            return

        click.echo(click.style(f'\n{len(issues)} ticket(s) in current sprint:\n', fg='green'))

        for issue in issues:
            status_color = 'green' if issue.fields.status.name in ['Done', 'Closed'] else 'yellow'
            click.echo(f"{click.style(issue.key, fg='cyan')}: {issue.fields.summary}")
            assignee = issue.fields.assignee.displayName if issue.fields.assignee else 'Unassigned'
            click.echo(f"  Status: {click.style(issue.fields.status.name, fg=status_color)} | Assignee: {assignee}\n")

    except Exception as e:
        click.echo(click.style(f'Error: {e}', fg='red'))
