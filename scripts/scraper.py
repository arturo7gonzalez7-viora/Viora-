import requests
import os
import time

ACCESS_TOKEN = "EwA4BMl6BAAU9BatlgMxts2T1B5e3Mucgfs4jcAAAZqBkJEQx1eb1qD30jP3MeTCAK5vfI0dHAYIDdfmw6chYlbf5CbnzzzmCJm+wE3HHiatRXFnZxwuIqL7BCdH67gt7xe9YEFTTcu3MbQG21PcupWm8aGBrYMuRWf4JFkh14DLhXg8gKbm9jVtJLRKrBd/urnwQFc7xCbmVHSCsYg9nnczYbEs+HwmvQcBq53cYu/QZfNcDrZjI5yt/5w1GeqpoiQ8CM93lLXAaieA7JFkC1XXfCdPgH9KNIpGlm2bcwuotK9u5WRFVQ1E7UyuWI4z9kFCpypdI8raz9vlNekdUISdeBrrmMh5DtuGaYFmWU+aLDojQ0/HwkpXXPFws5gQZgAAEDk/4ac1yawTg0q5hk6XYjsAA12dvKLwNzyFqYwtrb5gT2O4tVZdRM6YL12iFLUTLcYkSu8qOVJKeDThPQ8709O7OJl71fOEdYOxKWtD1RzTWtdh0ySfLkATHL61VzF16A0ZVT42KUxF4AP9OigQ8WUvgPxSs3SUJURE9uMc9oDkcy+9ec7SpPXHrxEV64Zta1UWZ97o4xpv0gVFsTOlEK8sa9kk6z56JzI+5gU09Vn/q0njeFa5vCM5YcLvKHvgN/9UkjR2VhCCB4JAk9hbq9G0lqtXG5euUYC1jvOhIuYyyd7G2MgI6cnEaR1lfkD8UwiuWWC2XjymGnW+GQUGhGEUVGgqel+OhH2P/ECwuQPsyv0avKZgmRNZ+v3sEVR2CzPWftT4wiIQVQmEx4RUtVAnIA7atl75LsXFGxIKdSsh5fTirNkkjbFDB2r5dATluSCScPlqdV24b+YgzbPDwFuY4Zh7qIXnOrkfqQAlBjMOAYozE0I+n5T8Lg4CzMIKuC2eaWzFhVHZl3VQoiom9FqWgZn8E0BA2sQzFez5xX+rm3tAWKJXDJUbq1samZndfD7C/dlV0ldvTrnpfM5AbzPuLh0izMbBBCPQJI8nVKQ8tvwEuoQYR1/oFxI4Tn3LWECru9hLoNqHDLpeWl4hdFOthLc+zr9dwlXFtw3vewKnCDkbNNGfWc2W8zLfnIslDmm0oYX92vmrTuGBv+gGzLahj/dwC/QpUCWEAdQwLWwFT4XAm8gp4gkwrJvUKAwaBYTXGPhsjzkO81GHrAdMWPI9RvhFMTxbaE923eGbXl8yR4NMSCg4Ti3qYC4+E685Nct6A20vQmSmBZad15JR4KcN1pYV8XhMUpgTuzwWURWuj0/IGHYpQ28hKHkA8YylBQO/dT/RriyewNohwpiqOblIEjo1ycw/cLm99uTRxOYPnEtbv/15aXxZVmHe3iOOUD4xDKoVhqzv739pFW3z959b1Z1t37luwsLMV9iBXctgE4w84FJAIcxryZlp6b10maNaVr42v0SJtQAqdbJAHCEthDgD"

HEADERS = {"Authorization": "Bearer " + ACCESS_TOKEN}
SAVE = os.path.expanduser("~/Desktop/Teams_Images")
os.makedirs(SAVE, exist_ok=True)
IMGS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".heic"}
downloaded = 0


def is_img(f):
    return os.path.splitext(f.lower())[1] in IMGS


def pages(url):
    out = []
    while url:
        r = requests.get(url, headers=HEADERS, timeout=30)
        if r.status_code != 200:
            print("API error:", r.status_code, r.text[:100])
            break
        d = r.json()
        out.extend(d.get("value", []))
        url = d.get("@odata.nextLink")
        time.sleep(0.2)
    return out


print("Fetching chats...")
chats = pages("https://graph.microsoft.com/v1.0/me/chats?$top=50")
print("Found", len(chats), "chats")

for chat in chats:
    cid = chat["id"]
    topic = chat.get("topic") or cid[:12]
    safe = "".join(c for c in topic if c.isalnum() or c in " _-").strip()[:40]
    if not safe:
        safe = cid[:12]
    folder = os.path.join(SAVE, safe)
    print("Scanning:", safe)
    msgs = pages("https://graph.microsoft.com/v1.0/me/chats/" + cid + "/messages?$top=50")
    for msg in msgs:
        for att in msg.get("attachments", []):
            name = att.get("name", "")
            url = att.get("contentUrl", "")
            if not name or not url or not is_img(name):
                continue
            os.makedirs(folder, exist_ok=True)
            path = os.path.join(folder, name)
            try:
                rv = requests.get(url, headers=HEADERS, timeout=30)
                if rv.status_code == 200:
                    open(path, "wb").write(rv.content)
                    downloaded = downloaded + 1
                    print("  saved:", name)
            except Exception as e:
                print("  error:", e)
        time.sleep(0.1)

print("DONE!", downloaded, "images saved to ~/Desktop/Teams_Images")
