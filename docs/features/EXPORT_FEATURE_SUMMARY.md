# Confluence Export Feature Summary

## New Feature: `--output` / `-o` Flag

Export full Confluence page content to markdown files **without truncation**.

---

## Usage

### Basic Export
```bash
jc confluence from-url "URL" --output filename.md
jc confluence from-url "URL" -o filename.md
```

### Combined with Other Options
```bash
# Export with browser open
jc confluence from-url "URL" -o file.md --open

# Export with preview in terminal
jc confluence from-url "URL" -o file.md --preview
```

---

## Features

### ✅ No Truncation
- Terminal preview: Shows first 1500 characters (truncated)
- File export: **Complete content, no truncation**

### ✅ Markdown Formatted
- Title as H1
- Metadata (Page ID, Space ID, URL)
- Child pages as numbered list with markdown links
- Full content section

### ✅ Auto-includes Child Pages
- Automatically fetches child pages when exporting
- Each child page listed with clickable markdown link

### ✅ Preserves Links
- HTML links converted to markdown format: `[text](url)`
- Confluence macros converted to readable text
- All URLs are absolute and clickable

---

## Examples from Testing

### Example 1: Parent Page with Children

**Command:**
```bash
jc confluence from-url 'https://advancedcsg.atlassian.net/wiki/spaces/DS2/pages/3960602729/CFIA+SOPs' -o cfia_sops_full.md
```

**Output File:** `cfia_sops_full.md` (1.6 KB)
```markdown
# CFIA SOPs

**Page ID:** 3960602729
**Space ID:** 3992813949
**URL:** https://advancedcsg.atlassian.net/wiki/spaces/DS2/pages/3960602729/CFIA+SOPs

---

## Child Pages

1. [CFIASOP0 - CFIA Document](https://advancedcsg.atlassian.net/wiki/pages/3960602734)
2. [CFIASOP1](https://advancedcsg.atlassian.net/wiki/pages/3960602750)
... (15 total child pages)

---

## Content

[Child Pages Listed Below]
```

### Example 2: Content Page (Full Content)

**Command:**
```bash
jc confluence from-url 'https://advancedcsg.atlassian.net/wiki/spaces/DS2/pages/3960602774/CFIASOP8+Aurora+Database+Data' -o cfiasop8_full.md
```

**Output File:** `cfiasop8_full.md` (2.6 KB)
- Complete SOP procedure with all steps
- All links preserved in markdown format
- No content truncation
- Includes link to AWS console: `[docman-db-instance-eu-west-2a](https://eu-west-2.console.aws.amazon.com/...)`

---

## Comparison: Preview vs Export

| Feature | `--preview` | `--output file.md` |
|---------|-------------|-------------------|
| Content Display | Terminal | File |
| Truncation | Yes (1500 chars) | **No** |
| Child Pages | Yes | Yes |
| Links | Markdown format | Markdown format |
| Use Case | Quick view | Full export for documentation |

---

## Use Cases

### 1. Documentation Export
Export Confluence pages for offline documentation:
```bash
jc confluence from-url "URL" -o docs/procedure.md
```

### 2. Batch Export with Child Pages
Export a parent page to get a table of contents with links:
```bash
jc confluence from-url "URL" -o toc.md
```
The file will contain all child page links ready for copy-paste.

### 3. Content Backup
Create markdown backups of important pages:
```bash
jc confluence from-url "URL" -o backups/important-page-$(date +%Y%m%d).md
```

### 4. Import to Other Systems
Export pages to markdown for import into:
- GitHub/GitLab wikis
- Static site generators (Hugo, Jekyll)
- Documentation tools (MkDocs, Docusaurus)
- Note-taking apps (Obsidian, Notion)

---

## Technical Details

### File Format
- **Encoding:** UTF-8
- **Format:** Markdown (.md)
- **Line Endings:** Platform-specific

### Content Processing
1. Fetch page with `body-format=storage`
2. Convert HTML to markdown
3. Fetch child pages if present
4. Format as structured markdown
5. Write complete content to file

### Error Handling
- Invalid URL: Error message with format help
- API errors: Graceful error message
- File write errors: Clear error with file path

---

## Test Coverage

### Added Tests (2 new tests)
1. `test_confluence_from_url_with_output` - Full export with child pages
2. `test_confluence_from_url_with_output_no_children` - Export without child pages

### Test Results
✅ All 53 tests passing

---

## Documentation Updated
- ✅ CLI_README.md - Added export examples
- ✅ CHEATSHEET.md - Added `-o` command
- ✅ TESTING.md - Added test descriptions
- ✅ This summary document

---

## Quick Reference

```bash
# Terminal preview (truncated)
jc confluence from-url "URL" --preview

# Full export to file (no truncation)
jc confluence from-url "URL" -o file.md

# Both preview + export
jc confluence from-url "URL" --preview -o file.md
```

**Pro Tip:** Use `-o` flag for complete content. Use `--preview` for quick checks.

---

Generated: 2026-03-25
Feature Version: 1.0.0
