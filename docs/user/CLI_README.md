# Atlassian CLI - Complete Jira & Confluence Command-Line Tool

A powerful, optimized Python CLI for managing Jira tickets and Confluence pages from the command line.

## Features

### Jira Operations
- ✓ View, search, and list tickets
- ✓ Add comments to tickets
- ✓ Edit ticket fields (summary, description, assignee, priority)
- ✓ Transition tickets between statuses
- ✓ Assign tickets to users
- ✓ Quick commands for your tickets and current sprint

### Confluence Operations
- ✓ List and search spaces
- ✓ View pages in a space
- ✓ Read page content
- ✓ Get page details from URL (with child pages support)
- ✓ Search across all Confluence content

### Configuration
- ✓ Secure credential storage
- ✓ Easy configuration management
- ✓ Environment variable support

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Configure credentials
```bash
python jira_cli_full.py config set
```

You'll be prompted for:
- **Server URL**: `https://yourcompany.atlassian.net`
- **Email**: Your Atlassian email
- **API Token**: Generate from https://id.atlassian.com/manage-profile/security/api-tokens

### 2. View your configuration
```bash
python jira_cli_full.py config show
```

## Usage Examples

### Configuration Commands

```bash
# Set up credentials
python jira_cli_full.py config set

# Show current config
python jira_cli_full.py config show

# Clear stored config
python jira_cli_full.py config clear
```

### Jira Ticket Commands

```bash
# Get ticket details
python jira_cli_full.py ticket get SD-5787

# Get ticket with comments
python jira_cli_full.py ticket get SD-5787 --comments

# Get full ticket details
python jira_cli_full.py ticket get SD-5787 --full

# Search tickets with JQL
python jira_cli_full.py ticket search "project = SD AND status = Open"

# Search with custom limit
python jira_cli_full.py ticket search "assignee = currentUser()" --limit 20

# Show your assigned tickets
python jira_cli_full.py ticket mine

# Show more of your tickets
python jira_cli_full.py ticket mine --limit 20
```

### Comment Commands

```bash
# Add a comment (opens text editor)
python jira_cli_full.py comment add SD-5787

# Add comment directly
python jira_cli_full.py comment add SD-5787 "This is my comment"

# Add comment from file
python jira_cli_full.py comment add SD-5787 --file comment.txt

# List comments on a ticket
python jira_cli_full.py comment list SD-5787
```

### Edit Commands

```bash
# Update summary
python jira_cli_full.py edit SD-5787 --summary "New summary text"

# Update description
python jira_cli_full.py edit SD-5787 --description "New description"

# Change assignee
python jira_cli_full.py edit SD-5787 --assignee "kevin.mbuluko"

# Update priority
python jira_cli_full.py edit SD-5787 --priority "High"

# Update multiple fields
python jira_cli_full.py edit SD-5787 --summary "New title" --priority "High" --assignee "kevin.mbuluko"
```

### Transition Commands

```bash
# Show available transitions
python jira_cli_full.py transition SD-5787

# Transition to a status
python jira_cli_full.py transition SD-5787 "In Progress"

# Common transitions
python jira_cli_full.py transition SD-5787 "Done"
python jira_cli_full.py transition SD-5787 "In Development"
python jira_cli_full.py transition SD-5787 "Open"
```

### Confluence Commands

```bash
# List all spaces
python jira_cli_full.py confluence spaces

# Search for spaces
python jira_cli_full.py confluence spaces --search "wildcat"
python jira_cli_full.py confluence spaces --search "H&C"

# List pages in a space
python jira_cli_full.py confluence pages AHC

# Search pages by title
python jira_cli_full.py confluence pages AHC --search "sprint review"

# View page details
python jira_cli_full.py confluence page 6725500929

# View page with content preview
python jira_cli_full.py confluence page 6725500929 --preview

# Get page from URL (extracts page ID automatically)
python jira_cli_full.py confluence from-url "https://your-domain.atlassian.net/wiki/spaces/SPACE/pages/123456789/Page-Title"

# Get page from URL with content preview
python jira_cli_full.py confluence from-url "URL" --preview

# Get page from URL and show child pages (auto-detects "children" macro)
python jira_cli_full.py confluence from-url "URL" --preview

# Explicitly show child pages
python jira_cli_full.py confluence from-url "URL" --children

# Export full content to file (NO TRUNCATION)
python jira_cli_full.py confluence from-url "URL" --output mypage.md
python jira_cli_full.py confluence from-url "URL" -o mypage.md

# Open page in browser
python jira_cli_full.py confluence from-url "URL" --open

# Search Confluence content
python jira_cli_full.py confluence search "wildcat sprint review"
python jira_cli_full.py confluence search "ticket report"
```

### Quick Commands

```bash
# List all projects
python jira_cli_full.py projects

# Search projects
python jira_cli_full.py projects --search "health"

# Show current sprint tickets (default project: SD)
python jira_cli_full.py sprint

# Show sprint for specific project
python jira_cli_full.py sprint --project PP

# Filter sprint by component
python jira_cli_full.py sprint --project SD --component "ProductArea:H&C"
```

## Advanced Usage

### JQL Search Examples

```bash
# Find open bugs assigned to you
python jira_cli_full.py ticket search "assignee = currentUser() AND type = Bug AND status = Open"

# Find high priority tickets in H&C
python jira_cli_full.py ticket search "project = SD AND component = 'ProductArea:H&C' AND priority = High"

# Find recently updated tickets
python jira_cli_full.py ticket search "updated >= -7d ORDER BY updated DESC" --limit 20

# Find tickets in current sprint
python jira_cli_full.py ticket search "sprint in openSprints() ORDER BY priority DESC"
```

### Workflow Examples

**Daily standup preparation:**
```bash
# Check your tickets
python jira_cli_full.py ticket mine

# Check current sprint
python jira_cli_full.py sprint --component "ProductArea:H&C"

# Add standup update
python jira_cli_full.py comment add SD-5787 "Standup: Working on implementation, blocked by X"
```

**Updating a ticket:**
```bash
# Move to In Progress and assign to yourself
python jira_cli_full.py transition SD-5787 "In Progress"
python jira_cli_full.py edit SD-5787 --assignee "kevin.mbuluko"

# Add work log comment
python jira_cli_full.py comment add SD-5787 "Started work on feature X"
```

**Finding documentation:**
```bash
# Search Wildcat space
python jira_cli_full.py confluence spaces --search wildcat

# Find sprint reviews
python jira_cli_full.py confluence search "wildcat sprint review"

# View specific page
python jira_cli_full.py confluence page 6725500929 --preview
```

## Creating an Alias (Optional)

For easier usage, create an alias:

### Windows (PowerShell)
Add to your PowerShell profile:
```powershell
function jira { python C:\Users\kevin.mbuluko\projects\jira-discovery\jira_cli_full.py $args }
```

Then use:
```bash
jira ticket get SD-5787
jira comment add SD-5787 "My comment"
jira sprint --component "ProductArea:H&C"
```

### Linux/Mac (Bash/Zsh)
Add to `~/.bashrc` or `~/.zshrc`:
```bash
alias jira='python /path/to/jira_cli_full.py'
```

## Configuration File Location

Configuration is stored at:
- **Windows**: `C:\Users\<username>\.jira_cli\config.json`
- **Linux/Mac**: `~/.jira_cli/config.json`

## Security Notes

- API tokens are stored locally in your home directory
- Never commit `config.json` to version control
- API tokens can be revoked at: https://id.atlassian.com/manage-profile/security/api-tokens

## Troubleshooting

**Error: Not configured**
```bash
python jira_cli_full.py config set
```

**Error: JiraError HTTP 400**
- Check your JQL syntax
- Ensure field names are correct
- Verify you have access to the project

**Error: Page not found**
- Verify the page ID is correct
- Check you have permission to view the page

## Help

View help for any command:
```bash
python jira_cli_full.py --help
python jira_cli_full.py ticket --help
python jira_cli_full.py comment --help
python jira_cli_full.py confluence --help
```

## Example Workflow

```bash
# 1. Configure (first time only)
python jira_cli_full.py config set

# 2. Check your tickets
python jira_cli_full.py ticket mine

# 3. View a specific ticket
python jira_cli_full.py ticket get SD-5787 --full

# 4. Move ticket to In Progress
python jira_cli_full.py transition SD-5787 "In Progress"

# 5. Add a comment
python jira_cli_full.py comment add SD-5787 "Working on this now"

# 6. Check sprint status
python jira_cli_full.py sprint --component "ProductArea:H&C"

# 7. Find team documentation
python jira_cli_full.py confluence search "wildcat playbook"

# 8. Read a page
python jira_cli_full.py confluence page 6809255976 --preview
```

## Features Comparison

| Feature | Basic CLI | Full CLI |
|---------|-----------|----------|
| View tickets | ✓ | ✓ |
| Search tickets | ✓ | ✓ |
| Add comments | ✓ | ✓ |
| Edit tickets | ✓ | ✓ |
| Transitions | ✓ | ✓ |
| Confluence spaces | ✗ | ✓ |
| Confluence pages | ✗ | ✓ |
| Confluence search | ✗ | ✓ |
| Color output | ✓ | ✓ |
| Config management | ✓ | ✓ |

Use `jira_cli_full.py` for complete Jira + Confluence functionality!
