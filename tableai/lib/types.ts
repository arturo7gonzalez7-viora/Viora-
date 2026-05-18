export interface Restaurant {
  id: string
  name: string
  phone: string
  address: string
  city: string
  state: string
  zip: string
  timezone: string
  logo_url: string | null
  google_place_id: string | null
  created_at: string
}

export interface Reservation {
  id: string
  restaurant_id: string
  guest_name: string
  guest_phone: string
  party_size: number
  date: string
  time: string
  status: 'confirmed' | 'cancelled' | 'no-show' | 'seated' | 'completed'
  notes: string | null
  created_at: string
}

export interface Call {
  id: string
  restaurant_id: string
  caller_name: string | null
  caller_phone: string
  duration_seconds: number
  intent: string | null
  summary: string | null
  transcript: string | null
  status: string
  created_at: string
}

export interface Review {
  id: string
  restaurant_id: string
  reviewer_name: string
  platform: string
  rating: number
  review_text: string
  ai_response: string | null
  response_status: 'pending' | 'approved' | 'sent'
  created_at: string
}

export interface LoyaltyMember {
  id: string
  restaurant_id: string
  name: string
  phone: string
  email: string | null
  points: number
  tier: 'bronze' | 'silver' | 'gold' | 'platinum'
  visits: number
  created_at: string
}

export interface DailySale {
  id: string
  restaurant_id: string
  date: string
  total_revenue: number
  cash: number
  card: number
  online: number
  covers: number
  notes: string | null
  created_at: string
}

export interface Expense {
  id: string
  restaurant_id: string
  date: string
  category: string
  description: string
  amount: number
  vendor: string | null
  created_at: string
}

export interface InventoryItem {
  id: string
  restaurant_id: string
  name: string
  category: string
  unit: string
  current_quantity: number
  min_quantity: number
  cost_per_unit: number
  supplier: string | null
  created_at: string
}

export interface ReviewRequest {
  id: string
  restaurant_id: string
  guest_name: string | null
  guest_phone: string | null
  rating: number
  feedback_text: string | null
  sent_to_google: boolean
  is_private: boolean
  reservation_id: string | null
  created_at: string
}

export interface Staff {
  id: string
  restaurant_id: string
  name: string
  role: string
  phone: string
  email: string | null
  hourly_rate: number
  status: 'active' | 'inactive'
  created_at: string
}
