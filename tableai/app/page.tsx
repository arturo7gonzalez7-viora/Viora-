'use client'

import { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'
import { useRestaurantId } from '@/lib/useRestaurantId'
import { getToday } from '@/lib/utils'
import { LoadingCards } from '@/components/LoadingState'
import { useLanguage } from '@/lib/LanguageContext'
import Link from 'next/link'
import { CalendarDays, Phone, Star, Gem, Plus, DollarSign, ArrowRight } from 'lucide-react'

interface Stats {
  reservations: number
  calls: number
  reviews: number
  loyaltyMembers: number
}

// Decorative sparkline bars
function Sparkline() {
  const heights = [40, 65, 45, 80, 55, 70, 50, 90, 60, 75, 85, 55]
  return (
    <div className="sparkline-bar mt-3 md:mt-4">
      {heights.map((h, i) => (
        <span
          key={i}
          style={{
            height: `${h}%`,
            animationDelay: `${i * 0.15}s`,
          }}
        />
      ))}
    </div>
  )
}

// Glowing teal indicator dot
function GlowDot() {
  return (
    <div className="relative">
      <div className="w-2.5 h-2.5 md:w-3 md:h-3 rounded-full bg-teal" />
      <div className="absolute inset-0 w-2.5 h-2.5 md:w-3 md:h-3 rounded-full bg-teal opacity-40 animate-ping" />
    </div>
  )
}

function useGreeting(t: (key: string) => string) {
  const hour = new Date().getHours()
  if (hour < 12) return t('dashboard.greeting.morning')
  if (hour < 18) return t('dashboard.greeting.afternoon')
  return t('dashboard.greeting.evening')
}

export default function Dashboard() {
  const { t } = useLanguage()
  const restaurantId = useRestaurantId()
  const [stats, setStats] = useState<Stats>({ reservations: 0, calls: 0, reviews: 0, loyaltyMembers: 0 })
  const [loading, setLoading] = useState(true)
  const greeting = useGreeting(t)
  const today = getToday()

  useEffect(() => {
    async function loadStats() {
      try {
        const [resResult, callResult, reviewResult, loyaltyResult] = await Promise.all([
          supabase.from('reservations').select('id', { count: 'exact', head: true }).eq('restaurant_id', restaurantId).eq('date', today),
          supabase.from('calls').select('id', { count: 'exact', head: true }).eq('restaurant_id', restaurantId).gte('created_at', today),
          supabase.from('reviews').select('id', { count: 'exact', head: true }).eq('restaurant_id', restaurantId).eq('response_status', 'pending'),
          supabase.from('loyalty_members').select('id', { count: 'exact', head: true }).eq('restaurant_id', restaurantId),
        ])

        setStats({
          reservations: resResult.count || 0,
          calls: callResult.count || 0,
          reviews: reviewResult.count || 0,
          loyaltyMembers: loyaltyResult.count || 0,
        })
      } catch (err) {
        console.error('Failed to load stats:', err)
      } finally {
        setLoading(false)
      }
    }
    loadStats()
  }, [today, restaurantId])

  const statCards = [
    { label: t('dashboard.stat.reservations'), value: stats.reservations, icon: CalendarDays },
    { label: t('dashboard.stat.calls'), value: stats.calls, icon: Phone },
    { label: t('dashboard.stat.reviews'), value: stats.reviews, icon: Star },
    { label: t('dashboard.stat.loyalty'), value: stats.loyaltyMembers, icon: Gem },
  ]

  const quickActions = [
    { label: t('dashboard.action.reservation'), icon: Plus, href: '/reservations' },
    { label: t('dashboard.action.sale'), icon: DollarSign, href: '/finance' },
    { label: t('dashboard.action.calls'), icon: Phone, href: '/calls' },
  ]

  return (
    <div className="space-y-5 md:space-y-8">
      {/* Greeting */}
      <div>
        <h1 className="text-3xl md:text-5xl font-black tracking-tight">
          {greeting} <span className="text-teal">Casa Mariachi</span>
        </h1>
        <p className="text-slate-500 mt-1 md:mt-2 text-xs md:text-sm">{t('dashboard.subtitle')}</p>
      </div>

      {/* Stats — 2x2 on mobile, 4-col on desktop */}
      {loading ? (
        <LoadingCards />
      ) : (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 md:gap-4">
          {statCards.map((card) => (
            <div key={card.label} className="stat-card !p-4 md:!p-6 group">
              <div className="flex items-start justify-between mb-0.5 md:mb-1">
                <p className="text-[10px] md:text-[11px] uppercase tracking-[0.12em] md:tracking-[0.15em] text-slate-500 font-medium leading-tight">{card.label}</p>
                <GlowDot />
              </div>
              <p className="text-3xl md:text-5xl font-black text-white mt-2 md:mt-3">{card.value}</p>
              <Sparkline />
            </div>
          ))}
        </div>
      )}

      {/* Quick Actions — stacked on mobile */}
      <div>
        <h2 className="text-base md:text-lg font-bold text-white mb-3 md:mb-4">{t('dashboard.quickactions')}</h2>
        <div className="flex flex-col md:flex-row md:flex-wrap gap-2 md:gap-3">
          {quickActions.map((action) => {
            const Icon = action.icon
            return (
              <Link
                key={action.label}
                href={action.href}
                className="btn-secondary flex items-center gap-2 group w-full md:w-auto justify-center md:justify-start"
              >
                <Icon size={16} className="text-teal" />
                <span className="text-sm">{action.label}</span>
                <ArrowRight size={14} className="text-slate-600 group-hover:text-teal transition-colors ml-auto md:ml-1" />
              </Link>
            )
          })}
        </div>
      </div>

      {/* Recent Activity */}
      <div className="card">
        <div className="p-4 md:p-6" style={{ borderBottom: '1px solid rgba(87,176,173,0.08)' }}>
          <h2 className="text-base md:text-lg font-bold text-white">{t('dashboard.activity')}</h2>
        </div>
        <div>
          {[
            { icon: CalendarDays, title: 'New reservation', desc: 'Check the Reservations tab for details', time: t('common.today') },
            { icon: Phone, title: 'AI answered a call', desc: 'View call logs for transcripts', time: t('common.today') },
            { icon: Star, title: 'New review received', desc: 'AI drafted a response — needs your approval', time: t('common.today') },
          ].map((item, i) => {
            const Icon = item.icon
            return (
              <div
                key={i}
                className="p-3 md:p-4 flex items-center gap-3 md:gap-4 hover:bg-white/[0.02] transition-colors active:bg-white/[0.04]"
                style={{ borderBottom: i < 2 ? '1px solid rgba(87,176,173,0.06)' : undefined }}
              >
                <div
                  className="w-9 h-9 md:w-10 md:h-10 rounded-xl flex items-center justify-center flex-shrink-0"
                  style={{ background: 'rgba(87,176,173,0.08)' }}
                >
                  <Icon size={16} className="text-teal md:hidden" />
                  <Icon size={18} className="text-teal hidden md:block" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-white">{item.title}</p>
                  <p className="text-xs text-slate-500 truncate">{item.desc}</p>
                </div>
                <span className="text-[10px] md:text-xs text-slate-600 flex-shrink-0">{item.time}</span>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
