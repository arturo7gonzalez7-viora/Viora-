import requests
import os
import time

# Paste your access token here
ACCESS_TOKEN = "PASTE_TOKEN_HERE"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Save images to Desktop
SAVE_FOLDER = os.path.expanduser("~/Desktop/Teams_Images")
os.makedirs(SAVE_FOLDER, exist_ok=True)

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.heic', '.heif'}

downloaded = 0
skipped = 0

def is_image(filename):
    ext = os.path.splitext(filename.lower())[1]
    return ext in IMAGE_EXTENSIONS

def download_file(url, filepath):
    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        if r.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(r.content)
            return True
    except Exception as e:
        print(f"  Error downloading: {e}")
    return False

def get_all_pages(url):
    results = []
    while url:
        r = requests.get(url, headers=HEADERS, timeout=30)
        if r.status_code != 200:
            print(f"  API error {r.status_code}: {r.text[:200]}")
            break
        data = r.json()
        results.extend(data.get('value', []))
        url = data.get('@odata.nextLink')
        time.sleep(0.2)
    return results

print("=== TEAMS IMAGE SCRAPER ===")
print(f"Saving to: {SAVE_FOLDER}")
print()

# Step 1: Get all chats
print("Fetching all chats...")
chats = get_all_pages("https://graph.microsoft.com/v1.0/me/chats?$expand=members&$top=50")
print(f"Found {len(chats)} chats")
print()

for chat in chats:
    chat_id = chat['id']
    chat_type = chat.get('chatType', 'unknown')
    
    # Get chat name
    topic = chat.get('topic') or ''
    if not topic:
        members = chat.get('members', [])
        names = [m.get('displayName', '') for m in members if m.get('displayName')]
        topic = ', '.join(names[:3]) or chat_id[:12]
    
    # Clean folder name
    safe_name = "".join(c for c in topic if c.isalnum() or c in ' _-').strip()[:50] or chat_id[:12]
    chat_folder = os.path.join(SAVE_FOLDER, safe_name)
    
    print(f"Scanning chat: {safe_name} ({chat_type})")
    
    # Step 2: Get messages with attachments
    messages_url = f"https://graph.microsoft.com/v1.0/me/chats/{chat_id}/messages?$top=50"
    messages = get_all_pages(messages_url)
    
    chat_images = 0
    
    for msg in messages:
        attachments = msg.get('attachments', [])
        
        for att in attachments:
            att_name = att.get('name', '')
            if not att_name or not is_image(att_name):
                continue
            
            content_url = att.get('contentUrl', '')
            if not content_url:
                continue
            
            os.makedirs(chat_folder, exist_ok=True)
            
            # Avoid duplicates
            filepath = os.path.join(chat_folder, att_name)
            base, ext = os.path.splitext(att_name)
            counter = 1
            while os.path.exists(filepath):
                filepath = os.path.join(chat_folder, f"{base}_{counter}{ext}")
                counter += 1
            
            if download_file(content_url, filepath):
                downloaded += 1
                chat_images += 1
                print(f"  ✅ {att_name}")
            else:
                skipped += 1
        
        time.sleep(0.1)
    
    if chat_images > 0:
        print(f"  → {chat_images} images saved")
    print()

print("=== DONE ===")
print(f"Total downloaded: {downloaded}")
print(f"Skipped/failed: {skipped}")
print(f"Saved to: {SAVE_FOLDER}")
