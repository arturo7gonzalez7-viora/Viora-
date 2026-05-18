'use client'
import { useState, useEffect } from 'react'
import { getRestaurantId } from './supabase'

export function useRestaurantId() {
  const [restaurantId, setRestaurantId] = useState<string>(getRestaurantId())
  
  useEffect(() => {
    setRestaurantId(getRestaurantId())
  }, [])
  
  return restaurantId
}
