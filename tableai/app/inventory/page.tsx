'use client'

import { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'
import { useRestaurantId } from '@/lib/useRestaurantId'
import { InventoryItem } from '@/lib/types'
import { formatCurrency, cn } from '@/lib/utils'
import { LoadingSkeleton, EmptyState, ErrorState } from '@/components/LoadingState'

export default function InventoryPage() {
  const restaurantId = useRestaurantId()
  const [items, setItems] = useState<InventoryItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  async function loadItems() {
    setLoading(true)
    setError(null)
    const { data, error: err } = await supabase
      .from('inventory_items')
      .select('*')
      .eq('restaurant_id', restaurantId)
      .order('name')

    if (err) setError(err.message)
    else setItems(data || [])
    setLoading(false)
  }

  useEffect(() => { loadItems() }, [restaurantId])

  const lowStock = items.filter(i => i.current_quantity <= i.min_quantity)

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-xl md:text-3xl font-black tracking-tight text-white">Inventory</h1>
        <p className="text-white/40 text-sm">{items.length} items</p>
      </div>

      {lowStock.length > 0 && (
        <div className="bg-red-500/10 border border-red-500/20 rounded-2xl p-3 md:p-4">
          <p className="font-semibold text-red-400 mb-1">⚠️ Low Stock Alert</p>
          <p className="text-sm text-white/60">
            {lowStock.map(i => i.name).join(', ')} — need to reorder soon.
          </p>
        </div>
      )}

      {loading ? (
        <LoadingSkeleton />
      ) : error ? (
        <ErrorState message={error} onRetry={loadItems} />
      ) : items.length === 0 ? (
        <EmptyState icon="📦" title="No inventory items" description="Add items to start tracking your inventory." />
      ) : (
        <div className="card divide-y divide-white/5">
          {items.map((item) => {
            const isLow = item.current_quantity <= item.min_quantity
            return (
              <div key={item.id} className="table-row">
                <div className="flex items-center gap-4 flex-1 min-w-0">
                  <div className={cn(
                    'w-10 h-10 rounded-xl flex items-center justify-center',
                    isLow ? 'bg-red-500/20' : 'bg-white/5'
                  )}>
                    <span>{isLow ? '⚠️' : '📦'}</span>
                  </div>
                  <div className="min-w-0">
                    <p className="font-medium text-white truncate">{item.name}</p>
                    <p className="text-sm text-white/40">
                      {item.category} · {formatCurrency(item.cost_per_unit)}/{item.unit}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className={cn('font-semibold', isLow ? 'text-red-400' : 'text-white')}>
                    {item.current_quantity} {item.unit}
                  </p>
                  <p className="text-xs text-white/30">min: {item.min_quantity}</p>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
