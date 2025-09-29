import json
import os
import argparse
from datetime import datetime
import re

def sanitize_filename(name):
    """Convert a string to a safe filename"""
    # Remove or replace invalid characters
    name = re.sub(r'[<>:"/\\|?*]', '-', name)
    # Remove multiple spaces and hyphens
    name = re.sub(r'\s+', ' ', name)
    name = re.sub(r'-+', '-', name)
    # Trim and limit length
    name = name.strip()[:100]
    return name

def parse_trello_date(date_str):
    """Parse Trello date format to datetime object"""
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except:
        return None

def convert_to_markdown(json_file):
    # Load JSON data
    with open(json_file, 'r') as f:
        data = json.load(f)

    board_name = data.get('name', 'Untitled Board')
    lists = {lst['id']: lst for lst in data.get('lists', [])}
    cards = data.get('cards', [])


    print(f"Converting Trello board '{board_name}' to markdown...")
    print(f"Found {len(lists)} lists and {len(cards)} cards")

    # Create output directory
    output_dir = f"{sanitize_filename(board_name)}_markdown"
    os.makedirs(output_dir, exist_ok=True)

    # Find which lists have cards
    lists_with_cards = set(card.get('idList') for card in cards)

    # Create directories only for lists that have cards
    for list_id, list_data in lists.items():
        if list_id in lists_with_cards:
            list_name = list_data.get('name', 'Unknown List')
            list_dir = os.path.join(output_dir, sanitize_filename(list_name))
            os.makedirs(list_dir, exist_ok=True)
            print(f"Created directory: {list_dir}")

    # Process each card
    for card in cards:
        card_name = card.get('name', 'Untitled Card')
        card_desc = card.get('desc', '')
        list_id = card.get('idList')
        list_name = lists.get(list_id, {}).get('name', 'Unknown List')
        is_closed = card.get('closed', False)
        card_id = card.get('id')

        # Get the most recent date for last modified
        date_last_activity = parse_trello_date(card.get('dateLastActivity'))

        # Create markdown content with frontmatter
        frontmatter_lines = ["---"]

        if date_last_activity:
            modified_str = date_last_activity.strftime('%Y-%m-%d')
            frontmatter_lines.append(f"modified: {modified_str}")

        export_date = datetime.now().strftime('%Y-%m-%d')
        frontmatter_lines.append(f"exported: {export_date}")

        if is_closed:
            frontmatter_lines.append("deleted: true")

        frontmatter_lines.append("---")

        markdown_content = "\n".join(frontmatter_lines) + "\n"

        if card_desc:
            markdown_content += f"{card_desc}\n"
        else:
            markdown_content += f"(no description)\n"

        # Create safe filename and put it in the list directory
        filename = f"{sanitize_filename(card_name)}.md"
        list_dir = os.path.join(output_dir, sanitize_filename(list_name))
        filepath = os.path.join(list_dir, filename)

        # Write markdown file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        # Set file modification time if we have a date
        if date_last_activity:
            timestamp = date_last_activity.timestamp()
            os.utime(filepath, (timestamp, timestamp))
            print(f"Created: {filename} (modified: {date_last_activity.strftime('%Y-%m-%d %H:%M:%S')})")
        else:
            print(f"Created: {filename}")

    print(f"\nConversion complete! {len(cards)} markdown files created in '{output_dir}' directory")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert Trello board JSON export to Obsidian markdown files')
    parser.add_argument('json_file', help='Path to the Trello JSON export file')

    args = parser.parse_args()
    convert_to_markdown(args.json_file)

