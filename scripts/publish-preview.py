#!/usr/bin/env python3
"""
Publish HTML preview and return clickable URL.
Usage: python3 publish-preview.py <html-file-or-content>
"""

import sys
import os
import subprocess
import time
from pathlib import Path
from datetime import datetime
import hashlib

PREVIEW_DIR = Path("/root/.openclaw/workspace/output/previews")
PREVIEW_PORT = 8765
TUNNEL_URL_FILE = "/tmp/preview-tunnel-url.txt"

def ensure_preview_server():
    """Ensure preview server + tunnel are running."""
    # Check if server is running
    result = subprocess.run(
        ["pgrep", "-f", f"python3.*http.server.*{PREVIEW_PORT}"],
        capture_output=True
    )
    
    if result.returncode != 0:
        # Start server
        os.chdir(PREVIEW_DIR)
        subprocess.Popen(
            ["python3", "-m", "http.server", str(PREVIEW_PORT)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(1)
    
    # Check if tunnel is running
    result = subprocess.run(
        ["pgrep", "-f", f"cloudflared.*tunnel.*{PREVIEW_PORT}"],
        capture_output=True
    )
    
    if result.returncode != 0:
        # Start tunnel
        tunnel_log = open("/tmp/preview-tunnel.log", "w")
        subprocess.Popen(
            ["cloudflared", "tunnel", "--url", f"http://localhost:{PREVIEW_PORT}"],
            stdout=tunnel_log,
            stderr=tunnel_log
        )
        time.sleep(4)
    
    # Get tunnel URL
    if os.path.exists(TUNNEL_URL_FILE):
        with open(TUNNEL_URL_FILE) as f:
            base_url = f.read().strip()
            if base_url:
                return base_url
    
    # Extract from log
    time.sleep(2)
    if os.path.exists("/tmp/preview-tunnel.log"):
        with open("/tmp/preview-tunnel.log") as f:
            for line in f:
                if "trycloudflare.com" in line and "https://" in line:
                    import re
                    match = re.search(r'https://[a-z0-9-]+\.trycloudflare\.com', line)
                    if match:
                        base_url = match.group(0)
                        with open(TUNNEL_URL_FILE, "w") as uf:
                            uf.write(base_url)
                        return base_url
    
    raise Exception("Could not get tunnel URL")

def publish(html_path_or_content):
    """Publish HTML and return preview URL."""
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    
    # Determine if input is file or content
    if os.path.isfile(html_path_or_content):
        with open(html_path_or_content) as f:
            content = f.read()
        filename = Path(html_path_or_content).name
    else:
        content = html_path_or_content
        filename = "preview.html"
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
    preview_name = f"preview_{timestamp}_{content_hash}.html"
    preview_path = PREVIEW_DIR / preview_name
    
    # Write file
    with open(preview_path, "w") as f:
        f.write(content)
    
    # Ensure server is running
    base_url = ensure_preview_server()
    
    # Return full URL
    full_url = f"{base_url}/{preview_name}"
    return full_url

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: publish-preview.py <html-file-or-content>", file=sys.stderr)
        sys.exit(1)
    
    try:
        url = publish(sys.argv[1])
        print(url)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
