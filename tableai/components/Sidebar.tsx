'use client'

import Link from 'next/link'
import Image from 'next/image'
import { usePathname } from 'next/navigation'
import { useState, useRef, useEffect } from 'react'
import { cn } from '@/lib/utils'
import { useLanguage } from '@/lib/LanguageContext'
import { useRestaurant } from '@/lib/useRestaurant'
import {
  LayoutDashboard,
  CalendarDays,
  Phone,
  Star,
  Gem,
  Package,
  ClipboardCheck,
  DollarSign,
  Megaphone,
  Settings,
  MoreHorizontal,
  Check,
  Plus,
  X,
} from 'lucide-react'

const navItems = [
  { href: '/', labelKey: 'nav.dashboard', icon: LayoutDashboard },
  { href: '/reservations', labelKey: 'nav.reservations', icon: CalendarDays },
  { href: '/calls', labelKey: 'nav.calls', icon: Phone },
  { href: '/reviews', labelKey: 'nav.reviews', icon: Star },
  { href: '/loyalty', labelKey: 'nav.loyalty', icon: Gem },
  { href: '/inventory', labelKey: 'nav.inventory', icon: Package },
  { href: '/compliance', labelKey: 'nav.compliance', icon: ClipboardCheck },
  { href: '/finance', labelKey: 'nav.finance', icon: DollarSign },
  { href: '/marketing', labelKey: 'nav.marketing', icon: Megaphone },
  { href: '/settings', labelKey: 'nav.settings', icon: Settings },
]

const mobileNavItems = [
  { href: '/', labelKey: 'nav.dashboard', icon: LayoutDashboard },
  { href: '/reservations', labelKey: 'nav.reservations', icon: CalendarDays },
  { href: '/calls', labelKey: 'nav.calls', icon: Phone },
  { href: '/reviews', labelKey: 'nav.reviews', icon: Star },
  { href: '/settings', labelKey: 'nav.settings', icon: Settings },
]

const moreNavItems = [
  { href: '/loyalty', labelKey: 'nav.loyalty', icon: Gem },
  { href: '/inventory', labelKey: 'nav.inventory', icon: Package },
  { href: '/compliance', labelKey: 'nav.compliance', icon: ClipboardCheck },
  { href: '/finance', labelKey: 'nav.finance', icon: DollarSign },
  { href: '/marketing', labelKey: 'nav.marketing', icon: Megaphone },
]

function getInitials(name: string): string {
  return name
    .split(/\s+/)
    .slice(0, 2)
    .map((w) => w[0]?.toUpperCase() || '')
    .join('')
}

/* ─── Add Restaurant Modal ─── */
function AddRestaurantModal({
  onClose,
  onAdd,
}: {
  onClose: () => void
  onAdd: (name: string, phone: string, city: string) => Promise<void>
}) {
  const [name, setName] = useState('')
  const [phone, setPhone] = useState('')
  const [city, setCity] = useState('')
  const [saving, setSaving] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!name.trim()) return
    setSaving(true)
    try {
      await onAdd(name.trim(), phone.trim(), city.trim())
    } catch {
      setSaving(false)
    }
  }

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/60" onClick={onClose} />
      <div
        className="relative w-full max-w-sm rounded-2xl p-6"
        style={{
          background: '#0E1225',
          border: '1px solid rgba(87,176,173,0.15)',
          boxShadow: '0 0 60px rgba(87,176,173,0.08)',
        }}
      >
        <div className="flex items-center justify-between mb-5">
          <h3 className="text-white font-semibold text-base">Add New Restaurant</h3>
          <button onClick={onClose} className="text-slate-400 hover:text-white">
            <X size={18} />
          </button>
        </div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="text-xs text-slate-400 mb-1 block">Name *</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-3 py-2.5 rounded-xl text-sm text-white placeholder-slate-600 outline-none focus:ring-1 focus:ring-teal"
              style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(87,176,173,0.1)' }}
              placeholder="Restaurant name"
              required
              autoFocus
            />
          </div>
          <div>
            <label className="text-xs text-slate-400 mb-1 block">Phone</label>
            <input
              type="text"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className="w-full px-3 py-2.5 rounded-xl text-sm text-white placeholder-slate-600 outline-none focus:ring-1 focus:ring-teal"
              style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(87,176,173,0.1)' }}
              placeholder="(555) 123 4567"
            />
          </div>
          <div>
            <label className="text-xs text-slate-400 mb-1 block">City</label>
            <input
              type="text"
              value={city}
              onChange={(e) => setCity(e.target.value)}
              className="w-full px-3 py-2.5 rounded-xl text-sm text-white placeholder-slate-600 outline-none focus:ring-1 focus:ring-teal"
              style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(87,176,173,0.1)' }}
              placeholder="Denver"
            />
          </div>
          <button
            type="submit"
            disabled={saving || !name.trim()}
            className="w-full py-2.5 rounded-xl text-sm font-semibold text-white transition-all disabled:opacity-40"
            style={{ background: '#00C9A7' }}
          >
            {saving ? 'Creating...' : 'Create Restaurant'}
          </button>
        </form>
      </div>
    </div>
  )
}

/* ─── Restaurant Switcher Dropdown ─── */
function RestaurantSwitcher() {
  const { restaurants, activeId, switchRestaurant, addRestaurant, loading } = useRestaurant()
  const [open, setOpen] = useState(false)
  const [showAddModal, setShowAddModal] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  const active = restaurants.find((r) => r.id === activeId)
  const displayName = active?.name || 'Restaurant'
  const initials = getInitials(displayName)
  const { t } = useLanguage()

  useEffect(() => {
    if (!open) return
    function handleClick(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false)
    }
    document.addEventListener('mousedown', handleClick)
    return () => document.removeEventListener('mousedown', handleClick)
  }, [open])

  return (
    <div className="relative" ref={ref}>
      {/* Trigger */}
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left transition-all hover:bg-white/[0.02]"
        style={{
          background: 'rgba(255,255,255,0.03)',
          border: '1px solid rgba(87,176,173,0.1)',
        }}
      >
        <div className="w-8 h-8 rounded-lg bg-teal/10 flex items-center justify-center flex-shrink-0">
          <span className="text-teal text-xs font-bold">{initials}</span>
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium text-white truncate">{displayName}</p>
          <p className="text-[10px] text-slate-500">{t('common.owner')}</p>
        </div>
      </button>

      {/* Dropdown */}
      {open && (
        <div
          className="absolute bottom-full left-0 right-0 mb-2 z-50 rounded-xl overflow-hidden"
          style={{
            background: 'rgba(14,18,37,0.95)',
            backdropFilter: 'blur(24px) saturate(180%)',
            WebkitBackdropFilter: 'blur(24px) saturate(180%)',
            border: '1px solid rgba(87,176,173,0.15)',
            boxShadow: '0 -4px 40px rgba(0,0,0,0.4)',
          }}
        >
          <div className="py-1 max-h-60 overflow-y-auto">
            {loading ? (
              <div className="px-4 py-3 text-sm text-slate-500">Loading...</div>
            ) : restaurants.length === 0 ? (
              <div className="px-4 py-3 text-sm text-slate-500">No restaurants found</div>
            ) : (
              restaurants.map((r) => (
                <button
                  key={r.id}
                  onClick={() => {
                    if (r.id !== activeId) switchRestaurant(r.id)
                    else setOpen(false)
                  }}
                  className="w-full flex items-center gap-3 px-4 py-2.5 text-left hover:bg-white/[0.04] transition-colors"
                >
                  <span className="flex-1 text-sm text-white truncate">{r.name}</span>
                  {r.id === activeId && <Check size={16} className="text-teal flex-shrink-0" />}
                </button>
              ))
            )}
          </div>
          <div style={{ borderTop: '1px solid rgba(87,176,173,0.1)' }}>
            <button
              onClick={() => {
                setOpen(false)
                setShowAddModal(true)
              }}
              className="w-full flex items-center gap-3 px-4 py-2.5 text-left hover:bg-white/[0.04] transition-colors"
            >
              <Plus size={16} className="text-teal" />
              <span className="text-sm text-teal font-medium">Add New Restaurant</span>
            </button>
          </div>
        </div>
      )}

      {/* Add Modal */}
      {showAddModal && (
        <AddRestaurantModal
          onClose={() => setShowAddModal(false)}
          onAdd={addRestaurant}
        />
      )}
    </div>
  )
}

/* ─── More Sheet (Mobile) ─── */
function MoreSheet({ onClose }: { onClose: () => void }) {
  const pathname = usePathname()
  const { t } = useLanguage()

  return (
    <div className="fixed inset-0 z-[55]">
      <div className="absolute inset-0 bg-black/50" onClick={onClose} />
      <div
        className="absolute bottom-0 left-0 right-0 rounded-t-2xl overflow-hidden"
        style={{
          background: 'rgba(8,13,26,0.95)',
          backdropFilter: 'blur(24px) saturate(180%)',
          WebkitBackdropFilter: 'blur(24px) saturate(180%)',
          borderTop: '1px solid rgba(87,176,173,0.15)',
          paddingBottom: 'env(safe-area-inset-bottom, 0px)',
        }}
      >
        {/* Handle + close */}
        <div className="flex items-center justify-between px-5 pt-3 pb-1">
          <div className="w-10 h-1 rounded-full bg-slate-600 mx-auto" />
        </div>
        <div className="flex justify-end px-4">
          <button onClick={onClose} className="p-2 text-slate-400 hover:text-white">
            <X size={20} />
          </button>
        </div>

        {/* Nav items */}
        <div className="px-4 pb-6 space-y-1">
          {moreNavItems.map((item) => {
            const isActive = pathname.startsWith(item.href)
            const Icon = item.icon
            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={onClose}
                className={cn(
                  'flex items-center gap-4 px-4 rounded-xl transition-all',
                  isActive ? 'text-teal' : 'text-slate-300 active:text-white active:bg-white/[0.03]'
                )}
                style={{
                  minHeight: '56px',
                  ...(isActive
                    ? { background: 'rgba(87,176,173,0.08)' }
                    : undefined),
                }}
              >
                <Icon size={22} strokeWidth={isActive ? 2.5 : 1.5} />
                <span className="text-base font-medium">{t(item.labelKey)}</span>
              </Link>
            )
          })}
        </div>
      </div>
    </div>
  )
}

/* ─── Main Sidebar Component ─── */
export default function Sidebar() {
  const pathname = usePathname()
  const { t } = useLanguage()
  const [moreOpen, setMoreOpen] = useState(false)

  const isOnMorePage = moreNavItems.some((item) => pathname.startsWith(item.href))

  return (
    <>
      {/* Desktop Sidebar */}
      <aside
        className="hidden md:flex flex-col w-64 h-screen fixed left-0 top-0 z-40"
        style={{
          background: '#080D1A',
          borderRight: '1px solid rgba(87,176,173,0.1)',
        }}
      >
        {/* Logo */}
        <Link href="/" className="px-5 pt-4 pb-4 flex items-center gap-3 hover:opacity-80 transition-opacity">
          <Image
            src="/logo.png"
            alt="Table AI"
            width={40}
            height={40}
            className="object-contain flex-shrink-0"
            priority
          />
          <div>
            <h1 className="text-xl font-black text-white tracking-tight leading-none">Table <span style={{color:'#00C9A7'}}>AI</span></h1>
            <p className="text-[9px] uppercase tracking-[0.2em] mt-1" style={{color:'#475569'}}>The Restaurant OS</p>
          </div>
        </Link>

        {/* Nav */}
        <nav className="flex-1 px-3 space-y-1 overflow-y-auto">
          {navItems.map((item) => {
            const isActive = item.href === '/' ? pathname === '/' : pathname.startsWith(item.href)
            const Icon = item.icon
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  'flex items-center gap-3 px-4 py-3 rounded-xl text-base font-medium transition-all duration-200 group relative',
                  isActive
                    ? 'text-teal'
                    : 'text-slate-400 hover:text-white hover:bg-white/[0.03]'
                )}
                style={isActive ? {
                  background: 'rgba(87,176,173,0.08)',
                  boxShadow: 'inset 3px 0 0 #57B0AD',
                } : undefined}
              >
                <Icon size={20} strokeWidth={isActive ? 2.5 : 1.5} />
                <span>{t(item.labelKey)}</span>
              </Link>
            )
          })}
        </nav>

        {/* Bottom Restaurant Card */}
        <div className="p-4">
          <RestaurantSwitcher />
        </div>
      </aside>

      {/* Mobile Bottom Nav */}
      <nav
        className="md:hidden fixed bottom-0 left-0 right-0 z-50"
        style={{
          background: 'rgba(8,13,26,0.85)',
          backdropFilter: 'blur(24px) saturate(180%)',
          WebkitBackdropFilter: 'blur(24px) saturate(180%)',
          borderTop: '1px solid rgba(87,176,173,0.12)',
          paddingBottom: 'max(env(safe-area-inset-bottom, 0px), 12px)',
        }}
      >
        <div className="flex justify-around items-center h-16 px-1">
          {mobileNavItems.map((item) => {
            const isActive = item.href === '/' ? pathname === '/' : pathname.startsWith(item.href)
            const Icon = item.icon
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  'relative flex flex-col items-center justify-center min-w-[56px] h-12 rounded-2xl transition-all duration-200',
                  isActive ? 'text-teal' : 'text-slate-500 active:text-slate-400'
                )}
              >
                {isActive && (
                  <div
                    className="absolute -top-1 w-6 h-[3px] rounded-full"
                    style={{
                      background: '#57B0AD',
                      boxShadow: '0 0 8px rgba(87,176,173,0.5)',
                    }}
                  />
                )}
                <Icon size={22} strokeWidth={isActive ? 2.5 : 1.5} />
                {isActive && (
                  <span className="text-[10px] font-semibold mt-0.5 tracking-tight">{t(item.labelKey)}</span>
                )}
              </Link>
            )
          })}

          {/* More button */}
          <button
            onClick={() => setMoreOpen(true)}
            className={cn(
              'relative flex flex-col items-center justify-center min-w-[56px] h-12 rounded-2xl transition-all duration-200',
              isOnMorePage ? 'text-teal' : 'text-slate-500 active:text-slate-400'
            )}
          >
            {isOnMorePage && (
              <div
                className="absolute -top-1 w-6 h-[3px] rounded-full"
                style={{
                  background: '#57B0AD',
                  boxShadow: '0 0 8px rgba(87,176,173,0.5)',
                }}
              />
            )}
            <MoreHorizontal size={22} strokeWidth={isOnMorePage ? 2.5 : 1.5} />
            {isOnMorePage && (
              <span className="text-[10px] font-semibold mt-0.5 tracking-tight">More</span>
            )}
          </button>
        </div>
      </nav>

      {/* More Sheet */}
      {moreOpen && <MoreSheet onClose={() => setMoreOpen(false)} />}
    </>
  )
}
