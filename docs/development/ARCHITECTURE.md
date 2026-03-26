# JC CLI Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User                                 │
│                    (PowerShell CLI)                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                       jc.py                                  │
│                  (Entry Point)                               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     jc/cli.py                                │
│              (CLI Group & Router)                            │
└─────┬──────────┬──────────┬──────────┬──────────┬───────────┘
      │          │          │          │          │
      ▼          ▼          ▼          ▼          ▼
   ┌──────┐ ┌─────────┐ ┌────────┐ ┌──────────┐ ┌─────────┐
   │config│ │ ticket  │ │comment │ │   edit   │ │confluence
   └──┬───┘ └────┬────┘ └───┬────┘ └────┬─────┘ └────┬────┘
      │          │          │          │          │
      │          │          │          │          │
      └──────────┴──────────┴──────────┴──────────┘
                         │
                         ▼
         ┌───────────────────────────────────┐
         │     jc/client.py                  │
         │   (AtlassianClient)               │
         │   • Jira API                      │
         │   • Confluence API                │
         │   • Config Management             │
         └─────────┬─────────────────────────┘
                   │
                   ├─────────────────┐
                   ▼                 ▼
         ┌──────────────┐   ┌───────────────┐
         │ jc/formatters.py│ │ ~/.jira_cli/  │
         │ • ADF Parser    │ │ config.json   │
         │ • HTML Cleaner  │ └───────────────┘
         └──────────────┘
                   │
                   ▼
         ┌──────────────────────┐
         │  Atlassian APIs      │
         │  • Jira REST API v3  │
         │  • Confluence API    │
         └──────────────────────┘
```

## Data Flow

### 1. Ticket Retrieval (with ADF Parsing)

```
User Command: jc ticket get SD-919 --full
       │
       ▼
jc/commands/ticket.py: ticket_get()
       │
       ├─→ client.jira.issue('SD-919')
       │         │
       │         ▼
       │   Jira API v3
       │         │
       │         ▼
       │   Returns: issue.raw['fields']['description'] (ADF)
       │
       ├─→ formatters.extract_text_from_adf(description)
       │         │
       │         ├─→ Recursively traverse ADF nodes
       │         ├─→ Extract text from each node
       │         ├─→ Replace emojis for console
       │         └─→ Return plain text
       │
       └─→ click.echo() → Display to user
```

### 2. Configuration Flow

```
User: jc config set
       │
       ▼
jc/commands/config.py: config_set()
       │
       ▼
client.save_config(server, email, token)
       │
       ├─→ Create ~/.jira_cli/ directory
       │
       └─→ Write config.json
             {
               "server": "https://company.atlassian.net",
               "email": "user@company.com",
               "api_token": "secret"
             }

Later, when accessing Jira:
       │
       ▼
client.jira (property)
       │
       ├─→ Load config from file
       ├─→ Override with ENV vars if present
       ├─→ Create JIRA() connection
       └─→ Return cached connection
```

### 3. Confluence Search Flow

```
User: jc confluence search "test query"
       │
       ▼
jc/commands/confluence.py: confluence_search_cmd()
       │
       ▼
client.confluence_search(query, limit)
       │
       ├─→ Build CQL query
       ├─→ Make HTTP request to Confluence API
       └─→ Return results with excerpts
              │
              ▼
       formatters.clean_html(excerpt)
              │
              ├─→ Remove HTML tags
              ├─→ Decode entities
              └─→ Return plain text
              │
              ▼
       click.echo() → Display to user
```

## Module Dependencies

```
┌─────────────┐
│   jc.py     │ (entry point)
└──────┬──────┘
       │ imports
       ▼
┌─────────────┐
│  jc/cli.py  │ (main CLI)
└──────┬──────┘
       │ imports all commands
       ▼
┌──────────────────────────────────────┐
│       jc/commands/*.py               │
│  (config, ticket, comment, etc.)     │
└──────┬─────────────────┬─────────────┘
       │                 │
       │ imports         │ imports
       ▼                 ▼
┌──────────────┐   ┌────────────────┐
│ jc/client.py │   │jc/formatters.py│
└──────────────┘   └────────────────┘

Dependencies:
• Commands depend on: client, formatters
• Client depends on: jira, requests
• Formatters depend on: re, html
• No circular dependencies ✅
```

## Component Responsibilities

### 1. **Entry Point (jc.py)**
- **Responsibility**: Launch CLI
- **Size**: 11 lines
- **Dependencies**: jc.cli

### 2. **CLI Router (jc/cli.py)**
- **Responsibility**: Register and route commands
- **Size**: 36 lines
- **Dependencies**: click, all command modules

### 3. **Client (jc/client.py)**
- **Responsibility**:
  - Manage Atlassian API connections
  - Handle authentication
  - Load/save configuration
- **Size**: 103 lines
- **Dependencies**: jira, requests, click

### 4. **Formatters (jc/formatters.py)**
- **Responsibility**:
  - Parse ADF (Atlassian Document Format)
  - Clean HTML
  - Format text for console display
- **Size**: 72 lines
- **Dependencies**: re, html

### 5. **Commands (jc/commands/*.py)**
- **Responsibility**: Implement CLI commands
- **Size**: 46-138 lines per module
- **Dependencies**: click, client, formatters

## Design Patterns Used

### 1. **Lazy Loading**
```python
@property
def jira(self):
    if self._jira is None:
        self._jira = JIRA(...)  # Only connect when needed
    return self._jira
```

### 2. **Singleton Pattern**
```python
# One global client instance
client = AtlassianClient()
```

### 3. **Command Pattern**
```python
@click.command('get')
def ticket_get(...):
    """Each command is self-contained"""
```

### 4. **Facade Pattern**
```python
# AtlassianClient provides simple interface to complex APIs
client.jira.issue('SD-123')
client.confluence_get('spaces')
```

### 5. **Strategy Pattern**
```python
# Different formatters for different content types
extract_text_from_adf(adf_content)
clean_html(html_content)
```

## Configuration Management

```
Priority Order (highest to lowest):
1. Environment Variables (JIRA_SERVER, JIRA_EMAIL, JIRA_API_TOKEN)
2. Config File (~/.jira_cli/config.json)
3. None (error if not configured)

Flow:
┌─────────────────┐
│ Check ENV vars  │
└────────┬────────┘
         │ if not set
         ▼
┌─────────────────┐
│ Load from file  │
└────────┬────────┘
         │ if not found
         ▼
┌─────────────────┐
│  Return empty   │
│    (prompt user)│
└─────────────────┘
```

## Error Handling Strategy

```
Level 1: Command Level
  ├─→ Try/except around main logic
  ├─→ Display user-friendly error message
  └─→ Exit gracefully (exit code 0 with error message)

Level 2: Client Level
  ├─→ Validate configuration before connecting
  ├─→ Lazy load to avoid unnecessary connections
  └─→ Let HTTP errors bubble up with context

Level 3: Formatter Level
  ├─→ Handle None/empty input gracefully
  ├─→ Return fallback text on parse errors
  └─→ Never crash on malformed input
```

## Performance Characteristics

### Startup Time
- **Cold start**: ~0.5s (module loading)
- **Warm start**: ~0.2s (Python cached)

### Command Execution
- **Simple commands** (config show): <0.1s
- **API commands** (ticket get): 0.5-2s (network dependent)
- **Search commands**: 1-5s (depends on result size)

### Memory Usage
- **Base**: ~30MB (Python + imports)
- **With API connection**: ~45MB
- **Peak during search**: ~60MB

## Testing Strategy

```
Test Pyramid:

              ┌────────────┐
              │  E2E Tests │  (Manual testing with real API)
              └────────────┘
           ┌──────────────────┐
           │ Integration Tests │  (Commands + Client mocked)
           └──────────────────┘
        ┌────────────────────────┐
        │     Unit Tests          │  (Individual functions)
        │  • ADF Parser (8 tests) │
        │  • HTML Cleaner (4 tests)│
        │  • Commands (20 tests)   │
        │  • Config (3 tests)      │
        │  • Client (2 tests)      │
        └────────────────────────┘

Coverage: 79% (426 statements, 89 missed)
```

## Extension Points

### 1. Adding New Commands
```python
# Create: jc/commands/newfeature.py
@click.group()
def newfeature():
    pass

@newfeature.command('action')
def action():
    pass

# Register in: jc/cli.py
cli.add_command(newfeature)
```

### 2. Adding New Formatters
```python
# Add to: jc/formatters.py
def format_markdown(md_text):
    """Convert markdown to plain text"""
    pass

# Use in commands
from jc.formatters import format_markdown
```

### 3. Adding New Client Methods
```python
# Add to: jc/client.py
def atlassian_get(self, product, endpoint):
    """Generic Atlassian API getter"""
    pass
```

## Security Considerations

1. **API Token Storage**
   - Stored in `~/.jira_cli/config.json`
   - File permissions: User-only (600)
   - Never logged or displayed

2. **Environment Variables**
   - Higher priority than file
   - Useful for CI/CD pipelines
   - Not persisted

3. **HTTPS Only**
   - All API calls use HTTPS
   - Certificate validation enabled

## Summary

The refactored architecture provides:
- ✅ Clear separation of concerns
- ✅ Modular, maintainable code
- ✅ Comprehensive test coverage (79%)
- ✅ 100% backward compatibility
- ✅ Easy extensibility
- ✅ Better performance through lazy loading
- ✅ Professional code organization
