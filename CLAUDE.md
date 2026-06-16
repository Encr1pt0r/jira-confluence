# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Shell Preference

Always use PowerShell 7 for commands in this project:
```
pwsh -Command "..."
```

## Setup

```powershell
pwsh -Command "pip install -r requirements.txt"
pwsh -Command "pip install -r requirements-test.txt"
```

## Running the CLI

```powershell
pwsh -Command "python jc.py --help"
```

## Testing

```powershell
# Full suite with coverage
pwsh -Command "python -m pytest test_jc.py --cov=jc --cov-report=term-missing"

# Single test method
pwsh -Command "python -m pytest test_jc.py::TestClassName::test_method_name -v"

# Tests matching a keyword
pwsh -Command "python -m pytest test_jc.py -k 'pattern' -v"

# Using the custom runner (supports categories: adf, commands, ticket)
pwsh -Command "python run_tests.py"
```

## Architecture

```
jc.py                  → entry point, calls jc.cli.cli()
jc/cli.py              → Click group that registers all command modules
jc/commands/           → one file per command group (ticket, comment, edit,
                         confluence, project, config)
jc/client.py           → AtlassianClient: wraps the jira library + requests
                         for Confluence; uses lazy @property for connections
jc/formatters.py       → ADF→text, HTML→text, HTML→Markdown converters
test_jc.py             → full test suite (~1 000 lines); all API calls mocked
run_tests.py           → helper runner with category filters
```

**Data flow:** CLI command → `jc/commands/*.py` → `AtlassianClient` (single global instance) → Jira REST API v3 / Confluence API v2 → formatters → terminal output.

**Configuration** is stored in `~/.jira_cli/config.json`; environment variables take priority over the file.

## Test Suite Structure

| Test class | Covers |
|---|---|
| `TestADFTextExtraction` | ADF node parsing, emoji replacement |
| `TestCleanHTML` | Tag removal, entity decoding |
| `TestHTMLToMarkdown` | Link/macro conversion |
| `TestConfigCommands` | `jc config set/show/clear` |
| `TestTicketCommands` | `jc ticket get/search/mine` |
| `TestCommentCommands` | `jc comment add/list` |
| `TestEditCommands` | `jc edit`, `jc transition` |
| `TestConfluenceCommands` | `jc confluence spaces/pages/page/search` |
| `TestProjectCommands` | `jc projects`, `jc sprint` |
| `TestErrorHandling` | API failures, missing config |
| `TestAtlassianClient` | Client init and config loading |

## Documentation

User-facing docs live in `docs/user/`; developer docs (architecture decisions, test strategy, refactoring notes) live in `docs/development/`. Update `docs/user/CLI_README.md` and `docs/user/CHEATSHEET.md` when adding or changing commands.

## TDD Policy

Write tests before or immediately after implementing any feature. Run them right away—never assume untested code works. All new CLI commands require both unit tests (mock the API) and coverage of error paths.
