'use client'

import { useState, useEffect, useCallback } from 'react'
import { supabase, getRestaurantId } from './supabase'

export interface Restaurant {
  id: string
  name: string
  phone: string | null
  city: string | null
}

export function useRestaurant() {
  const [restaurants, setRestaurants] = useState<Restaurant[]>([])
  const [activeId, setActiveId] = useState<string>(getRestaurantId())
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchRestaurants() {
      const { data, error } = await supabase
        .from('restaurants')
        .select('id, name, phone, city')
        .order('name')

      if (!error && data) {
        setRestaurants(data)
      }
      setLoading(false)
    }
    fetchRestaurants()
  }, [])

  const activeRestaurant = restaurants.find((r) => r.id === activeId) || null

  const switchRestaurant = useCallback((id: string) => {
    localStorage.setItem('tableai_active_restaurant', id)
    setActiveId(id)
    window.location.reload()
  }, [])

  const addRestaurant = useCallback(async (name: string, phone: string, city: string) => {
    const { data, error } = await supabase
      .from('restaurants')
      .insert({ name, phone: phone || null, city: city || null })
      .select('id')
      .single()

    if (error) throw error
    if (data) {
      switchRestaurant(data.id)
    }
  }, [switchRestaurant])

  return {
    restaurants,
    activeRestaurant,
    activeId,
    switchRestaurant,
    addRestaurant,
    loading,
  }
}
