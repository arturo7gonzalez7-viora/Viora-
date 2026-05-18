import httpx, json

SUPABASE_URL = "https://ligrfnbpvryzgjgqnjyt.supabase.co"
SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxpZ3JmbmJwdnJ5emdqZ3Fuanl0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzA0ODE5OSwiZXhwIjoyMDkyNjI0MTk5fQ.j9aeKa9QkBYTSkBrTN5TziCuMhIJeY1BgaoRlmG03gM"
PROJECT_REF = "ligrfnbpvryzgjgqnjyt"

with open('/root/.openclaw/workspace/tableai/schema.sql', 'r') as f:
    sql = f.read()

headers = {
    "apikey": SERVICE_KEY,
    "Authorization": f"Bearer {SERVICE_KEY}",
    "Content-Type": "application/json"
}

resp = httpx.post(
    f"https://api.supabase.com/v1/projects/{PROJECT_REF}/database/query",
    headers=headers,
    json={"query": sql},
    timeout=60
)
print(f"Status: {resp.status_code}")
print(resp.text[:1000])
