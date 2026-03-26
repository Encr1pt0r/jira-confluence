"""
Text formatting utilities for JC CLI
Handles ADF (Atlassian Document Format) parsing and HTML cleaning
"""

import re
import html


def extract_text_from_adf(adf_content):
    """Extract plain text from Atlassian Document Format (ADF)"""
    if not adf_content:
        return ""

    # If it's already a string, return it
    if isinstance(adf_content, str):
        return adf_content

    text_parts = []

    def extract_from_node(node):
        """Recursively extract text from ADF nodes"""
        if isinstance(node, dict):
            # Text nodes have 'text' field
            if 'text' in node:
                text_parts.append(node['text'])

            # Recursively process content
            if 'content' in node:
                for child in node['content']:
                    extract_from_node(child)

            # Add line breaks for paragraphs and list items
            node_type = node.get('type', '')
            if node_type in ['paragraph', 'heading', 'listItem']:
                text_parts.append('\n')

        elif isinstance(node, list):
            for item in node:
                extract_from_node(item)

    try:
        extract_from_node(adf_content)
        result = ''.join(text_parts).strip()
        # Clean up multiple newlines
        result = re.sub(r'\n{3,}', '\n\n', result)

        # Handle Windows console encoding issues by replacing problematic characters
        # Replace common emojis with text equivalents
        emoji_map = {
            '\u2705': '[OK]',  # ✅ check mark
            '\u274c': '[X]',   # ❌ cross mark
            '\u26a0': '[!]',   # ⚠️ warning
            '\u2139': '[i]',   # ℹ️ info
            '\u2714': '[✓]',   # ✔ check mark
            '\u2716': '[✗]',   # ✖ cross mark
        }
        for emoji, replacement in emoji_map.items():
            result = result.replace(emoji, replacement)

        return result
    except Exception as e:
        return f"(Error extracting text: {e})"


def clean_html(html_text):
    """Remove HTML tags and clean up text"""
    if not html_text:
        return ""
    clean = re.sub('<[^<]+?>', '', html_text)
    clean = html.unescape(clean)
    clean = re.sub(r'\s+', ' ', clean)
    return clean.strip()


def html_to_markdown(html_text):
    """Convert HTML to markdown, preserving links"""
    if not html_text:
        return ""

    text = html_text

    # Convert standard HTML links to markdown: <a href="url">text</a> -> [text](url)
    text = re.sub(r'<a\s+(?:[^>]*?\s+)?href=["\'](.*?)["\'](?:[^>]*?)>(.*?)</a>', r'[\2](\1)', text, flags=re.IGNORECASE)

    # Convert Confluence page links: <ac:link><ri:page ri:content-title="Page Title" /></ac:link>
    # Extract page title from Confluence links
    def replace_confluence_link(match):
        content_title = re.search(r'ri:content-title="([^"]+)"', match.group(0))
        if content_title:
            return f"[{content_title.group(1)}]"
        return match.group(0)

    text = re.sub(r'<ac:link>.*?</ac:link>', replace_confluence_link, text, flags=re.DOTALL)

    # Convert Confluence structured-macro children display to readable format
    children_macro = re.search(r'<ac:structured-macro\s+ac:name="children"[^>]*?/>', text)
    if children_macro:
        text = re.sub(r'<ac:structured-macro\s+ac:name="children"[^>]*?/>', '[Child Pages Listed Below]', text)

    # Handle other common Confluence macros
    text = re.sub(r'<ac:structured-macro\s+ac:name="([^"]+)"[^>]*?/>', r'[Macro: \1]', text)

    # Remove remaining XML/HTML tags
    text = re.sub('<[^<]+?>', '', text)

    # Clean up HTML entities
    text = html.unescape(text)

    # Clean up whitespace but preserve line breaks
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)

    return text.strip()
