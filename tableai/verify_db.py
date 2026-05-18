from supabase import create_client

SUPABASE_URL = "https://ligrfnbpvryzgjgqnjyt.supabase.co"
SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxpZ3JmbmJwdnJ5emdqZ3Fuanl0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzA0ODE5OSwiZXhwIjoyMDkyNjI0MTk5fQ.j9aeKa9QkBYTSkBrTN5TziCuMhIJeY1BgaoRlmG03gM"

client = create_client(SUPABASE_URL, SERVICE_KEY)

# Insert Casa Mariachi as the first restaurant
result = client.table("restaurants").insert({
    "name": "Casa Mariachi",
    "phone": "(303) 841-4505",
    "address": "9078 Kimmer Dr",
    "city": "Parker",
    "state": "CO",
    "zip": "80134",
    "timezone": "America/Denver",
    "plan": "elite"
}).execute()

print("Casa Mariachi inserted!")
print(f"Restaurant ID: {result.data[0]['id']}")

# Verify all tables exist
tables = [
    "restaurants", "users", "calls", "reservations", "sms_log",
    "reviews", "inventory_items", "inventory_logs", "checklist_templates",
    "checklist_completions", "incidents", "wifi_guests", "loyalty_members",
    "loyalty_transactions", "loyalty_rewards", "daily_sales", "expenses",
    "staff", "timesheets", "content_posts", "promotions"
]

print(f"\nVerifying {len(tables)} tables...")
for table in tables:
    try:
        client.table(table).select("id").limit(1).execute()
        print(f"  ✅ {table}")
    except Exception as e:
        print(f"  ❌ {table}: {e}")

print("\nDatabase ready!")
