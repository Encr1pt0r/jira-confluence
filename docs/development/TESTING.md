# Testing Guide for JC CLI

This document describes the testing setup and how to run tests for the JC CLI tool.

## Test Coverage

The test suite covers:

### 1. **ADF Text Extraction** (`TestADFTextExtraction`)
- Simple text extraction
- Formatted text (bold, italic)
- Headings at different levels
- Bullet and numbered lists
- Nested structures
- Empty content handling
- Emoji replacement for Windows console compatibility
- Complex nested ADF structures

### 2. **HTML Cleaning** (`TestCleanHTML`)
- Basic HTML tag removal
- HTML entity decoding
- Whitespace normalization
- Empty content handling

### 2b. **HTML to Markdown Conversion** (`TestHTMLToMarkdown`)
- Converting standard HTML links to markdown format
- Converting multiple links in content
- Converting Confluence page links
- Converting Confluence macros (children, toc, etc.)
- Preserving text content alongside links
- HTML entity decoding in links
- Empty content handling

### 3. **Configuration Commands** (`TestConfigCommands`)
- `config set` - Setting credentials
- `config show` - Displaying configuration (with token masking)
- `config clear` - Clearing stored credentials

### 4. **Ticket Commands** (`TestTicketCommands`)
- `ticket get` - Getting basic ticket info
- `ticket get --full` - Getting ticket with full description
- `ticket search` - Searching with JQL
- `ticket mine` - Listing assigned tickets
- Empty result handling

### 5. **Comment Commands** (`TestCommentCommands`)
- `comment add` - Adding comments to tickets
- `comment list` - Listing ticket comments with ADF parsing

### 6. **Edit Commands** (`TestEditCommands`)
- `edit --summary` - Updating ticket summary
- `edit --assignee` - Changing assignee
- `transition` - Listing available transitions
- `transition <status>` - Executing status transitions

### 7. **Confluence Commands** (`TestConfluenceCommands`)
- `confluence spaces` - Listing spaces
- `confluence pages` - Listing pages in a space
- `confluence page` - Getting page details with content
- `confluence from-url` - Getting page details from URL
- `confluence from-url --preview` - Getting page with content preview
- `confluence from-url --children` - Getting page with child pages
- `confluence from-url` with invalid URL - Error handling
- `confluence_get_children()` - Client method for fetching child pages
- `confluence search` - Searching Confluence content

### 8. **Project Commands** (`TestProjectCommands`)
- `projects` - Listing all projects
- `projects --search` - Searching projects
- `sprint` - Viewing sprint tickets

### 9. **Error Handling** (`TestErrorHandling`)
- Non-existent tickets
- Invalid JQL queries
- Missing configuration
- API errors

### 10. **Client Configuration** (`TestAtlassianClient`)
- Loading config from file
- Environment variable overrides
- Config file validation

## Setup

1. Install test dependencies:
```powershell
pip install -r requirements-test.txt
```

2. Ensure pytest is available:
```powershell
python -m pytest --version
```

## Running Tests

### Quick Start

Run all tests with coverage:
```powershell
python run_tests.py
```

### Test Runner Options

```powershell
# Run all tests with coverage report
python run_tests.py all

# Quick run without coverage (faster)
python run_tests.py quick

# Run only ADF parsing tests
python run_tests.py adf

# Run only CLI command tests
python run_tests.py commands

# Run specific test by name
python run_tests.py test_emoji
python run_tests.py ticket
```

### Using pytest directly

```powershell
# Run all tests with verbose output
python -m pytest test_jc.py -v

# Run specific test class
python -m pytest test_jc.py::TestADFTextExtraction -v

# Run specific test method
python -m pytest test_jc.py::TestADFTextExtraction::test_emoji_replacement -v

# Run with coverage
python -m pytest test_jc.py --cov=jc --cov-report=term-missing

# Run tests matching a pattern
python -m pytest test_jc.py -k "ticket" -v
```

## Coverage Reports

After running tests with coverage, you'll get:

1. **Terminal output** - Shows line-by-line coverage
2. **HTML report** - Detailed visual coverage report

To view the HTML report:
```powershell
# After running: python run_tests.py all
start htmlcov/index.html
```

## Test Structure

Each test class focuses on a specific area:

```python
class TestADFTextExtraction:      # Unit tests for ADF parsing
class TestCleanHTML:              # Unit tests for HTML cleaning
class TestConfigCommands:         # Integration tests for config commands
class TestTicketCommands:         # Integration tests for ticket commands
class TestCommentCommands:        # Integration tests for comment commands
class TestEditCommands:           # Integration tests for edit commands
class TestConfluenceCommands:     # Integration tests for Confluence commands
class TestProjectCommands:        # Integration tests for project commands
class TestErrorHandling:          # Tests for error scenarios
class TestAtlassianClient:        # Tests for client configuration
```

## Mocking Strategy

Tests use `unittest.mock` to mock external dependencies:

- **Jira API calls** - Mocked to avoid real API calls
- **File system** - Mocked for config file operations
- **HTTP requests** - Mocked for Confluence API calls

This ensures:
- Tests run fast (no network calls)
- Tests are deterministic (no external dependencies)
- Tests can run offline
- No real data is affected

## Key Features Tested

### 1. Text Readability from Command Line
Tests verify that:
- ADF descriptions are properly converted to readable text
- Emojis are replaced with console-safe alternatives
- Line breaks and formatting are preserved
- Long content is properly truncated

### 2. All CLI Commands
Every command and flag is tested:
- ✅ Configuration management
- ✅ Ticket operations (get, search, mine)
- ✅ Comment operations (add, list)
- ✅ Editing (summary, assignee, priority)
- ✅ Status transitions
- ✅ Confluence operations (spaces, pages, page details, from-url with all options, search)
- ✅ HTML to Markdown conversion (links, macros, entities)
- ✅ Project listing
- ✅ Sprint viewing

### 3. Error Handling
Tests ensure proper error messages for:
- Missing tickets
- Invalid queries
- Missing configuration
- API failures

## Continuous Improvement

To add new tests:

1. Add test methods to appropriate test class
2. Use descriptive test names: `test_<feature>_<scenario>`
3. Follow the Arrange-Act-Assert pattern
4. Mock external dependencies
5. Assert on both exit codes and output content

## Troubleshooting

**Import errors:**
```powershell
# Ensure you're in the project directory
cd C:\Users\kevin.mbuluko\projects\jira-discovery
python -m pytest test_jc.py -v
```

**Mock issues:**
- Ensure you're mocking at the correct level (client._jira vs client.jira)
- Check that patches match the actual import paths

**Coverage not showing:**
```powershell
# Ensure coverage is installed
pip install pytest-cov

# Run with explicit coverage
python -m pytest test_jc.py --cov=jc --cov-report=html
```
