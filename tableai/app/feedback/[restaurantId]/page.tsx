'use client'

import { Suspense, useEffect, useState } from 'react'
import { useParams, useSearchParams } from 'next/navigation'
import { supabase } from '@/lib/supabase'

interface RestaurantInfo {
  id: string
  name: string
  logo_url: string | null
  google_place_id: string | null
}

export default function FeedbackPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center" style={{ background: '#050810' }}>
        <div className="animate-pulse text-white/40 text-lg">Loading...</div>
      </div>
    }>
      <FeedbackContent />
    </Suspense>
  )
}

function FeedbackContent() {
  const params = useParams()
  const searchParams = useSearchParams()
  const restaurantId = params.restaurantId as string

  const guestName = searchParams.get('name') || null
  const guestPhone = searchParams.get('phone') || null
  const reservationId = searchParams.get('reservationId') || null

  const [restaurant, setRestaurant] = useState<RestaurantInfo | null>(null)
  const [loading, setLoading] = useState(true)
  const [rating, setRating] = useState<number | null>(null)
  const [feedbackText, setFeedbackText] = useState('')
  const [submitted, setSubmitted] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [phase, setPhase] = useState<'rate' | 'positive' | 'negative' | 'done'>('rate')

  useEffect(() => {
    async function loadRestaurant() {
      const { data } = await supabase
        .from('restaurants')
        .select('id, name, logo_url, google_place_id')
        .eq('id', restaurantId)
        .single()
      setRestaurant(data)
      setLoading(false)
    }
    loadRestaurant()
  }, [restaurantId])

  async function handleRate(stars: number) {
    setRating(stars)

    if (stars >= 4) {
      // Save to review_requests
      await supabase.from('review_requests').insert({
        restaurant_id: restaurantId,
        guest_name: guestName,
        guest_phone: guestPhone,
        rating: stars,
        sent_to_google: true,
        is_private: false,
        reservation_id: reservationId,
      })
      setPhase('positive')
    } else {
      setPhase('negative')
    }
  }

  async function handleSubmitFeedback() {
    if (!feedbackText.trim()) return
    setSubmitting(true)

    await supabase.from('review_requests').insert({
      restaurant_id: restaurantId,
      guest_name: guestName,
      guest_phone: guestPhone,
      rating: rating,
      feedback_text: feedbackText.trim(),
      sent_to_google: false,
      is_private: true,
      reservation_id: reservationId,
    })

    setSubmitting(false)
    setSubmitted(true)
    setPhase('done')
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ background: '#050810' }}>
        <div className="animate-pulse text-white/40 text-lg">Loading...</div>
      </div>
    )
  }

  if (!restaurant) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ background: '#050810' }}>
        <div className="text-white/60 text-center">
          <p className="text-2xl mb-2">🍽️</p>
          <p>Restaurant not found.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-8" style={{ background: '#050810' }}>
      <div className="w-full max-w-md text-center space-y-8">
        {/* Restaurant branding */}
        {restaurant.logo_url && (
          <img
            src={restaurant.logo_url}
            alt={restaurant.name}
            className="w-20 h-20 rounded-2xl mx-auto object-cover"
          />
        )}
        <h1 className="text-2xl font-bold text-white">{restaurant.name}</h1>

        {/* Rating phase */}
        {phase === 'rate' && (
          <div className="space-y-6">
            <p className="text-white/70 text-lg">How was your experience tonight?</p>
            <div className="flex justify-center gap-3">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  onClick={() => handleRate(star)}
                  className="text-5xl transition-transform duration-150 hover:scale-125 active:scale-110 focus:outline-none"
                  aria-label={`${star} star${star > 1 ? 's' : ''}`}
                >
                  <span className={rating !== null && star <= rating ? 'opacity-100' : 'opacity-30'}>
                    ⭐
                  </span>
                </button>
              ))}
            </div>
            {guestName && (
              <p className="text-white/30 text-sm">Thanks for dining with us, {guestName}!</p>
            )}
          </div>
        )}

        {/* Positive rating — redirect to Google */}
        {phase === 'positive' && (
          <div className="space-y-6 animate-fadeIn">
            <div className="text-5xl">🎉</div>
            <p className="text-white/80 text-lg">
              Thank you! We love hearing that.
              {restaurant.google_place_id
                ? ' Share your experience on Google:'
                : ''}
            </p>
            {restaurant.google_place_id ? (
              <a
                href={`https://search.google.com/local/writereview?placeid=${restaurant.google_place_id}`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block px-8 py-4 rounded-xl font-semibold text-lg transition-all duration-200 active:scale-95 hover:opacity-90"
                style={{ background: '#00C9A7', color: '#050810' }}
              >
                Leave a Google Review
              </a>
            ) : (
              <p className="text-white/50 text-sm">Your kind words mean the world to us.</p>
            )}
          </div>
        )}

        {/* Negative rating — private feedback form */}
        {phase === 'negative' && !submitted && (
          <div className="space-y-6 animate-fadeIn">
            <p className="text-white/80 text-lg">
              We are sorry to hear that. Please tell us what happened:
            </p>
            <textarea
              value={feedbackText}
              onChange={(e) => setFeedbackText(e.target.value)}
              placeholder="Tell us about your experience..."
              rows={4}
              className="w-full rounded-xl px-4 py-3 text-white placeholder-white/30 focus:outline-none focus:ring-2 focus:ring-[#00C9A7]/50 resize-none"
              style={{
                background: 'rgba(255,255,255,0.05)',
                border: '1px solid rgba(0,201,167,0.15)',
              }}
            />
            <button
              onClick={handleSubmitFeedback}
              disabled={submitting || !feedbackText.trim()}
              className="w-full px-8 py-4 rounded-xl font-semibold text-lg transition-all duration-200 active:scale-95 hover:opacity-90 disabled:opacity-40 disabled:cursor-not-allowed"
              style={{ background: '#00C9A7', color: '#050810' }}
            >
              {submitting ? 'Sending...' : 'Send Feedback'}
            </button>
          </div>
        )}

        {/* Done — thank you for negative feedback */}
        {phase === 'done' && (
          <div className="space-y-4 animate-fadeIn">
            <div className="text-5xl">🙏</div>
            <p className="text-white/80 text-lg">
              Thank you for letting us know. A manager will reach out soon.
            </p>
          </div>
        )}
      </div>

      <style jsx>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fadeIn {
          animation: fadeIn 0.3s ease-out;
        }
      `}</style>
    </div>
  )
}
