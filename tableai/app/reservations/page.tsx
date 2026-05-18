'use client'

import { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'
import { useRestaurantId } from '@/lib/useRestaurantId'
import { Reservation } from '@/lib/types'
import { formatTime, formatDate, cn } from '@/lib/utils'
import { LoadingSkeleton, EmptyState, ErrorState } from '@/components/LoadingState'
import Modal from '@/components/Modal'
import { Plus } from 'lucide-react'

const statusStyles: Record<string, string> = {
  confirmed: 'badge-confirmed',
  cancelled: 'badge-cancelled',
  'no-show': 'badge-no-show',
  seated: 'badge-seated',
  completed: 'badge bg-teal/20 text-teal',
}

export default function ReservationsPage() {
  const restaurantId = useRestaurantId()
  const [reservations, setReservations] = useState<Reservation[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showModal, setShowModal] = useState(false)
  const [saving, setSaving] = useState(false)

  const [form, setForm] = useState({
    guest_name: '',
    guest_phone: '',
    party_size: '2',
    date: new Date().toISOString().split('T')[0],
    time: '19:00',
    notes: '',
  })

  async function loadReservations() {
    setLoading(true)
    setError(null)
    const { data, error: err } = await supabase
      .from('reservations')
      .select('*')
      .eq('restaurant_id', restaurantId)
      .order('date', { ascending: false })
      .order('time', { ascending: true })
      .limit(50)

    if (err) {
      setError(err.message)
    } else {
      setReservations(data || [])
    }
    setLoading(false)
  }

  useEffect(() => { loadReservations() }, [restaurantId])

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setSaving(true)
    const { error: err } = await supabase.from('reservations').insert({
      restaurant_id: restaurantId,
      guest_name: form.guest_name,
      guest_phone: form.guest_phone,
      party_size: parseInt(form.party_size),
      date: form.date,
      time: form.time,
      notes: form.notes || null,
      status: 'confirmed',
    })

    if (!err) {
      setShowModal(false)
      setForm({ guest_name: '', guest_phone: '', party_size: '2', date: new Date().toISOString().split('T')[0], time: '19:00', notes: '' })
      loadReservations()
    }
    setSaving(false)
  }

  return (
    <div className="space-y-4 md:space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-xl md:text-3xl font-black tracking-tight text-white">Reservations</h1>
        {/* Desktop add button */}
        <button onClick={() => setShowModal(true)} className="btn-primary text-sm hidden md:flex items-center gap-2">
          <Plus size={16} />
          Add Reservation
        </button>
      </div>

      {loading ? (
        <LoadingSkeleton />
      ) : error ? (
        <ErrorState message={error} onRetry={loadReservations} />
      ) : reservations.length === 0 ? (
        <EmptyState icon="📅" title="No reservations yet" description="Add your first reservation to get started." />
      ) : (
        <div className="card">
          <div className="divide-y divide-white/5">
            {reservations.map((res) => (
              <div key={res.id} className="table-row min-h-[56px]">
                <div className="flex items-center gap-3 md:gap-4 flex-1 min-w-0">
                  <div className="w-11 h-11 md:w-12 md:h-12 bg-white/5 rounded-xl flex flex-col items-center justify-center flex-shrink-0">
                    <span className="text-[11px] md:text-xs font-bold text-teal">{formatTime(res.time)}</span>
                  </div>
                  <div className="min-w-0 flex-1">
                    <p className="font-medium text-white text-sm truncate">{res.guest_name}</p>
                    <p className="text-xs text-white/40 truncate">
                      {formatDate(res.date)} · Party of {res.party_size}
                    </p>
                  </div>
                </div>
                <span className={cn('ml-2 flex-shrink-0', statusStyles[res.status] || 'badge bg-white/10 text-white/50')}>
                  {res.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Mobile FAB — floating action button */}
      <button
        onClick={() => setShowModal(true)}
        className="md:hidden fixed bottom-20 left-4 z-40 w-14 h-14 rounded-full flex items-center justify-center shadow-2xl active:scale-95 transition-transform"
        style={{
          background: '#57B0AD',
          boxShadow: '0 4px 20px rgba(87,176,173,0.4), 0 0 40px rgba(87,176,173,0.15)',
          marginBottom: 'env(safe-area-inset-bottom, 0px)',
        }}
        aria-label="Add Reservation"
      >
        <Plus size={24} className="text-white" strokeWidth={2.5} />
      </button>

      {/* Add Reservation Modal */}
      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="New Reservation">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs md:text-sm text-white/60 mb-1">Guest Name</label>
            <input
              type="text"
              required
              value={form.guest_name}
              onChange={(e) => setForm({ ...form, guest_name: e.target.value })}
              className="input-field"
              placeholder="John Smith"
              autoComplete="name"
            />
          </div>
          <div>
            <label className="block text-xs md:text-sm text-white/60 mb-1">Phone</label>
            <input
              type="tel"
              required
              value={form.guest_phone}
              onChange={(e) => setForm({ ...form, guest_phone: e.target.value })}
              className="input-field"
              placeholder="(555) 123-4567"
              autoComplete="tel"
              inputMode="tel"
            />
          </div>
          <div className="grid grid-cols-2 gap-3 md:gap-4">
            <div>
              <label className="block text-xs md:text-sm text-white/60 mb-1">Date</label>
              <input
                type="date"
                required
                value={form.date}
                onChange={(e) => setForm({ ...form, date: e.target.value })}
                className="input-field"
              />
            </div>
            <div>
              <label className="block text-xs md:text-sm text-white/60 mb-1">Time</label>
              <input
                type="time"
                required
                value={form.time}
                onChange={(e) => setForm({ ...form, time: e.target.value })}
                className="input-field"
              />
            </div>
          </div>
          <div>
            <label className="block text-xs md:text-sm text-white/60 mb-1">Party Size</label>
            <select
              value={form.party_size}
              onChange={(e) => setForm({ ...form, party_size: e.target.value })}
              className="input-field"
            >
              {[1,2,3,4,5,6,7,8,10,12,15,20].map(n => (
                <option key={n} value={n}>{n} {n === 1 ? 'guest' : 'guests'}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-xs md:text-sm text-white/60 mb-1">Notes (optional)</label>
            <textarea
              value={form.notes}
              onChange={(e) => setForm({ ...form, notes: e.target.value })}
              className="input-field"
              rows={2}
              placeholder="Birthday, allergies, special requests..."
            />
          </div>
          <div className="flex flex-col-reverse md:flex-row gap-3 pt-2">
            <button type="button" onClick={() => setShowModal(false)} className="btn-secondary flex-1 text-sm">
              Cancel
            </button>
            <button type="submit" disabled={saving} className="btn-primary flex-1 text-sm">
              {saving ? 'Saving...' : 'Confirm Reservation'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  )
}
