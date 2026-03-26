"""
JC - Jira & Confluence CLI Tool

A complete command-line interface for Atlassian tools.
"""

__version__ = '2.0.0'
__author__ = 'Kevin Mbuluko'

from jc.cli import cli
from jc.client import client, AtlassianClient
from jc.formatters import extract_text_from_adf, clean_html

__all__ = [
    'cli',
    'client',
    'AtlassianClient',
    'extract_text_from_adf',
    'clean_html',
]
