# JC - Jira & Confluence CLI

Super fast command-line tool for Atlassian Jira and Confluence.

## Quick Setup

### 1. Install 
```bash
pip install -r requirements.txt
```

### 2. Configure 
```bash
python jc.py config show
```

### 3. Create Alias (Recommended)

**PowerShell** - Add to your profile:
```powershell
function jc { python /path/to/jira-discovery/jc.py $args }
```

Replace `/path/to/jira-discovery` with your actual installation path.

To edit profile: `notepad $PROFILE`

**Then restart PowerShell and use:**
```bash
jc ticket mine
jc comment add SD-5787 "My update"
jc sprint
```

## Common Commands

### Your Work
```bash
jc ticket mine                    # Your tickets
jc ticket get SD-5787            # Ticket details
jc ticket get SD-5787 --full     # Full details + description
jc ticket get SD-5787 --comments # Include comments
```

### Search
```bash
jc ticket search "project = SD AND status = Open"
jc ticket search "assignee = currentUser() AND status != Done"
jc sprint                                    # Current sprint
jc sprint --component "ProductArea:H&C"     # Wildcat sprint
```

### Comments
```bash
jc comment add SD-5787                    # Opens editor
jc comment add SD-5787 "My comment"       # Direct comment
jc comment list SD-5787                   # Show comments
```

### Edit Tickets
```bash
jc edit SD-5787 --summary "New title"
jc edit SD-5787 --assignee "username"
jc edit SD-5787 --priority "High"
jc transition SD-5787                     # Show available transitions
jc transition SD-5787 "In Progress"      # Change status
jc transition SD-5787 "Done"             # Mark complete
```

### Confluence
```bash
jc confluence search "wildcat sprint review"
jc confluence spaces --search "H&C"
jc confluence pages AHC
jc confluence page 6725500929 --preview
```

### Projects
```bash
jc projects                     # List all
jc projects --search "health"   # Search projects
```

## All Commands

```bash
jc --help                  # Show all commands
jc config --help          # Config commands
jc ticket --help          # Ticket commands
jc comment --help         # Comment commands
jc confluence --help      # Confluence commands
```

## Configuration

```bash
jc config show            # View settings
jc config set             # Update credentials
jc config clear           # Remove credentials
```

## JQL Examples

```bash
# Open bugs assigned to you
jc ticket search "assignee = currentUser() AND type = Bug AND status = Open"

# H&C tickets in current sprint
jc ticket search "project = SD AND component = 'ProductArea:H&C' AND sprint in openSprints()"

# High priority tickets
jc ticket search "priority = High AND status != Done"

# Recently updated
jc ticket search "updated >= -7d ORDER BY updated DESC"
```

## Wildcat Team Quick Commands

```bash
# Current sprint
jc sprint --component "ProductArea:H&C"

# Search for your H&C tickets
jc ticket search "assignee = currentUser() AND component = 'ProductArea:H&C'"

# Find Wildcat docs
jc confluence search "wildcat"
jc confluence search "wildcat sprint review"
jc confluence search "wildcat playbook"

# View sprint review
jc confluence page 6725500929 --preview
```

## Features

**Jira:**
- ✓ View, search, list tickets
- ✓ Add & manage comments
- ✓ Edit all ticket fields
- ✓ Transition tickets (change status)
- ✓ Full JQL support
- ✓ Quick shortcuts (mine, sprint)

**Confluence:**
- ✓ Search all content
- ✓ Browse spaces
- ✓ View pages with preview
- ✓ Find team documentation

**Config:**
- ✓ Secure credential storage (~/.jira_cli/config.json)
- ✓ Easy setup and management
- ✓ Environment variable support

## Documentation

📚 **More Documentation**: See the [`docs/`](docs/) folder for comprehensive documentation:
- **User Guides**: [`docs/user/`](docs/user/) - Getting started, CLI reference, cheatsheet
- **Development**: [`docs/development/`](docs/development/) - Architecture, testing, refactoring
- **Features**: [`docs/features/`](docs/features/) - Feature-specific documentation
- **Examples**: [`docs/examples/`](docs/examples/) - Sample outputs and exports

## Project Structure

- **jc.py** - Main CLI entry point
- **jc/** - Core application package
  - **commands/** - Command implementations
  - **client.py** - Jira/Confluence API client
  - **cli.py** - CLI framework
  - **formatters.py** - Output formatting
- **test_jc.py** - Comprehensive test suite
- **docs/** - All documentation
- **playground/** - Experimental scripts

## Example Workflow

```bash
# Morning standup prep
jc ticket mine
jc sprint --component "ProductArea:H&C"

# Work on a ticket
jc ticket get SD-5787 --full
jc transition SD-5787 "In Progress"
jc comment add SD-5787 "Started working on this"

# Update during the day
jc comment add SD-5787 "Fixed the main issue, testing now"

# Complete the ticket
jc transition SD-5787 "Done"
jc comment add SD-5787 "Completed and tested"

# Find team docs
jc confluence search "wildcat playbook"
``

## Support

Get help anytime:
```bash
jc --help
jc ticket --help
jc comment --help
jc confluence --help
```

---

**JC** - Jira Confluence CLI
Fast. Simple. Powerful. 🚀
