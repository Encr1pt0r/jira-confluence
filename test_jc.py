#!/usr/bin/env python3
"""
Comprehensive unit tests for JC CLI tool
Tests all commands, ADF parsing, and output formatting
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock, mock_open
from click.testing import CliRunner
from pathlib import Path
import sys
import os

# Add the current directory to the path to import jc
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import from the jc package
from jc import cli, client
from jc.formatters import extract_text_from_adf, clean_html, html_to_markdown
from jc.client import CONFIG_FILE
import jc


class TestADFTextExtraction:
    """Test Atlassian Document Format text extraction"""

    def test_extract_simple_text(self):
        """Test extracting simple text from ADF"""
        adf = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {"type": "text", "text": "Hello World"}
                    ]
                }
            ]
        }
        result = extract_text_from_adf(adf)
        assert "Hello World" in result

    def test_extract_text_with_formatting(self):
        """Test extracting text with bold/italic formatting"""
        adf = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {"type": "text", "text": "Normal "},
                        {
                            "type": "text",
                            "text": "bold text",
                            "marks": [{"type": "strong"}]
                        }
                    ]
                }
            ]
        }
        result = extract_text_from_adf(adf)
        assert "Normal" in result
        assert "bold text" in result

    def test_extract_text_with_headings(self):
        """Test extracting headings"""
        adf = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "heading",
                    "attrs": {"level": 1},
                    "content": [
                        {"type": "text", "text": "Main Heading"}
                    ]
                },
                {
                    "type": "paragraph",
                    "content": [
                        {"type": "text", "text": "Paragraph text"}
                    ]
                }
            ]
        }
        result = extract_text_from_adf(adf)
        assert "Main Heading" in result
        assert "Paragraph text" in result

    def test_extract_text_with_bullet_list(self):
        """Test extracting bullet list items"""
        adf = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "bulletList",
                    "content": [
                        {
                            "type": "listItem",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {"type": "text", "text": "First item"}
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "listItem",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {"type": "text", "text": "Second item"}
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        result = extract_text_from_adf(adf)
        assert "First item" in result
        assert "Second item" in result

    def test_extract_empty_content(self):
        """Test extracting from empty content"""
        result = extract_text_from_adf(None)
        assert result == ""

        result = extract_text_from_adf({})
        assert result == ""

    def test_extract_plain_string(self):
        """Test that plain strings are returned as-is"""
        result = extract_text_from_adf("Plain text")
        assert result == "Plain text"

    def test_emoji_replacement(self):
        """Test that emojis are replaced with text equivalents"""
        adf = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {"type": "text", "text": "\u2705 Done"},
                        {"type": "text", "text": "\u274c Failed"}
                    ]
                }
            ]
        }
        result = extract_text_from_adf(adf)
        assert "[OK]" in result
        assert "[X]" in result
        assert "\u2705" not in result
        assert "\u274c" not in result

    def test_complex_nested_structure(self):
        """Test extracting from deeply nested ADF structure"""
        adf = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "heading",
                    "attrs": {"level": 1},
                    "content": [
                        {"type": "text", "text": "Title"}
                    ]
                },
                {
                    "type": "bulletList",
                    "content": [
                        {
                            "type": "listItem",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {"type": "text", "text": "Item with "},
                                        {
                                            "type": "text",
                                            "text": "bold",
                                            "marks": [{"type": "strong"}]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        result = extract_text_from_adf(adf)
        assert "Title" in result
        assert "Item with" in result
        assert "bold" in result


class TestCleanHTML:
    """Test HTML cleaning function"""

    def test_clean_basic_html(self):
        """Test cleaning basic HTML tags"""
        html = "<p>Hello <strong>World</strong></p>"
        result = clean_html(html)
        assert result == "Hello World"

    def test_clean_html_with_entities(self):
        """Test cleaning HTML entities"""
        html = "Hello &amp; goodbye &lt;tag&gt;"
        result = clean_html(html)
        assert result == "Hello & goodbye <tag>"

    def test_clean_empty_html(self):
        """Test cleaning empty content"""
        assert clean_html(None) == ""
        assert clean_html("") == ""

    def test_clean_html_with_multiple_spaces(self):
        """Test cleaning extra whitespace"""
        html = "<p>Hello    \n\n    World</p>"
        result = clean_html(html)
        assert result == "Hello World"


class TestHTMLToMarkdown:
    """Test HTML to Markdown conversion function"""

    def test_convert_standard_links(self):
        """Test converting standard HTML links to markdown"""
        html = '<a href="https://example.com">Example Link</a>'
        result = html_to_markdown(html)
        assert result == "[Example Link](https://example.com)"

    def test_convert_multiple_links(self):
        """Test converting multiple links"""
        html = '<p><a href="https://site1.com">Link 1</a> and <a href="https://site2.com">Link 2</a></p>'
        result = html_to_markdown(html)
        assert "[Link 1](https://site1.com)" in result
        assert "[Link 2](https://site2.com)" in result

    def test_convert_confluence_page_links(self):
        """Test converting Confluence page links"""
        html = '<ac:link><ri:page ri:content-title="Test Page" /></ac:link>'
        result = html_to_markdown(html)
        assert "[Test Page]" in result

    def test_convert_children_macro(self):
        """Test converting children macro to readable text"""
        html = '<ac:structured-macro ac:name="children" ac:schema-version="2" />'
        result = html_to_markdown(html)
        assert "[Child Pages Listed Below]" in result

    def test_convert_other_macros(self):
        """Test converting other macros"""
        html = '<ac:structured-macro ac:name="toc" />'
        result = html_to_markdown(html)
        assert "[Macro: toc]" in result

    def test_preserve_text_with_links(self):
        """Test preserving text content alongside links"""
        html = '<p>Check out <a href="https://example.com">this link</a> for more info</p>'
        result = html_to_markdown(html)
        assert "Check out" in result
        assert "[this link](https://example.com)" in result
        assert "for more info" in result

    def test_empty_html_to_markdown(self):
        """Test converting empty HTML"""
        assert html_to_markdown(None) == ""
        assert html_to_markdown("") == ""

    def test_html_entities_in_markdown(self):
        """Test HTML entities are properly decoded"""
        html = '<a href="https://example.com?a=1&amp;b=2">Link &amp; Text</a>'
        result = html_to_markdown(html)
        assert "[Link & Text](https://example.com?a=1&b=2)" in result


class TestConfigCommands:
    """Test configuration management commands"""

    def setup_method(self):
        """Setup test runner"""
        self.runner = CliRunner()

    @patch('jc.client.CONFIG_FILE')
    def test_config_set(self, mock_config_file):
        """Test setting configuration"""
        with self.runner.isolated_filesystem():
            mock_config_file.parent.mkdir = Mock()
            mock_config_file.exists = Mock(return_value=False)

            result = self.runner.invoke(cli, [
                'config', 'set',
                '--server', 'https://test.atlassian.net',
                '--email', 'test@example.com',
                '--api-token', 'test-token'
            ])

            assert result.exit_code == 0
            assert 'Configuration saved' in result.output

    @patch('jc.client.CONFIG_FILE')
    def test_config_show(self, mock_config_file):
        """Test showing configuration"""
        mock_config_file.exists.return_value = True

        mock_config_data = {
            'server': 'https://test.atlassian.net',
            'email': 'test@example.com',
            'api_token': 'secret-token'
        }

        with patch('builtins.open', mock_open(read_data=json.dumps(mock_config_data))):
            result = self.runner.invoke(cli, ['config', 'show'])

            assert result.exit_code == 0
            assert 'https://test.atlassian.net' in result.output
            assert 'test@example.com' in result.output
            assert 'secret-token' not in result.output  # Should be masked
            assert '**' in result.output

    @patch('jc.commands.config.CONFIG_FILE')
    def test_config_clear(self, mock_config_file):
        """Test clearing configuration"""
        mock_config_file.exists.return_value = True
        mock_config_file.unlink = Mock()

        result = self.runner.invoke(cli, ['config', 'clear'], input='y\n')

        assert result.exit_code == 0
        assert 'cleared' in result.output.lower()


class TestTicketCommands:
    """Test Jira ticket commands"""

    def setup_method(self):
        """Setup test runner and mocks"""
        self.runner = CliRunner()

    def test_ticket_get_basic(self):
        """Test getting basic ticket info"""
        # Create mock issue
        mock_issue = Mock()
        mock_issue.key = 'TEST-123'
        mock_issue.fields.summary = 'Test Issue'
        mock_issue.fields.status.name = 'In Progress'
        mock_issue.fields.issuetype.name = 'Story'
        mock_issue.fields.priority.name = 'High'
        mock_issue.fields.assignee.displayName = 'John Doe'
        mock_issue.fields.labels = ['test', 'demo']
        mock_issue.fields.created = '2024-01-01T00:00:00.000+0000'
        mock_issue.fields.updated = '2024-01-02T00:00:00.000+0000'
        mock_issue.raw = {'fields': {}}

        mock_jira = Mock()
        mock_jira.issue.return_value = mock_issue

        with patch.object(client, '_jira', mock_jira):
            with patch.object(client, 'config', {'server': 'https://test.atlassian.net'}):
                result = self.runner.invoke(cli, ['ticket', 'get', 'TEST-123'])

                assert result.exit_code == 0
                assert 'TEST-123' in result.output
                assert 'Test Issue' in result.output
                assert 'In Progress' in result.output

    def test_ticket_get_with_description(self):
        """Test getting ticket with full description"""
        mock_issue = Mock()
        mock_issue.key = 'TEST-456'
        mock_issue.fields.summary = 'Test with Description'
        mock_issue.fields.status.name = 'Open'
        mock_issue.fields.issuetype.name = 'Bug'
        mock_issue.fields.priority = None
        mock_issue.fields.assignee = None
        mock_issue.fields.labels = []
        mock_issue.fields.created = '2024-01-01T00:00:00.000+0000'
        mock_issue.fields.updated = '2024-01-02T00:00:00.000+0000'

        # Mock ADF description
        mock_issue.raw = {
            'fields': {
                'description': {
                    'type': 'doc',
                    'version': 1,
                    'content': [
                        {
                            'type': 'paragraph',
                            'content': [
                                {'type': 'text', 'text': 'This is a test description'}
                            ]
                        }
                    ]
                }
            }
        }

        mock_jira = Mock()
        mock_jira.issue.return_value = mock_issue

        with patch.object(client, '_jira', mock_jira):
            with patch.object(client, 'config', {'server': 'https://test.atlassian.net'}):
                result = self.runner.invoke(cli, ['ticket', 'get', 'TEST-456', '--full'])

                assert result.exit_code == 0
                assert 'TEST-456' in result.output
                assert 'Description:' in result.output
                assert 'This is a test description' in result.output

    def test_ticket_search(self):
        """Test searching tickets with JQL"""
        mock_issue1 = Mock()
        mock_issue1.key = 'TEST-1'
        mock_issue1.fields.summary = 'First issue'
        mock_issue1.fields.status.name = 'Open'
        mock_issue1.fields.assignee.displayName = 'User 1'

        mock_issue2 = Mock()
        mock_issue2.key = 'TEST-2'
        mock_issue2.fields.summary = 'Second issue'
        mock_issue2.fields.status.name = 'Closed'
        mock_issue2.fields.assignee = None

        mock_jira = Mock()
        mock_jira.search_issues.return_value = [mock_issue1, mock_issue2]

        with patch.object(client, '_jira', mock_jira):
            result = self.runner.invoke(cli, ['ticket', 'search', 'project=TEST'])

            assert result.exit_code == 0
            assert 'TEST-1' in result.output
            assert 'TEST-2' in result.output
            assert 'First issue' in result.output
            assert 'Second issue' in result.output

    def test_ticket_mine(self):
        """Test listing user's assigned tickets"""
        mock_issue = Mock()
        mock_issue.key = 'TEST-999'
        mock_issue.fields.summary = 'My ticket'
        mock_issue.fields.status.name = 'In Progress'

        mock_jira = Mock()
        mock_jira.search_issues.return_value = [mock_issue]

        with patch.object(client, '_jira', mock_jira):
            result = self.runner.invoke(cli, ['ticket', 'mine'])

            assert result.exit_code == 0
            assert 'TEST-999' in result.output
            assert 'My ticket' in result.output

    def test_ticket_mine_empty(self):
        """Test listing tickets when none assigned"""
        mock_jira = Mock()
        mock_jira.search_issues.return_value = []

        with patch.object(client, '_jira', mock_jira):
            result = self.runner.invoke(cli, ['ticket', 'mine'])

            assert result.exit_code == 0
            assert 'No issues assigned' in result.output


class TestCommentCommands:
    """Test comment management commands"""

    def setup_method(self):
        """Setup test runner"""
        self.runner = CliRunner()

    def test_comment_add(self):
        """Test adding a comment"""
        mock_jira = Mock()
        mock_jira.add_comment = Mock()

        with patch.object(client, '_jira', mock_jira):
            result = self.runner.invoke(cli, [
                'comment', 'add', 'TEST-123', 'This is a test comment'
            ])

            assert result.exit_code == 0
            assert 'Comment added' in result.output
            mock_jira.add_comment.assert_called_once_with('TEST-123', 'This is a test comment')

    def test_comment_list(self):
        """Test listing comments"""
        mock_issue = Mock()
        mock_issue.raw = {
            'fields': {
                'comment': {
                    'comments': [
                        {
                            'author': {'displayName': 'John Doe'},
                            'created': '2024-01-01T00:00:00.000+0000',
                            'body': {
                                'type': 'doc',
                                'version': 1,
                                'content': [
                                    {
                                        'type': 'paragraph',
                                        'content': [
                                            {'type': 'text', 'text': 'First comment'}
                                        ]
                                    }
                                ]
                            }
                        },
                        {
                            'author': {'displayName': 'Jane Smith'},
                            'created': '2024-01-02T00:00:00.000+0000',
                            'body': {
                                'type': 'doc',
                                'version': 1,
                                'content': [
                                    {
                                        'type': 'paragraph',
                                        'content': [
                                            {'type': 'text', 'text': 'Second comment'}
                                        ]
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        }

        mock_jira = Mock()
        mock_jira.issue.return_value = mock_issue

        with patch.object(client, '_jira', mock_jira):
            result = self.runner.invoke(cli, ['comment', 'list', 'TEST-123'])

            assert result.exit_code == 0
            assert 'John Doe' in result.output
            assert 'Jane Smith' in result.output
            assert 'First comment' in result.output
            assert 'Second comment' in result.output


class TestEditCommands:
    """Test ticket editing commands"""

    def setup_method(self):
        """Setup test runner"""
        self.runner = CliRunner()

    def test_edit_summary(self):
        """Test editing ticket summary"""
        mock_issue = Mock()
        mock_issue.update = Mock()

        mock_jira = Mock()
        mock_jira.issue.return_value = mock_issue

        with patch.object(client, '_jira', mock_jira):
            result = self.runner.invoke(cli, [
                'edit', 'TEST-123', '--summary', 'New summary'
            ])

            assert result.exit_code == 0
            assert 'Updated' in result.output
            mock_issue.update.assert_called_once()

    def test_edit_assignee(self):
        """Test changing ticket assignee"""
        mock_issue = Mock()

        mock_jira = Mock()
        mock_jira.issue.return_value = mock_issue
        mock_jira.assign_issue = Mock()

        with patch.object(client, '_jira', mock_jira):
            result = self.runner.invoke(cli, [
                'edit', 'TEST-123', '--assignee', 'john.doe'
            ])

            assert result.exit_code == 0
            mock_jira.assign_issue.assert_called_once_with('TEST-123', 'john.doe')

    def test_transition_list(self):
        """Test listing available transitions"""
        mock_jira = Mock()
        mock_jira.transitions.return_value = [
            {'id': '1', 'name': 'Start Progress'},
            {'id': '2', 'name': 'Done'}
        ]

        with patch.object(client, '_jira', mock_jira):
            result = self.runner.invoke(cli, ['transition', 'TEST-123'])

            assert result.exit_code == 0
            assert 'Start Progress' in result.output
            assert 'Done' in result.output

    def test_transition_execute(self):
        """Test executing a transition"""
        mock_jira = Mock()
        mock_jira.transitions.return_value = [
            {'id': '1', 'name': 'Start Progress'},
            {'id': '2', 'name': 'Done'}
        ]
        mock_jira.transition_issue = Mock()

        with patch.object(client, '_jira', mock_jira):
            result = self.runner.invoke(cli, ['transition', 'TEST-123', 'Done'])

            assert result.exit_code == 0
            assert 'Transitioned' in result.output
            mock_jira.transition_issue.assert_called_once_with('TEST-123', '2')


class TestConfluenceCommands:
    """Test Confluence commands"""

    def setup_method(self):
        """Setup test runner"""
        self.runner = CliRunner()

    @patch('jc.client.client.confluence_get')
    def test_confluence_spaces(self, mock_confluence_get):
        """Test listing Confluence spaces"""
        mock_confluence_get.return_value = {
            'results': [
                {'key': 'TEST', 'name': 'Test Space'},
                {'key': 'DEMO', 'name': 'Demo Space'}
            ]
        }

        with patch.object(client, 'config', {'server': 'https://test.atlassian.net'}):
            result = self.runner.invoke(cli, ['confluence', 'spaces'])

            assert result.exit_code == 0
            assert 'TEST' in result.output
            assert 'Test Space' in result.output
            assert 'DEMO' in result.output

    @patch('jc.client.client.confluence_get')
    def test_confluence_pages(self, mock_confluence_get):
        """Test listing pages in a space"""
        mock_confluence_get.return_value = {
            'results': [
                {
                    'title': 'Page 1',
                    '_links': {'webui': '/spaces/TEST/pages/123'}
                },
                {
                    'title': 'Page 2',
                    '_links': {'webui': '/spaces/TEST/pages/456'}
                }
            ]
        }

        with patch.object(client, 'config', {'server': 'https://test.atlassian.net'}):
            result = self.runner.invoke(cli, ['confluence', 'pages', 'TEST'])

            assert result.exit_code == 0
            assert 'Page 1' in result.output
            assert 'Page 2' in result.output

    @patch('jc.client.client.confluence_get')
    def test_confluence_page_detail(self, mock_confluence_get):
        """Test getting page details"""
        mock_confluence_get.return_value = {
            'title': 'Test Page',
            'spaceId': 'TEST',
            '_links': {'webui': '/spaces/TEST/pages/123'},
            'body': {
                'storage': {
                    'value': '<p>This is the page content</p>'
                }
            }
        }

        with patch.object(client, 'config', {'server': 'https://test.atlassian.net'}):
            result = self.runner.invoke(cli, ['confluence', 'page', '123', '--preview'])

            assert result.exit_code == 0
            assert 'Test Page' in result.output
            assert 'This is the page content' in result.output

    @patch('jc.client.client.confluence_search')
    def test_confluence_search(self, mock_search):
        """Test searching Confluence"""
        mock_search.return_value = [
            {
                'title': 'Search Result 1',
                'url': '/wiki/spaces/TEST/pages/123',
                'excerpt': 'This is a test result',
                'resultGlobalContainer': {'title': 'TEST Space'}
            }
        ]

        with patch.object(client, 'config', {'server': 'https://test.atlassian.net'}):
            result = self.runner.invoke(cli, ['confluence', 'search', 'test'])

            assert result.exit_code == 0
            assert 'Search Result 1' in result.output
            assert 'This is a test result' in result.output

    @patch('jc.client.client.confluence_get')
    def test_confluence_from_url_basic(self, mock_confluence_get):
        """Test getting page from URL"""
        mock_confluence_get.return_value = {
            'title': 'Test Page',
            'spaceId': '12345',
            '_links': {'webui': '/spaces/TEST/pages/999/Test-Page'},
            'body': {
                'storage': {
                    'value': '<p>Page content</p>'
                }
            }
        }

        with patch.object(client, 'config', {'server': 'https://test.atlassian.net'}):
            result = self.runner.invoke(cli, [
                'confluence', 'from-url',
                'https://test.atlassian.net/wiki/spaces/TEST/pages/999/Test-Page'
            ])

            assert result.exit_code == 0
            assert 'Test Page' in result.output
            assert 'Page ID: 999' in result.output
            assert 'Space: 12345' in result.output

    @patch('jc.client.client.confluence_get')
    def test_confluence_from_url_with_preview(self, mock_confluence_get):
        """Test getting page from URL with content preview"""
        mock_confluence_get.return_value = {
            'title': 'Test Page',
            'spaceId': '12345',
            '_links': {'webui': '/spaces/TEST/pages/888'},
            'body': {
                'storage': {
                    'value': '<p>This is <strong>test</strong> content</p>'
                }
            }
        }

        with patch.object(client, 'config', {'server': 'https://test.atlassian.net'}):
            result = self.runner.invoke(cli, [
                'confluence', 'from-url',
                'https://test.atlassian.net/wiki/pages/888',
                '--preview'
            ])

            assert result.exit_code == 0
            assert 'Test Page' in result.output
            assert 'Content Preview:' in result.output
            assert 'test' in result.output

    @patch('jc.client.client.confluence_get_children')
    @patch('jc.client.client.confluence_get')
    def test_confluence_from_url_with_children(self, mock_confluence_get, mock_get_children):
        """Test getting page from URL with child pages"""
        mock_confluence_get.return_value = {
            'title': 'Parent Page',
            'spaceId': '12345',
            '_links': {'webui': '/spaces/TEST/pages/777'},
            'body': {
                'storage': {
                    'value': '<ac:structured-macro ac:name="children" />'
                }
            }
        }

        mock_get_children.return_value = {
            'results': [
                {'id': '778', 'title': 'Child Page 1'},
                {'id': '779', 'title': 'Child Page 2'}
            ]
        }

        with patch.object(client, 'config', {'server': 'https://test.atlassian.net'}):
            result = self.runner.invoke(cli, [
                'confluence', 'from-url',
                'https://test.atlassian.net/wiki/spaces/TEST/pages/777',
                '--preview'
            ])

            assert result.exit_code == 0
            assert 'Parent Page' in result.output
            assert 'Child Pages:' in result.output
            assert 'Child Page 1' in result.output
            assert 'Child Page 2' in result.output
            assert '/wiki/pages/778' in result.output
            assert '/wiki/pages/779' in result.output

    @patch('jc.client.client.confluence_get')
    def test_confluence_from_url_invalid_url(self, mock_confluence_get):
        """Test handling invalid URL format"""
        with patch.object(client, 'config', {'server': 'https://test.atlassian.net'}):
            result = self.runner.invoke(cli, [
                'confluence', 'from-url',
                'https://test.atlassian.net/invalid/url'
            ])

            assert result.exit_code == 0
            assert 'Could not extract page ID' in result.output

    @patch('jc.client.client.confluence_get_children')
    @patch('jc.client.client.confluence_get')
    def test_confluence_from_url_with_output(self, mock_confluence_get, mock_get_children):
        """Test exporting page to file"""
        mock_confluence_get.return_value = {
            'title': 'Export Test Page',
            'spaceId': '12345',
            '_links': {'webui': '/spaces/TEST/pages/555'},
            'body': {
                'storage': {
                    'value': '<p>This is the full content that should not be truncated.</p>'
                }
            }
        }

        mock_get_children.return_value = {
            'results': [
                {'id': '556', 'title': 'Child Page 1'},
                {'id': '557', 'title': 'Child Page 2'}
            ]
        }

        with self.runner.isolated_filesystem():
            with patch.object(client, 'config', {'server': 'https://test.atlassian.net'}):
                result = self.runner.invoke(cli, [
                    'confluence', 'from-url',
                    'https://test.atlassian.net/wiki/pages/555',
                    '--output', 'test_export.md'
                ])

                assert result.exit_code == 0
                assert 'Exported to: test_export.md' in result.output

                # Verify file was created and contains expected content
                with open('test_export.md', 'r', encoding='utf-8') as f:
                    content = f.read()
                    assert 'Export Test Page' in content
                    assert '**Page ID:** 555' in content
                    assert '**Space ID:** 12345' in content
                    assert 'Child Page 1' in content
                    assert 'Child Page 2' in content
                    assert 'full content that should not be truncated' in content
                    # Verify content is NOT truncated
                    assert '(truncated)' not in content

    @patch('jc.client.client.confluence_get')
    def test_confluence_from_url_with_output_no_children(self, mock_confluence_get):
        """Test exporting page without children to file"""
        mock_confluence_get.return_value = {
            'title': 'Simple Page',
            'spaceId': '99999',
            '_links': {'webui': '/spaces/TEST/pages/888'},
            'body': {
                'storage': {
                    'value': '<p>Simple content without children.</p>'
                }
            }
        }

        with self.runner.isolated_filesystem():
            with patch.object(client, 'config', {'server': 'https://test.atlassian.net'}):
                result = self.runner.invoke(cli, [
                    'confluence', 'from-url',
                    'https://test.atlassian.net/wiki/pages/888',
                    '-o', 'simple.md'
                ])

                assert result.exit_code == 0
                assert 'Exported to: simple.md' in result.output

                # Verify file content
                with open('simple.md', 'r', encoding='utf-8') as f:
                    content = f.read()
                    assert 'Simple Page' in content
                    assert 'Simple content without children' in content
                    assert 'Child Pages' not in content

    @patch('jc.client.client.confluence_get')
    def test_confluence_get_children_method(self, mock_get):
        """Test confluence_get_children client method"""
        mock_get.return_value = {
            'results': [
                {'id': '100', 'title': 'Child 1'},
                {'id': '200', 'title': 'Child 2'}
            ]
        }

        with patch.object(client, 'config', {'server': 'https://test.atlassian.net'}):
            result = client.confluence_get_children('123')

            assert 'results' in result
            assert len(result['results']) == 2
            # Verify it calls confluence_get with the correct endpoint
            mock_get.assert_called_once_with('pages/123/children', params={'limit': 25})


class TestProjectCommands:
    """Test project-related commands"""

    def setup_method(self):
        """Setup test runner"""
        self.runner = CliRunner()

    def test_projects_list(self):
        """Test listing projects"""
        mock_project1 = Mock()
        mock_project1.key = 'TEST'
        mock_project1.name = 'Test Project'

        mock_project2 = Mock()
        mock_project2.key = 'DEMO'
        mock_project2.name = 'Demo Project'

        mock_jira = Mock()
        mock_jira.projects.return_value = [mock_project1, mock_project2]

        with patch.object(client, '_jira', mock_jira):
            result = self.runner.invoke(cli, ['projects'])

            assert result.exit_code == 0
            assert 'TEST' in result.output
            assert 'Test Project' in result.output
            assert 'DEMO' in result.output

    def test_projects_search(self):
        """Test searching projects"""
        mock_project = Mock()
        mock_project.key = 'TEST'
        mock_project.name = 'Test Project'

        mock_jira = Mock()
        mock_jira.projects.return_value = [mock_project]

        with patch.object(client, '_jira', mock_jira):
            result = self.runner.invoke(cli, ['projects', '--search', 'test'])

            assert result.exit_code == 0
            assert 'TEST' in result.output

    def test_sprint_command(self):
        """Test sprint command"""
        mock_issue = Mock()
        mock_issue.key = 'TEST-100'
        mock_issue.fields.summary = 'Sprint item'
        mock_issue.fields.status.name = 'In Progress'
        mock_issue.fields.assignee.displayName = 'John Doe'

        mock_jira = Mock()
        mock_jira.search_issues.return_value = [mock_issue]

        with patch.object(client, '_jira', mock_jira):
            result = self.runner.invoke(cli, ['sprint', '--project', 'TEST'])

            assert result.exit_code == 0
            assert 'TEST-100' in result.output
            assert 'Sprint item' in result.output


class TestErrorHandling:
    """Test error handling and edge cases"""

    def setup_method(self):
        """Setup test runner"""
        self.runner = CliRunner()

    def test_ticket_not_found(self):
        """Test handling of non-existent ticket"""
        mock_jira = Mock()
        mock_jira.issue.side_effect = Exception('Issue not found')

        with patch.object(client, '_jira', mock_jira):
            result = self.runner.invoke(cli, ['ticket', 'get', 'NOTFOUND-999'])

            assert result.exit_code == 0  # Click doesn't fail, shows error
            assert 'Error' in result.output

    def test_search_with_invalid_jql(self):
        """Test handling of invalid JQL"""
        mock_jira = Mock()
        mock_jira.search_issues.side_effect = Exception('Invalid JQL')

        with patch.object(client, '_jira', mock_jira):
            result = self.runner.invoke(cli, ['ticket', 'search', 'invalid JQL!!!'])

            assert 'Error' in result.output

    def test_no_configuration(self):
        """Test behavior when not configured"""
        # Create a new client with no config
        with patch.object(client, 'config', {}):
            with patch.object(client, '_jira', None):
                result = self.runner.invoke(cli, ['ticket', 'get', 'TEST-1'])

                # Should show error about not being configured
                assert 'Error' in result.output or result.exit_code != 0


class TestAtlassianClient:
    """Test AtlassianClient class"""

    @patch('jc.client.CONFIG_FILE')
    def test_load_config_from_file(self, mock_config_file):
        """Test loading config from file"""
        mock_config_file.exists.return_value = True
        config_data = {
            'server': 'https://test.atlassian.net',
            'email': 'test@example.com',
            'api_token': 'test-token'
        }

        with patch('builtins.open', mock_open(read_data=json.dumps(config_data))):
            from jc.client import AtlassianClient
            test_client = AtlassianClient()
            assert test_client.config['server'] == 'https://test.atlassian.net'
            assert test_client.config['email'] == 'test@example.com'

    @patch('jc.client.CONFIG_FILE')
    @patch.dict(os.environ, {
        'JIRA_SERVER': 'https://env.atlassian.net',
        'JIRA_EMAIL': 'env@example.com',
        'JIRA_API_TOKEN': 'env-token'
    })
    def test_load_config_from_env(self, mock_config_file):
        """Test that environment variables override config file"""
        mock_config_file.exists.return_value = True
        config_data = {
            'server': 'https://file.atlassian.net',
            'email': 'file@example.com',
            'api_token': 'file-token'
        }

        with patch('builtins.open', mock_open(read_data=json.dumps(config_data))):
            from jc.client import AtlassianClient
            test_client = AtlassianClient()
            # Environment variables should override file config
            assert test_client.config['server'] == 'https://env.atlassian.net'
            assert test_client.config['email'] == 'env@example.com'
            assert test_client.config['api_token'] == 'env-token'


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
