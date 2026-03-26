"""
Atlassian API client for Jira and Confluence
"""

import os
import json
import requests
import click
import sys
from pathlib import Path
from jira import JIRA
from requests.auth import HTTPBasicAuth

CONFIG_DIR = Path.home() / '.jira_cli'
CONFIG_FILE = CONFIG_DIR / 'config.json'


class AtlassianClient:
    """Unified client for Jira and Confluence"""

    def __init__(self):
        self.config = self.load_config()
        self._jira = None
        self._confluence_auth = None

    def load_config(self):
        """Load configuration from file or environment"""
        config = {}

        # Try config file first
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)

        # Override with environment variables if present
        if os.getenv('JIRA_SERVER'):
            config['server'] = os.getenv('JIRA_SERVER')
        if os.getenv('JIRA_EMAIL'):
            config['email'] = os.getenv('JIRA_EMAIL')
        if os.getenv('JIRA_API_TOKEN'):
            config['api_token'] = os.getenv('JIRA_API_TOKEN')

        return config

    def save_config(self, server: str, email: str, api_token: str):
        """Save configuration to file"""
        CONFIG_DIR.mkdir(exist_ok=True)
        config = {
            'server': server,
            'email': email,
            'api_token': api_token
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        self.config = config

    @property
    def jira(self):
        """Lazy-load Jira connection"""
        if self._jira is None:
            if not all(k in self.config for k in ['server', 'email', 'api_token']):
                click.echo(click.style('Error: Not configured. Run: jira config set', fg='red'))
                sys.exit(1)

            self._jira = JIRA(
                server=self.config['server'],
                basic_auth=(self.config['email'], self.config['api_token']),
                options={'rest_api_version': '3'}
            )
        return self._jira

    @property
    def confluence_auth(self):
        """Get Confluence authentication"""
        if self._confluence_auth is None:
            if not all(k in self.config for k in ['server', 'email', 'api_token']):
                click.echo(click.style('Error: Not configured. Run: jira config set', fg='red'))
                sys.exit(1)
            self._confluence_auth = HTTPBasicAuth(self.config['email'], self.config['api_token'])
        return self._confluence_auth

    def confluence_get(self, endpoint: str, params: dict = None):
        """Make GET request to Confluence API"""
        base_url = f"{self.config['server']}/wiki/api/v2"
        url = f"{base_url}/{endpoint}"
        response = requests.get(url, auth=self.confluence_auth, params=params)
        response.raise_for_status()
        return response.json()

    def confluence_search(self, query: str, limit: int = 25):
        """Search Confluence content"""
        search_url = f"{self.config['server']}/wiki/rest/api/search"
        params = {'cql': f'text ~ "{query}"', 'limit': limit}
        response = requests.get(search_url, auth=self.confluence_auth, params=params)
        response.raise_for_status()
        return response.json().get('results', [])

    def confluence_get_children(self, page_id: str, limit: int = 25):
        """Get child pages of a Confluence page"""
        return self.confluence_get(f'pages/{page_id}/children', params={'limit': limit})


# Global client instance
client = AtlassianClient()
