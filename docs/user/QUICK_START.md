# Atlassian CLI - Quick Start Guide

## ✓ Installation Complete!

Your optimized Python CLI for Jira & Confluence is ready to use.

## File Locations

- **Main CLI**: `jira_cli_full.py` - Complete Jira + Confluence functionality
- **Config**: `~/.jira_cli/config.json` - Your credentials (already configured!)
- **Documentation**: `CLI_README.md` - Full command reference

## Most Common Commands

### Your Work
```bash
# See your tickets
python jira_cli_full.py ticket mine

# See current sprint (H&C)
python jira_cli_full.py sprint --component "ProductArea:H&C"

# Get ticket details
python jira_cli_full.py ticket get SD-5787
```

### Comments
```bash
# Add comment (opens editor)
python jira_cli_full.py comment add SD-5787

# Add comment directly
python jira_cli_full.py comment add SD-5787 "My update here"

# List comments
python jira_cli_full.py comment list SD-5787
```

### Update Tickets
```bash
# Move to In Progress
python jira_cli_full.py transition SD-5787 "In Progress"

# Update summary
python jira_cli_full.py edit SD-5787 --summary "New title"

# Assign to someone
python jira_cli_full.py edit SD-5787 --assignee "username"
```

### Search
```bash
# JQL search
python jira_cli_full.py ticket search "project = SD AND status = Open"

# Confluence search
python jira_cli_full.py confluence search "wildcat sprint review"
```

### Confluence
```bash
# Search Wildcat content
python jira_cli_full.py confluence search wildcat

# List spaces
python jira_cli_full.py confluence spaces --search "H&C"

# View page
python jira_cli_full.py confluence page 6725500929 --preview
```

## Configuration

```bash
# View config
python jira_cli_full.py config show

# Update config
python jira_cli_full.py config set

# Clear config
python jira_cli_full.py config clear
```

## Help

Get help for any command:
```bash
python jira_cli_full.py --help
python jira_cli_full.py ticket --help
python jira_cli_full.py comment --help
python jira_cli_full.py confluence --help
```

## Create an Alias (Recommended!)

### PowerShell
Add to your PowerShell profile:
```powershell
function jira { python C:\Users\kevin.mbuluko\projects\jira-discovery\jira_cli_full.py $args }
```

Then use simply:
```bash
jira ticket mine
jira comment add SD-5787 "My comment"
jira confluence search wildcat
```

To edit your profile:
```powershell
notepad $PROFILE
```

## Features

### Jira
- ✓ View & search tickets
- ✓ Add & list comments
- ✓ Edit fields (summary, description, assignee, priority)
- ✓ Transition tickets (change status)
- ✓ Quick commands (mine, sprint, projects)
- ✓ Full JQL support

### Confluence
- ✓ Search content
- ✓ List spaces
- ✓ View pages
- ✓ Read page content
- ✓ Find Wildcat documentation

### Configuration
- ✓ Secure credential storage
- ✓ Easy setup & management
- ✓ Environment variable support

## Example Workflow

```bash
# Check your tickets
python jira_cli_full.py ticket mine

# View one in detail
python jira_cli_full.py ticket get SD-5787 --full

# Move to In Progress
python jira_cli_full.py transition SD-5787 "In Progress"

# Add work update
python jira_cli_full.py comment add SD-5787 "Started implementation"

# Check sprint status
python jira_cli_full.py sprint --component "ProductArea:H&C"

# Find team docs
python jira_cli_full.py confluence search "wildcat playbook"
```

## Testing - Verified Working!

```
✓ Configuration saved
✓ Retrieved your tickets (SD-3283, SD-3432, SD-3792)
✓ Searched Confluence for Wildcat content
✓ Retrieved ticket details (SD-3589)
```

## Full Documentation

See `CLI_README.md` for complete command reference and advanced usage.

## Summary

You now have a powerful CLI tool that can:
1. **Read** Jira tickets, comments, and details
2. **Edit** ticket fields and update information
3. **Comment** on tickets with full text editor support
4. **Transition** tickets between statuses
5. **Search** using JQL and Confluence CQL
6. **Access** Confluence spaces and pages
7. **Configure** credentials securely

All from the command line! 🚀
