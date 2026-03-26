"""
Confluence operation commands
"""

import click
import re
from jc.client import client
from jc.formatters import clean_html, html_to_markdown


@click.group()
def confluence():
    """Confluence operations"""
    pass


@confluence.command('spaces')
@click.option('--search', help='Search spaces')
@click.option('--limit', default=25, help='Maximum results')
def confluence_spaces(search, limit):
    """List Confluence spaces"""
    try:
        data = client.confluence_get('spaces', params={'limit': limit})
        spaces = data.get('results', [])

        if search:
            spaces = [s for s in spaces if
                     search.lower() in s.get('name', '').lower() or
                     search.lower() in s.get('key', '').lower()]

        if not spaces:
            click.echo(click.style('No spaces found', fg='yellow'))
            return

        click.echo(click.style(f'\nFound {len(spaces)} space(s):\n', fg='green'))

        for space in spaces:
            click.echo(click.style(f"{space.get('key')}: {space.get('name')}", fg='cyan'))
            click.echo(f"  URL: {client.config['server']}/wiki/spaces/{space.get('key')}\n")

    except Exception as e:
        click.echo(click.style(f'Error: {e}', fg='red'))


@confluence.command('pages')
@click.argument('space_key')
@click.option('--search', help='Search pages by title')
@click.option('--limit', default=25, help='Maximum results')
def confluence_pages(space_key, search, limit):
    """List pages in a space"""
    try:
        data = client.confluence_get(f'spaces/{space_key}/pages', params={'limit': limit})
        pages = data.get('results', [])

        if search:
            pages = [p for p in pages if search.lower() in p.get('title', '').lower()]

        if not pages:
            click.echo(click.style('No pages found', fg='yellow'))
            return

        click.echo(click.style(f'\nFound {len(pages)} page(s) in {space_key}:\n', fg='green'))

        for page in pages:
            click.echo(click.style(page.get('title'), fg='cyan'))
            webui = page.get('_links', {}).get('webui', '')
            click.echo(f"  URL: {client.config['server']}/wiki{webui}\n")

    except Exception as e:
        click.echo(click.style(f'Error: {e}', fg='red'))


@confluence.command('page')
@click.argument('page_id')
@click.option('--preview', is_flag=True, help='Show content preview')
def confluence_page(page_id, preview):
    """Get page details"""
    try:
        data = client.confluence_get(f'pages/{page_id}', params={'body-format': 'storage'})

        click.echo(click.style(f"\n{data.get('title')}", fg='cyan', bold=True))
        click.echo(f"Space: {data.get('spaceId', 'N/A')}")
        webui = data.get('_links', {}).get('webui', '')
        click.echo(f"URL: {client.config['server']}/wiki{webui}")

        if preview:
            body = data.get('body', {})
            if 'storage' in body:
                content = body['storage'].get('value', '')
                markdown_content = html_to_markdown(content)
                click.echo(f"\n{click.style('Content Preview:', bold=True)}")
                click.echo(markdown_content[:1500])
                if len(markdown_content) > 1500:
                    click.echo("\n... (truncated)")

    except Exception as e:
        click.echo(click.style(f'Error: {e}', fg='red'))


@confluence.command('search')
@click.argument('query')
@click.option('--limit', default=10, help='Maximum results')
def confluence_search_cmd(query, limit):
    """Search Confluence content"""
    try:
        results = client.confluence_search(query, limit)

        if not results:
            click.echo(click.style('No results found', fg='yellow'))
            return

        click.echo(click.style(f'\nFound {len(results)} result(s):\n', fg='green'))

        for i, result in enumerate(results, 1):
            click.echo(click.style(f"{i}. {result.get('title', 'Untitled')}", fg='cyan'))

            space_info = result.get('resultGlobalContainer', {})
            if space_info:
                click.echo(f"   Space: {space_info.get('title', 'N/A')}")

            click.echo(f"   URL: {client.config['server']}{result.get('url', '')}")

            if 'excerpt' in result:
                excerpt = clean_html(result.get('excerpt', ''))[:150]
                click.echo(f"   {excerpt}...")

            click.echo()

    except Exception as e:
        click.echo(click.style(f'Error: {e}', fg='red'))


@confluence.command('from-url')
@click.argument('url')
@click.option('--preview', is_flag=True, help='Show content preview')
@click.option('--open', 'open_browser', is_flag=True, help='Open page in browser')
@click.option('--children', is_flag=True, help='Show child pages (if any)')
@click.option('--output', '-o', help='Export full content to file (no truncation)')
def confluence_from_url(url, preview, open_browser, children, output):
    """Get page details from a Confluence URL"""
    try:
        # Extract page ID from URL
        # Supports formats like:
        # - /wiki/spaces/SPACE/pages/123456789/Page-Title
        # - /wiki/pages/123456789
        # - /wiki/pages/123456789/Page-Title
        page_id_match = re.search(r'/pages/(\d+)', url)

        if not page_id_match:
            click.echo(click.style('Error: Could not extract page ID from URL', fg='red'))
            click.echo('Expected format: .../wiki/spaces/SPACE/pages/123456789/... or .../wiki/pages/123456789/...')
            return

        page_id = page_id_match.group(1)

        # Fetch page details with body content
        params = {}
        if preview or output:
            params['body-format'] = 'storage'
        data = client.confluence_get(f'pages/{page_id}', params=params)

        click.echo(click.style(f"\n{data.get('title')}", fg='cyan', bold=True))
        click.echo(f"Page ID: {page_id}")
        click.echo(f"Space: {data.get('spaceId', 'N/A')}")

        webui = data.get('_links', {}).get('webui', '')
        full_url = f"{client.config['server']}/wiki{webui}"
        click.echo(f"URL: {full_url}")

        if preview:
            body = data.get('body', {})
            if 'storage' in body:
                content = body['storage'].get('value', '')
                markdown_content = html_to_markdown(content)
                click.echo(f"\n{click.style('Content Preview:', bold=True)}")
                if markdown_content:
                    click.echo(markdown_content[:1500])
                    if len(markdown_content) > 1500:
                        click.echo("\n... (truncated)")
                else:
                    click.echo("(No content available)")
            else:
                click.echo(f"\n{click.style('Note:', fg='yellow')} Content format not available in response")
                click.echo(f"Available keys: {list(body.keys())}")

        # Fetch child pages if needed
        child_pages = []
        should_fetch_children = children or output or (preview and 'ac:structured-macro ac:name="children"' in data.get('body', {}).get('storage', {}).get('value', ''))

        if should_fetch_children:
            try:
                child_data = client.confluence_get_children(page_id)
                child_pages = child_data.get('results', [])
            except Exception as e:
                if not output:
                    click.echo(click.style(f'\nError fetching child pages: {e}', fg='yellow'))

        # Show child pages in terminal
        if (children or (preview and 'ac:structured-macro ac:name="children"' in data.get('body', {}).get('storage', {}).get('value', ''))) and not output:
            if child_pages:
                click.echo(f"\n{click.style('Child Pages:', bold=True)}")
                for i, child in enumerate(child_pages, 1):
                    child_title = child.get('title', 'Untitled')
                    child_id = child.get('id', '')
                    # Construct URL from page ID
                    child_url = f"{client.config['server']}/wiki/pages/{child_id}"
                    click.echo(f"  {i}. [{child_title}]({child_url})")
            else:
                if children:
                    click.echo(f"\n{click.style('No child pages found', fg='yellow')}")

        # Export to file if requested
        if output:
            try:
                body = data.get('body', {})
                content = ''
                if 'storage' in body:
                    content = body['storage'].get('value', '')

                markdown_content = html_to_markdown(content)

                # Build the export file content
                export_lines = [
                    f"# {data.get('title', 'Untitled')}",
                    "",
                    f"**Page ID:** {page_id}",
                    f"**Space ID:** {data.get('spaceId', 'N/A')}",
                    f"**URL:** {full_url}",
                    "",
                    "---",
                    ""
                ]

                # Add child pages section if any
                if child_pages:
                    export_lines.append("## Child Pages")
                    export_lines.append("")
                    for i, child in enumerate(child_pages, 1):
                        child_title = child.get('title', 'Untitled')
                        child_id = child.get('id', '')
                        child_url = f"{client.config['server']}/wiki/pages/{child_id}"
                        export_lines.append(f"{i}. [{child_title}]({child_url})")
                    export_lines.append("")
                    export_lines.append("---")
                    export_lines.append("")

                # Add full content (no truncation)
                if markdown_content:
                    export_lines.append("## Content")
                    export_lines.append("")
                    export_lines.append(markdown_content)
                else:
                    export_lines.append("*No content available*")

                # Write to file
                with open(output, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(export_lines))

                click.echo(click.style(f'\nExported to: {output}', fg='green'))

            except Exception as e:
                click.echo(click.style(f'\nError exporting to file: {e}', fg='red'))

        if open_browser:
            import webbrowser
            webbrowser.open(full_url)
            click.echo(click.style('\nOpened in browser', fg='green'))

    except Exception as e:
        click.echo(click.style(f'Error: {e}', fg='red'))
