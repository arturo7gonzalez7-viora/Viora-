from supabase import create_client
from datetime import date, time, datetime, timedelta
import random

url = 'https://ligrfnbpvryzgjgqnjyt.supabase.co'
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxpZ3JmbmJwdnJ5emdqZ3Fuanl0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzA0ODE5OSwiZXhwIjoyMDkyNjI0MTk5fQ.j9aeKa9QkBYTSkBrTN5TziCuMhIJeY1BgaoRlmG03gM'
sb = create_client(url, key)

RID = '961ca902-54d9-44dd-bdab-df732a46b98f'
today = date.today()

print("Seeding Test Rest with mock data...")

# Update restaurant info
sb.table('restaurants').update({
    'phone': '(720) 555-0192',
    'address': '1847 Blake Street',
    'city': 'Denver',
    'state': 'CO',
    'zip': '80202',
    'hours': {'mon': '11am-10pm', 'tue': '11am-10pm', 'wed': '11am-10pm', 'thu': '11am-11pm', 'fri': '11am-12am', 'sat': '10am-12am', 'sun': '10am-9pm'},
    'plan': 'elite'
}).eq('id', RID).execute()
print("Restaurant info updated")

# RESERVATIONS
reservations = [
    {'guest_name': 'Marcus & Jennifer Williams', 'guest_phone': '(303) 555-0142', 'party_size': 4, 'date': str(today), 'time': '18:00', 'status': 'confirmed', 'notes': 'Anniversary dinner, request corner booth'},
    {'guest_name': 'Sarah Chen', 'guest_phone': '(720) 555-0287', 'party_size': 2, 'date': str(today), 'time': '18:30', 'status': 'confirmed', 'notes': None},
    {'guest_name': 'Rodriguez Family', 'guest_phone': '(303) 555-0391', 'party_size': 8, 'date': str(today), 'time': '19:00', 'status': 'confirmed', 'notes': 'Birthday celebration, need high chair'},
    {'guest_name': 'David Park', 'guest_phone': '(720) 555-0156', 'party_size': 2, 'date': str(today), 'time': '19:30', 'status': 'confirmed', 'notes': None},
    {'guest_name': 'Thompson Group', 'guest_phone': '(303) 555-0428', 'party_size': 6, 'date': str(today), 'time': '20:00', 'status': 'confirmed', 'notes': 'Corporate dinner'},
    {'guest_name': 'Emily Vasquez', 'guest_phone': '(720) 555-0319', 'party_size': 3, 'date': str(today), 'time': '20:30', 'status': 'confirmed', 'notes': None},
    {'guest_name': 'James & Lisa Kim', 'guest_phone': '(303) 555-0537', 'party_size': 2, 'date': str(today + timedelta(days=1)), 'time': '19:00', 'status': 'confirmed'},
    {'guest_name': 'Perez Birthday Party', 'guest_phone': '(720) 555-0644', 'party_size': 12, 'date': str(today + timedelta(days=1)), 'time': '18:00', 'status': 'confirmed', 'notes': 'Need to arrange birthday cake'},
    {'guest_name': 'Michael Torres', 'guest_phone': '(303) 555-0751', 'party_size': 4, 'date': str(today - timedelta(days=1)), 'time': '19:30', 'status': 'completed'},
    {'guest_name': 'Ashley Johnson', 'guest_phone': '(720) 555-0862', 'party_size': 2, 'date': str(today - timedelta(days=1)), 'time': '20:00', 'status': 'no_show'},
]
for r in reservations:
    r['restaurant_id'] = RID
    r['reminder_sent'] = True
    r['source'] = 'phone'
sb.table('reservations').insert(reservations).execute()
print(f"Added {len(reservations)} reservations")

# CALLS
calls = [
    {'caller_phone': '(303) 555-0142', 'caller_name': 'Marcus Williams', 'duration_seconds': 87, 'intent': 'reservation', 'summary': 'Called to make anniversary dinner reservation for 4. Requested corner booth. Confirmed for tonight at 6pm.'},
    {'caller_phone': '(720) 555-0391', 'caller_name': 'Maria Rodriguez', 'duration_seconds': 124, 'intent': 'reservation', 'summary': 'Birthday party reservation for 8 guests. Mentioned they want a birthday cake surprise. Booked for tonight at 7pm.'},
    {'caller_phone': '(303) 555-0428', 'caller_name': 'Brian Thompson', 'duration_seconds': 63, 'intent': 'reservation', 'summary': 'Corporate dinner for 6. Asked about private dining options. Confirmed for 8pm tonight.'},
    {'caller_phone': '(720) 555-0917', 'caller_name': 'Unknown', 'duration_seconds': 45, 'intent': 'question', 'summary': 'Asked about happy hour times and what drinks are included. Informed about $5 drinks from 3-6pm daily.'},
    {'caller_phone': '(303) 555-0223', 'caller_name': 'Unknown', 'duration_seconds': 38, 'intent': 'question', 'summary': 'Asked if we are open on Easter Sunday and what our hours are. Confirmed 10am-9pm.'},
    {'caller_phone': '(720) 555-0534', 'caller_name': 'Unknown', 'duration_seconds': 29, 'intent': 'question', 'summary': 'Asked about gluten-free menu options. Informed that we have several GF options and to mention dietary needs when seated.'},
    {'caller_phone': '(303) 555-0645', 'caller_name': 'Unknown', 'duration_seconds': 95, 'intent': 'complaint', 'summary': 'Customer complained that their takeout order last Tuesday was missing an entree. Offered a complimentary replacement on next visit.'},
    {'caller_phone': '(720) 555-0756', 'caller_name': 'Jennifer Park', 'duration_seconds': 52, 'intent': 'reservation', 'summary': 'Tried to book for tonight but requested time was full. Offered alternative at 8:30pm, customer said they would call back.'},
]
for c in calls:
    c['restaurant_id'] = RID
sb.table('calls').insert(calls).execute()
print(f"Added {len(calls)} calls")

# REVIEWS
reviews = [
    {'platform': 'google', 'reviewer_name': 'Jessica M.', 'rating': 5, 'review_text': 'Absolutely incredible experience! The food was authentic and delicious, service was attentive without being intrusive, and the atmosphere was perfect for our anniversary. The mole sauce was the best I have ever tasted. We will definitely be back!', 'ai_response': 'Thank you so much Jessica! We are thrilled you chose us for your anniversary and that the mole sauce left such an impression. It is made fresh daily from a family recipe. We cannot wait to welcome you back!', 'response_posted': True, 'response_approved': True, 'review_date': str(today - timedelta(days=1))},
    {'platform': 'google', 'reviewer_name': 'Robert K.', 'rating': 5, 'review_text': 'Best Mexican food in Denver, no contest. The street tacos are incredible and the margaritas are strong and well-made. Great live music on Friday nights. Staff is friendly and knowledgeable. Highly recommend!', 'ai_response': 'Robert, this made our whole team smile! We take pride in our street tacos and hand-crafted margaritas. Hope to see you at Friday night live music again soon!', 'response_posted': True, 'response_approved': True, 'review_date': str(today - timedelta(days=2))},
    {'platform': 'google', 'reviewer_name': 'Amanda L.', 'rating': 4, 'review_text': 'Really good food and great vibe. Only knocking one star because the wait was a bit long on Saturday night, but totally understandable given how packed it was. The enchiladas were amazing and the chips and salsa were fresh and addictive.', 'ai_response': 'Thank you Amanda! We are glad you enjoyed the enchiladas and our house-made chips. Saturday nights are our busiest and we are working on improving wait times. Your feedback helps us get better!', 'response_posted': False, 'response_approved': False, 'review_date': str(today - timedelta(days=3))},
    {'platform': 'yelp', 'reviewer_name': 'Carlos T.', 'rating': 5, 'review_text': 'Came here for my birthday with family and they made it so special. The manager came to our table, they brought out a flan with a candle, and the whole staff sang. Food was phenomenal. The carne asada is a must-order.', 'ai_response': 'Happy birthday Carlos! Making special moments memorable is what we live for. The carne asada is indeed a fan favorite. Wishing you many more celebrations with us!', 'response_posted': True, 'response_approved': True, 'review_date': str(today - timedelta(days=4))},
    {'platform': 'google', 'reviewer_name': 'Patricia W.', 'rating': 2, 'review_text': 'Food was okay but service was slow and our server seemed overwhelmed. Took 20 minutes to get water and 45 minutes for our entrees. The food was good when it came but not worth the wait on a Tuesday night when it was not even that busy.', 'ai_response': 'Patricia, we sincerely apologize for the slow service during your visit. This is not the standard we hold ourselves to. We would love to make it right. Please reach out to us directly at manager@testrest.com and we will ensure your next visit is exceptional.', 'response_posted': False, 'response_approved': False, 'review_date': str(today - timedelta(days=5))},
    {'platform': 'google', 'reviewer_name': 'Daniel H.', 'rating': 5, 'review_text': 'The guacamole is made tableside and it is absolutely worth it. Perfect texture, perfectly seasoned. The birria tacos with consomme for dipping are a must. This place has become our Friday night go-to.', 'ai_response': 'Daniel, you have excellent taste! Our tableside guac and birria tacos are two of our proudest dishes. See you Friday!', 'response_posted': True, 'response_approved': True, 'review_date': str(today - timedelta(days=6))},
]
for r in reviews:
    r['restaurant_id'] = RID
sb.table('reviews').insert(reviews).execute()
print(f"Added {len(reviews)} reviews")

# LOYALTY MEMBERS
members = [
    {'name': 'Maria Gonzalez', 'phone': '(303) 555-1001', 'email': 'mgonzalez@email.com', 'points': 2840, 'total_spent': 1247.50, 'visit_count': 34, 'tier': 'gold'},
    {'name': 'James Park', 'phone': '(720) 555-1002', 'email': 'jpark@email.com', 'points': 5120, 'total_spent': 3890.00, 'visit_count': 67, 'tier': 'vip'},
    {'name': 'Sofia Ramirez', 'phone': '(303) 555-1003', 'email': 'sramirez@email.com', 'points': 1450, 'total_spent': 634.25, 'visit_count': 18, 'tier': 'silver'},
    {'name': 'Michael Chen', 'phone': '(720) 555-1004', 'email': 'mchen@email.com', 'points': 890, 'total_spent': 312.00, 'visit_count': 9, 'tier': 'bronze'},
    {'name': 'Ashley Thompson', 'phone': '(303) 555-1005', 'email': 'athompson@email.com', 'points': 3200, 'total_spent': 1876.50, 'visit_count': 41, 'tier': 'gold'},
    {'name': 'Carlos Rivera', 'phone': '(720) 555-1006', 'email': 'crivera@email.com', 'points': 7650, 'total_spent': 5430.00, 'visit_count': 89, 'tier': 'vip'},
    {'name': 'Emily Watson', 'phone': '(303) 555-1007', 'email': 'ewatson@email.com', 'points': 420, 'total_spent': 198.75, 'visit_count': 5, 'tier': 'bronze'},
    {'name': 'David Martinez', 'phone': '(720) 555-1008', 'email': 'dmartinez@email.com', 'points': 1980, 'total_spent': 892.00, 'visit_count': 22, 'tier': 'silver'},
    {'name': 'Jennifer Lee', 'phone': '(303) 555-1009', 'email': 'jlee@email.com', 'points': 2100, 'total_spent': 1100.50, 'visit_count': 27, 'tier': 'gold'},
    {'name': 'Robert Hernandez', 'phone': '(720) 555-1010', 'email': 'rhernandez@email.com', 'points': 650, 'total_spent': 276.00, 'visit_count': 7, 'tier': 'bronze'},
]
for m in members:
    m['restaurant_id'] = RID
sb.table('loyalty_members').insert(members).execute()
print(f"Added {len(members)} loyalty members")

# INVENTORY
inventory = [
    {'name': 'Avocados', 'category': 'produce', 'unit': 'each', 'current_qty': 48, 'par_level': 60, 'cost_per_unit': 0.85, 'supplier': 'Fresh Farms Co'},
    {'name': 'Chicken Breast', 'category': 'protein', 'unit': 'lbs', 'current_qty': 32, 'par_level': 40, 'cost_per_unit': 4.20, 'supplier': 'Premier Meats'},
    {'name': 'Carne Asada (Skirt Steak)', 'category': 'protein', 'unit': 'lbs', 'current_qty': 18, 'par_level': 25, 'cost_per_unit': 8.50, 'supplier': 'Premier Meats'},
    {'name': 'Corn Tortillas', 'category': 'dry', 'unit': 'case', 'current_qty': 8, 'par_level': 10, 'cost_per_unit': 22.00, 'supplier': 'La Paloma Distributing'},
    {'name': 'Flour Tortillas', 'category': 'dry', 'unit': 'case', 'current_qty': 5, 'par_level': 8, 'cost_per_unit': 28.00, 'supplier': 'La Paloma Distributing'},
    {'name': 'Limes', 'category': 'produce', 'unit': 'lbs', 'current_qty': 22, 'par_level': 15, 'cost_per_unit': 1.20, 'supplier': 'Fresh Farms Co'},
    {'name': 'Tequila Blanco (House)', 'category': 'alcohol', 'unit': 'bottle', 'current_qty': 24, 'par_level': 18, 'cost_per_unit': 18.50, 'supplier': 'Rocky Mountain Spirits'},
    {'name': 'Tequila Reposado (Premium)', 'category': 'alcohol', 'unit': 'bottle', 'current_qty': 12, 'par_level': 10, 'cost_per_unit': 34.00, 'supplier': 'Rocky Mountain Spirits'},
    {'name': 'Draft Beer Kegs', 'category': 'alcohol', 'unit': 'each', 'current_qty': 3, 'par_level': 4, 'cost_per_unit': 145.00, 'supplier': 'Denver Brew Supply'},
    {'name': 'Queso Fresco', 'category': 'dairy', 'unit': 'lbs', 'current_qty': 8, 'par_level': 12, 'cost_per_unit': 5.40, 'supplier': 'Dairy Fresh'},
    {'name': 'Sour Cream', 'category': 'dairy', 'unit': 'lbs', 'current_qty': 14, 'par_level': 10, 'cost_per_unit': 2.80, 'supplier': 'Dairy Fresh'},
    {'name': 'Cilantro', 'category': 'produce', 'unit': 'lbs', 'current_qty': 3, 'par_level': 5, 'cost_per_unit': 2.50, 'supplier': 'Fresh Farms Co'},
    {'name': 'Dried Chiles (Ancho)', 'category': 'dry', 'unit': 'lbs', 'current_qty': 6, 'par_level': 4, 'cost_per_unit': 7.20, 'supplier': 'La Paloma Distributing'},
    {'name': 'Triple Sec', 'category': 'alcohol', 'unit': 'bottle', 'current_qty': 9, 'par_level': 8, 'cost_per_unit': 12.00, 'supplier': 'Rocky Mountain Spirits'},
    {'name': 'To-Go Containers (Large)', 'category': 'dry', 'unit': 'case', 'current_qty': 2, 'par_level': 5, 'cost_per_unit': 48.00, 'supplier': 'Restaurant Supply Co'},
]
for i in inventory:
    i['restaurant_id'] = RID
    i['active'] = True
sb.table('inventory_items').insert(inventory).execute()
print(f"Added {len(inventory)} inventory items")

# DAILY SALES (last 7 days)
for i in range(7):
    d = today - timedelta(days=i)
    is_weekend = d.weekday() >= 4
    revenue = round(random.uniform(4200, 6800) if is_weekend else random.uniform(2800, 4500), 2)
    covers = random.randint(95, 180) if is_weekend else random.randint(60, 110)
    sb.table('daily_sales').insert({
        'restaurant_id': RID,
        'date': str(d),
        'total_revenue': revenue,
        'cash_sales': round(revenue * 0.18, 2),
        'card_sales': round(revenue * 0.67, 2),
        'delivery_sales': round(revenue * 0.15, 2),
        'covers': covers,
        'avg_ticket': round(revenue / covers, 2),
    }).execute()
print("Added 7 days of sales data")

# EXPENSES
expenses = [
    {'date': str(today), 'category': 'food_cost', 'amount': 1240.00, 'description': 'Weekly produce and protein order', 'vendor': 'Fresh Farms Co'},
    {'date': str(today), 'category': 'labor', 'amount': 2180.00, 'description': 'Weekly payroll', 'vendor': 'Internal'},
    {'date': str(today - timedelta(days=1)), 'category': 'alcohol', 'amount': 680.00, 'description': 'Liquor restock', 'vendor': 'Rocky Mountain Spirits'},
    {'date': str(today - timedelta(days=2)), 'category': 'supplies', 'amount': 145.00, 'description': 'Cleaning supplies and paper goods', 'vendor': 'Restaurant Supply Co'},
    {'date': str(today - timedelta(days=3)), 'category': 'utilities', 'amount': 420.00, 'description': 'Gas and electric', 'vendor': 'Xcel Energy'},
    {'date': str(today - timedelta(days=4)), 'category': 'marketing', 'amount': 250.00, 'description': 'Instagram ads for Cinco de Mayo promo', 'vendor': 'Meta Ads'},
    {'date': str(today - timedelta(days=5)), 'category': 'food_cost', 'amount': 890.00, 'description': 'Dairy and dry goods restock', 'vendor': 'Dairy Fresh'},
    {'date': str(today - timedelta(days=6)), 'category': 'other', 'amount': 180.00, 'description': 'Equipment repair (ice machine)', 'vendor': 'Denver Appliance Repair'},
]
for e in expenses:
    e['restaurant_id'] = RID
sb.table('expenses').insert(expenses).execute()
print(f"Added {len(expenses)} expenses")

# STAFF
staff = [
    {'name': 'Rosa Mendez', 'role': 'manager', 'hourly_rate': 22.00, 'phone': '(303) 555-2001', 'email': 'rosa@testrest.com'},
    {'name': 'Miguel Torres', 'role': 'cook', 'hourly_rate': 18.50, 'phone': '(720) 555-2002', 'email': None},
    {'name': 'Alejandro Ruiz', 'role': 'cook', 'hourly_rate': 17.00, 'phone': '(303) 555-2003', 'email': None},
    {'name': 'Brittany Cole', 'role': 'server', 'hourly_rate': 12.00, 'phone': '(720) 555-2004', 'email': None},
    {'name': 'Tyler Brooks', 'role': 'server', 'hourly_rate': 12.00, 'phone': '(303) 555-2005', 'email': None},
    {'name': 'Ana Flores', 'role': 'server', 'hourly_rate': 12.00, 'phone': '(720) 555-2006', 'email': None},
    {'name': 'Kevin Nash', 'role': 'bartender', 'hourly_rate': 15.00, 'phone': '(303) 555-2007', 'email': None},
    {'name': 'Isabella Cruz', 'role': 'host', 'hourly_rate': 14.00, 'phone': '(720) 555-2008', 'email': None},
]
staff_ids = []
for s in staff:
    s['restaurant_id'] = RID
    s['active'] = True
    res = sb.table('staff').insert(s).execute()
    staff_ids.append(res.data[0]['id'])
print(f"Added {len(staff)} staff members")

# PROMOTIONS
promos = [
    {'name': 'Taco Tuesday', 'description': 'Pick two tacos plus one side plus one premium cocktail. Our most popular weekly deal.', 'day_of_week': 'tuesday', 'active': True},
    {'name': 'Happy Hour', 'description': '$5 house margaritas, $5 draft beers, $5 wines, and $5 tequila shots. Every day 3pm to 6pm.', 'active': True},
    {'name': 'Cinco de Mayo Weekend', 'description': 'Extended happy hour all weekend, live mariachi band, and a special limited menu featuring regional dishes from Jalisco.', 'start_date': str(today + timedelta(days=5)), 'end_date': str(today + timedelta(days=7)), 'active': True},
    {'name': 'Sunday Brunch', 'description': 'Bottomless mimosas with any brunch entree. Live acoustic music. 10am to 2pm.', 'day_of_week': 'sunday', 'active': True},
]
for p in promos:
    p['restaurant_id'] = RID
sb.table('promotions').insert(promos).execute()
print(f"Added {len(promos)} promotions")

# CONTENT POSTS
posts = [
    {'platform': 'instagram', 'caption': 'Taco Tuesday is BACK and better than ever! Two tacos, one side, one craft cocktail. Tag someone you are bringing tonight.', 'hashtags': '#TacoTuesday #DenverFood #MexicanFood #TacoLovers #Denver', 'scheduled_for': None, 'posted': True},
    {'platform': 'instagram', 'caption': 'Our birria tacos with consomme have been absolutely blowing up this week. The wait is worth it. Come early, stay late.', 'hashtags': '#BirriaQuesatacos #Denver #DenverEats #FoodTok #MexicanFood', 'scheduled_for': None, 'posted': True},
    {'platform': 'facebook', 'caption': 'Big announcement! We are hosting a special Cinco de Mayo weekend celebration with live mariachi, extended happy hour, and a limited menu featuring authentic dishes from Jalisco. Reserve your table now before we sell out!', 'hashtags': None, 'scheduled_for': str(today + timedelta(days=3)) + 'T10:00:00', 'posted': False},
    {'platform': 'tiktok', 'caption': 'Making our famous guacamole tableside because you deserve to see every ingredient go in. Fresh avocados, lime, cilantro, jalapeño, and our secret touch.', 'hashtags': '#Guacamole #MexicanFood #FoodTok #Denver #Cooking', 'scheduled_for': None, 'posted': True},
    {'platform': 'instagram', 'caption': 'Sunday Funday starts with our bottomless mimosa brunch. Live music, fresh food, good vibes. Doors open at 10am.', 'hashtags': '#SundayBrunch #Mimosas #DenverBrunch #Denver #BrunchVibes', 'scheduled_for': str(today + timedelta(days=2)) + 'T08:00:00', 'posted': False},
]
for p in posts:
    p['restaurant_id'] = RID
sb.table('content_posts').insert(posts).execute()
print(f"Added {len(posts)} content posts")

# COMPLIANCE CHECKLISTS
templates = [
    {'name': 'Opening Checklist', 'frequency': 'daily', 'items': [
        {'task': 'Check all refrigerator temperatures (must be below 40F)', 'required': True},
        {'task': 'Verify food storage labels and dates', 'required': True},
        {'task': 'Sanitize all prep surfaces and cutting boards', 'required': True},
        {'task': 'Stock server stations with napkins and utensils', 'required': True},
        {'task': 'Check that all fire exits are clear and unlocked', 'required': True},
        {'task': 'Test POS system and printers', 'required': True},
        {'task': 'Fill salt, pepper, and condiment stations', 'required': False},
        {'task': 'Check reservation book for special requests', 'required': True},
    ]},
    {'name': 'Closing Checklist', 'frequency': 'daily', 'items': [
        {'task': 'Properly store and label all remaining food', 'required': True},
        {'task': 'Clean and sanitize all cooking surfaces and equipment', 'required': True},
        {'task': 'Mop all kitchen and dining area floors', 'required': True},
        {'task': 'Empty and clean all trash bins', 'required': True},
        {'task': 'Lock all doors and set alarm', 'required': True},
        {'task': 'Count and balance the register', 'required': True},
        {'task': 'Run dishwasher final cycle', 'required': True},
    ]},
    {'name': 'Weekly Deep Clean', 'frequency': 'weekly', 'items': [
        {'task': 'Clean behind all kitchen equipment', 'required': True},
        {'task': 'Degrease exhaust hood and filters', 'required': True},
        {'task': 'Clean and descale ice machine', 'required': True},
        {'task': 'Wipe down all walls and baseboards', 'required': False},
        {'task': 'Deep clean walk-in cooler', 'required': True},
        {'task': 'Inspect and test all fire suppression equipment', 'required': True},
    ]},
]
for t in templates:
    t['restaurant_id'] = RID
    t['active'] = True
sb.table('checklist_templates').insert(templates).execute()
print(f"Added {len(templates)} compliance templates")

# WIFI GUESTS
wifi = [
    {'name': 'Taylor S.', 'email': 'taylors@gmail.com', 'phone': '(303) 555-3001', 'visit_count': 8, 'opted_in_sms': True, 'opted_in_email': True},
    {'name': 'Jordan M.', 'email': 'jordanm@gmail.com', 'phone': '(720) 555-3002', 'visit_count': 3, 'opted_in_sms': True, 'opted_in_email': False},
    {'name': 'Alex P.', 'email': 'alexp@yahoo.com', 'phone': None, 'visit_count': 1, 'opted_in_sms': False, 'opted_in_email': True},
    {'name': 'Casey R.', 'email': 'caseyr@gmail.com', 'phone': '(303) 555-3004', 'visit_count': 12, 'opted_in_sms': True, 'opted_in_email': True},
    {'name': 'Morgan K.', 'email': 'morgank@outlook.com', 'phone': '(720) 555-3005', 'visit_count': 5, 'opted_in_sms': False, 'opted_in_email': True},
]
for w in wifi:
    w['restaurant_id'] = RID
sb.table('wifi_guests').insert(wifi).execute()
print(f"Added {len(wifi)} WiFi guests")

print("\nAll mock data seeded successfully! Test Rest is now a thriving business.")
