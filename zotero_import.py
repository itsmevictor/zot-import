#!/usr/bin/env python3.11
import sys
import os
import argparse
from pyzotero import zotero

# CONFIGURATION - Set these environment variables:
# ZOTERO_LIBRARY_ID - Your library ID (find at https://www.zotero.org/settings/keys)
# ZOTERO_API_KEY - Your API key (create at https://www.zotero.org/settings/keys/new)
# ZOTERO_LIBRARY_TYPE - 'user' or 'group' (defaults to 'user')
LIBRARY_ID = os.environ.get('ZOTERO_LIBRARY_ID')
LIBRARY_TYPE = os.environ.get('ZOTERO_LIBRARY_TYPE', 'user')
API_KEY = os.environ.get('ZOTERO_API_KEY')

def import_reference(title=None, item_type='journalArticle', collection_id=None, doi=None, authors=None, url=None):
    if not title and not doi:
        print("Error: You must provide at least a title or a DOI.")
        return

    if not LIBRARY_ID or not API_KEY:
        print("Error: ZOTERO_LIBRARY_ID and ZOTERO_API_KEY environment variables must be set.")
        print("Get your credentials at: https://www.zotero.org/settings/keys")
        return

    try:
        zot = zotero.Zotero(LIBRARY_ID, LIBRARY_TYPE, API_KEY)
    except Exception as e:
        print(f"Error initializing Zotero client: {e}")
        return

    # 1. Get a template for the item type
    print(f"Fetching template for '{item_type}'...")
    try:
        template = zot.item_template(item_type)
    except Exception as e:
        print(f"Error fetching template: {e}")
        return

    # 2. Fill in the data
    if title:
        template['title'] = title
    if doi:
        template['DOI'] = doi
    if url:
        template['url'] = url

    # Add authors if provided
    if authors:
        template['creators'] = []
        for author in authors:
            # Parse author string - accept "First Last" or "Last" format
            parts = author.strip().split(None, 1)  # Split on first whitespace
            if len(parts) == 2:
                template['creators'].append({
                    'creatorType': 'author',
                    'firstName': parts[0],
                    'lastName': parts[1]
                })
            else:
                # Single name - could be organization or single-name author
                template['creators'].append({
                    'creatorType': 'author',
                    'lastName': parts[0],
                    'firstName': ''
                })

    # 3. Add to collection if specified
    if collection_id:
        template['collections'] = [collection_id]
        
    # 4. Create the item
    print("Sending to Zotero...")
    try:
        resp = zot.create_items([template])
        # Pyzotero returns a dict with 'success', 'failed', 'unchanged'.
        # The 'success' key contains a dict mapping index to item key.
        if resp.get('success'):
            # Get the first (and only) item key from the success dict
            new_key = list(resp['success'].values())[0]
            print(f"✅ Successfully imported item: {new_key}")
            print(f"   Title: {title}")
        elif resp.get('failed'):
             print("❌ Import failed.")
             print(f"Failed items: {resp.get('failed')}")
        else:
            print("❌ Import result unclear or unchanged.")
            print(resp)
    except Exception as e:
        print(f"Error creating item: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import a reference to Zotero.")
    parser.add_argument("title", nargs="?", default=None, help="Title of the reference (optional if DOI provided)")
    parser.add_argument("--type", default="journalArticle", help="Item type (book, webpage, etc.)")
    parser.add_argument("--collection", help="Collection Key (e.g., ABC12345)")
    parser.add_argument("--doi", help="DOI of the reference (e.g., 10.1000/xyz123)")
    parser.add_argument("--author", action="append", dest="authors", help="Author name (can be used multiple times; format: 'First Last' or 'Last')")
    parser.add_argument("--url", help="URL to the resource")

    args = parser.parse_args()

    import_reference(args.title, args.type, args.collection, args.doi, args.authors, args.url)
