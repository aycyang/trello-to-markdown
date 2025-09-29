# Trello to Obsidian Markdown Migration Script

**Warning:** 100% vibecoded. I haven't tested this on any data other than my own. Use at your own risk.

A Python script that converts Trello JSON exports to Obsidian-compatible markdown files with proper organization and metadata.

## Features

- Converts Trello cards to individual markdown files
- Organizes files by Trello lists into directory structure
- Adds YAML frontmatter with metadata:
  - `modified`: Last activity date from Trello
  - `exported`: Date when the migration was performed
  - `deleted`: Boolean flag for cards that were deleted in Trello
- Preserves file modification times from Trello data
- Sanitizes filenames for filesystem compatibility
- Handles cards with and without descriptions

## Usage

1. Export your Trello board as JSON from Trello (Board Menu → More → Print and Export → Export as JSON)
2. Run the script with your JSON export file as an argument:

```bash
python3 migrate.py your-trello-export.json
```

The script will create a directory named `[BoardName]_markdown` containing subdirectories for each Trello list with cards.

## Output Format

Each card becomes a markdown file with YAML frontmatter:

```yaml
---
modified: 2024-11-05
exported: 2025-09-28
deleted: true
---
Card description content here
```

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)
