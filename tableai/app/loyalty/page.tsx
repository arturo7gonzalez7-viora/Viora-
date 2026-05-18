'use client'

import { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'
import { useRestaurantId } from '@/lib/useRestaurantId'
import { LoyaltyMember } from '@/lib/types'
import { cn } from '@/lib/utils'
import { LoadingSkeleton, EmptyState, ErrorState } from '@/components/LoadingState'

const tierConfig: Record<string, { bg: string; text: string; icon: string }> = {
  bronze: { bg: 'bg-orange-500/20', text: 'text-orange-400', icon: '🥉' },
  silver: { bg: 'bg-gray-400/20', text: 'text-gray-300', icon: '🥈' },
  gold: { bg: 'bg-amber-500/20', text: 'text-amber-400', icon: '🥇' },
  platinum: { bg: 'bg-purple-500/20', text: 'text-purple-300', icon: '💎' },
}

export default function LoyaltyPage() {
  const restaurantId = useRestaurantId()
  const [members, setMembers] = useState<LoyaltyMember[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  async function loadMembers() {
    setLoading(true)
    setError(null)
    const { data, error: err } = await supabase
      .from('loyalty_members')
      .select('*')
      .eq('restaurant_id', restaurantId)
      .order('points', { ascending: false })
      .limit(100)

    if (err) setError(err.message)
    else setMembers(data || [])
    setLoading(false)
  }

  useEffect(() => { loadMembers() }, [restaurantId])

  const totalPoints = members.reduce((sum, m) => sum + m.points, 0)

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-xl md:text-3xl font-black tracking-tight text-white">Loyalty Program</h1>
        <p className="text-white/40 text-sm">{members.length} members</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 md:gap-4">
        <div className="stat-card">
          <p className="text-white/40 text-sm">Total Members</p>
          <p className="text-3xl font-bold mt-1">{members.length}</p>
        </div>
        <div className="stat-card">
          <p className="text-white/40 text-sm">Total Points</p>
          <p className="text-3xl font-bold mt-1">{totalPoints.toLocaleString()}</p>
        </div>
        <div className="stat-card">
          <p className="text-white/40 text-sm">Gold+ Members</p>
          <p className="text-3xl font-bold mt-1">
            {members.filter(m => m.tier === 'gold' || m.tier === 'platinum').length}
          </p>
        </div>
      </div>

      {/* Member List */}
      {loading ? (
        <LoadingSkeleton />
      ) : error ? (
        <ErrorState message={error} onRetry={loadMembers} />
      ) : members.length === 0 ? (
        <EmptyState icon="💎" title="No loyalty members yet" description="Members will appear here as they sign up for your loyalty program." />
      ) : (
        <div className="card divide-y divide-white/5">
          {members.map((member) => {
            const tier = tierConfig[member.tier] || tierConfig.bronze
            return (
              <div key={member.id} className="table-row">
                <div className="flex items-center gap-4 flex-1 min-w-0">
                  <div className={cn('w-10 h-10 rounded-full flex items-center justify-center', tier.bg)}>
                    <span>{tier.icon}</span>
                  </div>
                  <div className="min-w-0">
                    <p className="font-medium text-white truncate">{member.name}</p>
                    <p className="text-sm text-white/40">{member.visits} visits · {member.phone}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="font-semibold text-teal">{member.points.toLocaleString()} pts</p>
                  <span className={cn('badge', tier.bg, tier.text, 'text-[10px]')}>
                    {member.tier}
                  </span>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
