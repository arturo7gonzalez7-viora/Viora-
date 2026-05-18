'use client'

import { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'
import { useRestaurantId } from '@/lib/useRestaurantId'
import { LoadingSkeleton, EmptyState } from '@/components/LoadingState'

interface Promotion {
  id: string
  restaurant_id: string
  name: string
  description: string
  type: string
  start_date: string
  end_date: string
  status: string
  created_at: string
}

interface ContentPost {
  id: string
  restaurant_id: string
  platform: string
  content: string
  media_url: string | null
  scheduled_at: string | null
  status: string
  created_at: string
}

export default function MarketingPage() {
  const restaurantId = useRestaurantId()
  const [promotions, setPromotions] = useState<Promotion[]>([])
  const [posts, setPosts] = useState<ContentPost[]>([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<'promotions' | 'content'>('promotions')

  useEffect(() => {
    async function load() {
      const [promoRes, postRes] = await Promise.all([
        supabase.from('promotions').select('*').eq('restaurant_id', restaurantId).order('created_at', { ascending: false }).limit(20),
        supabase.from('content_posts').select('*').eq('restaurant_id', restaurantId).order('created_at', { ascending: false }).limit(20),
      ])
      setPromotions(promoRes.data || [])
      setPosts(postRes.data || [])
      setLoading(false)
    }
    load()
  }, [restaurantId])

  if (loading) return <div className="space-y-6"><h1 className="text-xl md:text-3xl font-black tracking-tight text-white">Marketing</h1><LoadingSkeleton /></div>

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-xl md:text-3xl font-black tracking-tight text-white">Marketing</h1>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 bg-navy-50 rounded-xl p-1 w-full md:w-fit">
        <button
          onClick={() => setActiveTab('promotions')}
          className={`flex-1 md:flex-none px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeTab === 'promotions' ? 'bg-teal text-navy' : 'text-white/40 hover:text-white'}`}
        >
          Promotions
        </button>
        <button
          onClick={() => setActiveTab('content')}
          className={`flex-1 md:flex-none px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeTab === 'content' ? 'bg-teal text-navy' : 'text-white/40 hover:text-white'}`}
        >
          Content
        </button>
      </div>

      {activeTab === 'promotions' ? (
        promotions.length === 0 ? (
          <EmptyState icon="📣" title="No promotions yet" description="Create promotions to attract more customers." />
        ) : (
          <div className="space-y-4">
            {promotions.map((promo) => (
              <div key={promo.id} className="card p-4 md:p-6">
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="font-semibold text-white">{promo.name}</h3>
                    <p className="text-sm text-white/50 mt-1">{promo.description}</p>
                    <p className="text-xs text-white/30 mt-2">
                      {promo.start_date} → {promo.end_date}
                    </p>
                  </div>
                  <span className={`badge ${promo.status === 'active' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-white/10 text-white/40'}`}>
                    {promo.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )
      ) : (
        posts.length === 0 ? (
          <EmptyState icon="✍️" title="No content posts yet" description="Schedule social media content to keep your audience engaged." />
        ) : (
          <div className="space-y-4">
            {posts.map((post) => (
              <div key={post.id} className="card p-4 md:p-6">
                <div className="flex items-start justify-between mb-2">
                  <span className="badge bg-white/5 text-white/40">{post.platform}</span>
                  <span className={`badge ${post.status === 'published' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-amber-500/20 text-amber-400'}`}>
                    {post.status}
                  </span>
                </div>
                <p className="text-sm text-white/70">{post.content}</p>
                {post.scheduled_at && (
                  <p className="text-xs text-white/30 mt-2">
                    Scheduled: {new Date(post.scheduled_at).toLocaleString()}
                  </p>
                )}
              </div>
            ))}
          </div>
        )
      )}
    </div>
  )
}
