# JC Command Cheatsheet

## Setup
```bash
python jc.py config show                    # View config
python jc.py config set                     # Update config
```

## Tickets
```bash
jc ticket mine                              # Your tickets
jc ticket mine --limit 20                   # More results
jc ticket get SD-5787                       # View ticket
jc ticket get SD-5787 --full                # Full details
jc ticket get SD-5787 --comments            # Include comments
jc ticket search "JQL query"                # JQL search
```

## Comments
```bash
jc comment add SD-5787                      # Opens editor
jc comment add SD-5787 "text"               # Direct comment
jc comment list SD-5787                     # Show comments
```

## Edit
```bash
jc edit SD-5787 --summary "New title"
jc edit SD-5787 --assignee "username"
jc edit SD-5787 --priority "High"
jc edit SD-5787 --description "New desc"
```

## Status
```bash
jc transition SD-5787                       # Show options
jc transition SD-5787 "In Progress"
jc transition SD-5787 "Done"
```

## Sprint
```bash
jc sprint                                   # Current sprint (SD)
jc sprint --project PP                      # Different project
jc sprint --component "ProductArea:H&C"     # Filter by component
```

## Confluence
```bash
jc confluence search "query"                # Search content
jc confluence spaces                        # List spaces
jc confluence spaces --search "text"        # Search spaces
jc confluence pages AHC                     # Pages in space
jc confluence page 123456                   # View page
jc confluence page 123456 --preview         # With content
jc confluence from-url "URL"                # Get page from URL
jc confluence from-url "URL" --preview      # With content & child pages
jc confluence from-url "URL" --children     # Show child pages
jc confluence from-url "URL" -o file.md     # Export to file (FULL, no truncation)
jc confluence from-url "URL" --open         # Open in browser
```

## Projects
```bash
jc projects                                 # List all
jc projects --search "health"               # Search projects
```

## JQL Examples
```bash
# Your open tickets
jc ticket search "assignee = currentUser() AND status != Done"

# H&C tickets
jc ticket search "component = 'ProductArea:H&C' AND sprint in openSprints()"

# High priority
jc ticket search "priority = High AND status = Open"

# Recently updated
jc ticket search "updated >= -7d ORDER BY updated DESC"

# Bugs assigned to you
jc ticket search "assignee = currentUser() AND type = Bug"
```

## Wildcat Team Shortcuts
```bash
jc sprint --component "ProductArea:H&C"
jc ticket search "assignee = currentUser() AND component = 'ProductArea:H&C'"
jc confluence search "wildcat"
jc confluence search "wildcat sprint review"
jc confluence page 6725500929 --preview
jc confluence from-url "https://advancedcsg.atlassian.net/wiki/spaces/DS2/pages/3960602729" --preview
```

## Common Workflows

### Start work on ticket
```bash
jc ticket get SD-5787 --full
jc transition SD-5787 "In Progress"
jc comment add SD-5787 "Started working on this"
```

### Update progress
```bash
jc comment add SD-5787 "Fixed main issue, testing now"
```

### Complete ticket
```bash
jc transition SD-5787 "Done"
jc comment add SD-5787 "Completed and tested"
```

### Daily standup prep
```bash
jc ticket mine
jc sprint --component "ProductArea:H&C"
```

## Help
```bash
jc --help                                   # All commands
jc ticket --help                            # Ticket help
jc comment --help                           # Comment help
jc confluence --help                        # Confluence help
```

## Alias Setup (One Time)
```powershell
notepad $PROFILE
```
Add:
```powershell
function jc { python C:\Users\kevin.mbuluko\projects\jira-discovery\jc.py $args }
```
Save, restart PowerShell.

---
**JC - Jira Confluence CLI** | Fast. Simple. Powerful.
