import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

const DEFAULT_RESTAURANT_ID = process.env.NEXT_PUBLIC_RESTAURANT_ID || '41dabcfe-41e7-4b4c-ba49-a38c06fe544c'

export function getRestaurantId(): string {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('tableai_active_restaurant') || DEFAULT_RESTAURANT_ID
  }
  return DEFAULT_RESTAURANT_ID
}


