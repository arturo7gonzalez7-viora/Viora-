#!/usr/bin/env python3
"""
Generate a quick preview link for HTML files.
Uploads to transfer.sh for instant sharing.
"""

import sys
import os
import subprocess
import urllib.request
import urllib.parse
from pathlib import Path

def upload_to_transfer(filepath):
    """Upload file to transfer.sh and return the URL."""
    filename = os.path.basename(filepath)
    
    with open(filepath, 'rb') as f:
        content = f.read()
    
    # Upload to transfer.sh
    req = urllib.request.Request(
        f'https://transfer.sh/{filename}',
        data=content,
        headers={'Content-Type': 'text/html'},
        method='PUT'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            url = resp.read().decode().strip()
            return url
    except Exception as e:
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: html-preview.py <html-file>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    print(f"📤 Uploading {filepath}...", file=sys.stderr)
    url = upload_to_transfer(filepath)
    
    if url:
        print(f"✅ Preview ready!", file=sys.stderr)
        print(f"🔗 {url}", file=sys.stderr)
        print(url)  # Print just the URL to stdout for piping
    else:
        print("❌ Upload failed", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
