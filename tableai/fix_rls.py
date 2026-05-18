import httpx

SUPABASE_URL = "https://ligrfnbpvryzgjgqnjyt.supabase.co"
SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxpZ3JmbmJwdnJ5emdqZ3Fuanl0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzA0ODE5OSwiZXhwIjoyMDkyNjI0MTk5fQ.j9aeKa9QkBYTSkBrTN5TziCuMhIJeY1BgaoRlmG03gM"

# Test read with anon key
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxpZ3JmbmJwdnJ5emdqZ3Fuanl0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzcwNDgxOTksImV4cCI6MjA5MjYyNDE5OX0.USNLCrPr9agHIxQbRRb6ampRKvJlBSuQz-ZSFiQXYIw"

# Test with anon key (what the browser uses)
resp = httpx.get(
    f"{SUPABASE_URL}/rest/v1/restaurants?select=id,name",
    headers={
        "apikey": ANON_KEY,
        "Authorization": f"Bearer {ANON_KEY}",
    }
)
print(f"Anon read status: {resp.status_code}")
print(f"Anon read result: {resp.text[:300]}")
