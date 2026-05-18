'use client'

import { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'
import { useRestaurantId } from '@/lib/useRestaurantId'
import { Review, ReviewRequest } from '@/lib/types'
import { LoadingSkeleton, EmptyState, ErrorState } from '@/components/LoadingState'

function StarRating({ rating }: { rating: number }) {
  return (
    <div className="flex gap-0.5">
      {[1, 2, 3, 4, 5].map((star) => (
        <span key={star} className={star <= rating ? 'text-amber-400' : 'text-white/10'}>
          ★
        </span>
      ))}
    </div>
  )
}

function SmartReviewSetup({ restaurantId }: { restaurantId: string }) {
  const [placeId, setPlaceId] = useState('')
  const [threshold, setThreshold] = useState<4 | 5>(4)
  const [active, setActive] = useState(false)
  const [saving, setSaving] = useState(false)
  const [copied, setCopied] = useState(false)
  const [loaded, setLoaded] = useState(false)

  useEffect(() => {
    async function loadSettings() {
      const { data } = await supabase
        .from('restaurants')
        .select('google_place_id')
        .eq('id', restaurantId)
        .single()
      if (data?.google_place_id) {
        setPlaceId(data.google_place_id)
        setActive(true)
      }
      setLoaded(true)
    }
    loadSettings()
  }, [restaurantId])

  async function handleSave() {
    setSaving(true)
    await supabase
      .from('restaurants')
      .update({ google_place_id: placeId || null })
      .eq('id', restaurantId)
    setSaving(false)
  }

  function handleCopyLink() {
    const link = `https://tableai.io/feedback/${restaurantId}`
    navigator.clipboard.writeText(link)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  if (!loaded) return null

  return (
    <div className="card p-6 space-y-5">
      <div>
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          ⭐ Smart Review Requests
        </h2>
        <p className="text-white/50 text-sm mt-1">
          Automatically ask guests for reviews after their visit. Happy guests go to Google. Unhappy guests send private feedback to you.
        </p>
      </div>

      <div className="space-y-4">
        {/* Google Place ID */}
        <div>
          <label className="block text-sm font-medium text-white/70 mb-1">Google Place ID</label>
          <input
            type="text"
            value={placeId}
            onChange={(e) => setPlaceId(e.target.value)}
            placeholder="ChIJ..."
            className="w-full rounded-xl px-4 py-3 text-white placeholder-white/30 focus:outline-none focus:ring-2 focus:ring-[#00C9A7]/50"
            style={{
              background: 'rgba(255,255,255,0.05)',
              border: '1px solid rgba(0,201,167,0.15)',
            }}
          />
          <a
            href="https://support.google.com/business/answer/10342818"
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs text-[#00C9A7]/70 hover:text-[#00C9A7] mt-1 inline-block"
          >
            How to find your Place ID →
          </a>
        </div>

        {/* Star Threshold */}
        <div>
          <label className="block text-sm font-medium text-white/70 mb-1">Star threshold</label>
          <div className="flex gap-2">
            <button
              onClick={() => setThreshold(4)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                threshold === 4
                  ? 'bg-[#00C9A7]/20 text-[#00C9A7] border border-[#00C9A7]/40'
                  : 'bg-white/5 text-white/50 border border-white/10 hover:border-white/20'
              }`}
            >
              Send to Google at 4+ stars
            </button>
            <button
              onClick={() => setThreshold(5)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                threshold === 5
                  ? 'bg-[#00C9A7]/20 text-[#00C9A7] border border-[#00C9A7]/40'
                  : 'bg-white/5 text-white/50 border border-white/10 hover:border-white/20'
              }`}
            >
              Send to Google at 5 stars only
            </button>
          </div>
        </div>

        {/* Active Toggle */}
        <div className="flex items-center gap-3">
          <button
            onClick={() => setActive(!active)}
            className={`relative w-12 h-7 rounded-full transition-colors duration-200 ${
              active ? 'bg-[#00C9A7]' : 'bg-white/10'
            }`}
          >
            <span
              className={`absolute top-1 left-1 w-5 h-5 rounded-full bg-white transition-transform duration-200 ${
                active ? 'translate-x-5' : 'translate-x-0'
              }`}
            />
          </button>
          <span className="text-sm text-white/70">{active ? 'Active' : 'Inactive'}</span>
        </div>
      </div>

      {/* Actions */}
      <div className="flex flex-col sm:flex-row gap-3 pt-2">
        <button
          onClick={handleSave}
          disabled={saving}
          className="btn-primary text-sm py-2.5 px-6"
        >
          {saving ? 'Saving...' : 'Save Settings'}
        </button>
        <button
          onClick={handleCopyLink}
          className="btn-secondary text-sm py-2.5 px-6 relative"
        >
          {copied ? '✓ Copied!' : 'Copy Feedback Link'}
        </button>
      </div>
    </div>
  )
}

function PrivateFeedback({ restaurantId }: { restaurantId: string }) {
  const [feedback, setFeedback] = useState<ReviewRequest[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      const { data } = await supabase
        .from('review_requests')
        .select('*')
        .eq('restaurant_id', restaurantId)
        .eq('is_private', true)
        .order('created_at', { ascending: false })
        .limit(50)
      setFeedback(data || [])
      setLoading(false)
    }
    load()
  }, [restaurantId])

  if (loading || feedback.length === 0) return null

  return (
    <div className="card p-6 space-y-4">
      <div className="flex items-center gap-3">
        <h2 className="text-lg font-bold text-white">🔒 Private Feedback</h2>
        <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-red-500/20 text-red-400 text-xs font-bold">
          {feedback.length}
        </span>
      </div>

      <div className="space-y-3">
        {feedback.map((item) => {
          const date = new Date(item.created_at).toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric',
          })

          return (
            <div
              key={item.id}
              className="rounded-xl p-4 space-y-2"
              style={{
                background: 'rgba(255,255,255,0.03)',
                borderLeft: '3px solid rgba(239,68,68,0.5)',
              }}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <p className="font-medium text-white text-sm">
                    {item.guest_name || 'Anonymous'}
                  </p>
                  <StarRating rating={item.rating} />
                </div>
                <span className="text-xs text-white/30">{date}</span>
              </div>
              {item.feedback_text && (
                <p className="text-white/60 text-sm leading-relaxed">{item.feedback_text}</p>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default function ReviewsPage() {
  const restaurantId = useRestaurantId()
  const [reviews, setReviews] = useState<Review[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [approvingId, setApprovingId] = useState<string | null>(null)

  async function loadReviews() {
    setLoading(true)
    setError(null)
    const { data, error: err } = await supabase
      .from('reviews')
      .select('*')
      .eq('restaurant_id', restaurantId)
      .order('created_at', { ascending: false })
      .limit(50)

    if (err) setError(err.message)
    else setReviews(data || [])
    setLoading(false)
  }

  useEffect(() => { loadReviews() }, [restaurantId])

  async function approveResponse(reviewId: string) {
    setApprovingId(reviewId)
    const { error: err } = await supabase
      .from('reviews')
      .update({ response_status: 'approved' })
      .eq('id', reviewId)

    if (!err) {
      setReviews(reviews.map(r => r.id === reviewId ? { ...r, response_status: 'approved' } : r))
    }
    setApprovingId(null)
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="page-title">Reviews</h1>
        <div className="flex items-center gap-2 text-sm">
          <span className="text-white/40">
            {reviews.filter(r => r.response_status === 'pending').length} pending
          </span>
        </div>
      </div>

      {/* Smart Review Requests Setup */}
      <SmartReviewSetup restaurantId={restaurantId} />

      {/* Private Feedback */}
      <PrivateFeedback restaurantId={restaurantId} />

      {/* Existing Reviews List */}
      {loading ? (
        <LoadingSkeleton />
      ) : error ? (
        <ErrorState message={error} onRetry={loadReviews} />
      ) : reviews.length === 0 ? (
        <EmptyState icon="⭐" title="No reviews yet" description="When customers leave reviews, they will appear here with AI drafted responses." />
      ) : (
        <div className="space-y-4">
          {reviews.map((review) => {
            const reviewDate = new Date(review.created_at).toLocaleDateString('en-US', {
              month: 'short', day: 'numeric', year: 'numeric',
            })

            return (
              <div key={review.id} className="card p-6 space-y-4">
                {/* Header */}
                <div className="flex items-start justify-between">
                  <div>
                    <div className="flex items-center gap-3 mb-1">
                      <p className="font-semibold text-white">{review.reviewer_name}</p>
                      {review.platform && (
                        <span className="badge bg-white/5 text-white/40">{review.platform}</span>
                      )}
                    </div>
                    <div className="flex items-center gap-3">
                      <StarRating rating={review.rating} />
                      <span className="text-xs text-white/30">{reviewDate}</span>
                    </div>
                  </div>
                  <span className={`badge ${
                    review.response_status === 'pending' ? 'bg-amber-500/20 text-amber-400' :
                    review.response_status === 'approved' ? 'bg-emerald-500/20 text-emerald-400' :
                    'bg-teal/20 text-teal'
                  }`}>
                    {review.response_status}
                  </span>
                </div>

                {/* Review Text */}
                <p className="text-white/70 text-sm leading-relaxed">{review.review_text}</p>

                {/* AI Response */}
                {review.ai_response && (
                  <div className="bg-teal/5 border border-teal/10 rounded-xl p-3 md:p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-teal text-sm">🤖</span>
                      <p className="text-xs font-semibold text-teal uppercase tracking-wider">AI Drafted Response</p>
                    </div>
                    <p className="text-sm text-white/60 leading-relaxed break-words">{review.ai_response}</p>

                    {review.response_status === 'pending' && (
                      <div className="flex flex-col md:flex-row gap-2 mt-3 md:mt-4">
                        <button
                          onClick={() => approveResponse(review.id)}
                          disabled={approvingId === review.id}
                          className="btn-primary text-sm py-2 w-full md:w-auto"
                        >
                          {approvingId === review.id ? 'Approving...' : '✓ Approve & Send'}
                        </button>
                        <button className="btn-secondary text-sm py-2 w-full md:w-auto">
                          ✏️ Edit
                        </button>
                      </div>
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
