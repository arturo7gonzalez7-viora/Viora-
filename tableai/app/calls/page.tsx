'use client'

import { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'
import { useRestaurantId } from '@/lib/useRestaurantId'
import { Call } from '@/lib/types'
import { formatDuration, cn } from '@/lib/utils'
import { LoadingSkeleton, EmptyState, ErrorState } from '@/components/LoadingState'

const intentColors: Record<string, string> = {
  reservation: 'bg-blue-500/20 text-blue-400',
  inquiry: 'bg-amber-500/20 text-amber-400',
  complaint: 'bg-red-500/20 text-red-400',
  order: 'bg-emerald-500/20 text-emerald-400',
  catering: 'bg-purple-500/20 text-purple-400',
  other: 'bg-white/10 text-white/50',
}

export default function CallsPage() {
  const restaurantId = useRestaurantId()
  const [calls, setCalls] = useState<Call[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [expandedId, setExpandedId] = useState<string | null>(null)

  async function loadCalls() {
    setLoading(true)
    setError(null)
    const { data, error: err } = await supabase
      .from('calls')
      .select('*')
      .eq('restaurant_id', restaurantId)
      .order('created_at', { ascending: false })
      .limit(50)

    if (err) setError(err.message)
    else setCalls(data || [])
    setLoading(false)
  }

  useEffect(() => { loadCalls() }, [restaurantId])

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-xl md:text-3xl font-black tracking-tight text-white">AI Call Log</h1>
        <p className="text-white/40 text-sm">{calls.length} calls</p>
      </div>

      {loading ? (
        <LoadingSkeleton />
      ) : error ? (
        <ErrorState message={error} onRetry={loadCalls} />
      ) : calls.length === 0 ? (
        <EmptyState icon="📞" title="No calls yet" description="When your AI answers calls, they'll show up here." />
      ) : (
        <div className="card divide-y divide-white/5">
          {calls.map((call) => {
            const isExpanded = expandedId === call.id
            const callTime = new Date(call.created_at).toLocaleString('en-US', {
              month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit',
            })

            return (
              <div key={call.id}>
                <button
                  onClick={() => setExpandedId(isExpanded ? null : call.id)}
                  className="w-full table-row text-left"
                >
                  <div className="flex items-center gap-4 flex-1 min-w-0">
                    <div className="w-10 h-10 bg-teal/10 rounded-full flex items-center justify-center flex-shrink-0">
                      <span className="text-teal">📞</span>
                    </div>
                    <div className="min-w-0 flex-1">
                      <p className="font-medium text-white truncate">
                        {call.caller_name || call.caller_phone || 'Unknown Caller'}
                      </p>
                      <p className="text-sm text-white/40">
                        {callTime} · {formatDuration(call.duration_seconds)}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    {call.intent && (
                      <span className={cn('badge', intentColors[call.intent] || intentColors.other)}>
                        {call.intent}
                      </span>
                    )}
                    <span className={cn('text-white/30 transition-transform', isExpanded && 'rotate-180')}>
                      ▼
                    </span>
                  </div>
                </button>

                {isExpanded && (
                  <div className="px-3 pb-3 md:px-6 md:pb-4 bg-white/[0.02]">
                    {call.summary ? (
                      <div className="bg-navy rounded-xl p-4 border border-white/5">
                        <p className="text-xs text-white/40 uppercase tracking-wider mb-2">AI Summary</p>
                        <p className="text-sm text-white/80 leading-relaxed">{call.summary}</p>
                      </div>
                    ) : (
                      <p className="text-sm text-white/30 italic">No summary available</p>
                    )}
                    {call.caller_phone && (
                      <p className="text-xs text-white/30 mt-3">📱 {call.caller_phone}</p>
                    )}
                  </div>
                )}
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
