'use client'

import { useState } from 'react'
import Image from 'next/image'
import { Bell } from 'lucide-react'
import { useRestaurant } from '@/lib/useRestaurant'

export default function TopBar({ restaurantName: fallbackName }: { restaurantName: string }) {
  const [showNotifications, setShowNotifications] = useState(false)
  const { activeRestaurant } = useRestaurant()
  const restaurantName = activeRestaurant?.name || fallbackName

  return (
    <header
      className="fixed top-0 left-0 right-0 md:left-64 z-30 flex items-center justify-between px-4 md:px-6"
      style={{
        paddingTop: 'env(safe-area-inset-top, 0px)',
        minHeight: '56px',
        height: 'calc(56px + env(safe-area-inset-top, 0px))',
        background: 'rgba(5,8,16,0.8)',
        backdropFilter: 'blur(20px) saturate(180%)',
        WebkitBackdropFilter: 'blur(20px) saturate(180%)',
        borderBottom: '1px solid rgba(87,176,173,0.08)',
      }}
    >
      {/* Left: Logo on mobile, restaurant name on desktop */}
      <div className="flex items-center gap-3">
        <Image
          src="/logo.png"
          alt="Table AI"
          width={30}
          height={30}
          className="object-contain flex-shrink-0 md:hidden"
        />
        <p className="hidden md:block text-slate-500 text-sm font-medium">{restaurantName}</p>
      </div>

      {/* Center: Restaurant name on mobile */}
      <div className="md:hidden absolute left-1/2 -translate-x-1/2">
        <h1 className="text-sm font-bold text-white tracking-tight whitespace-nowrap">
          {restaurantName}
        </h1>
      </div>

      {/* Right side */}
      <div className="flex items-center gap-2 relative">
        {/* Notification Bell */}
        <button
          onClick={() => setShowNotifications(!showNotifications)}
          className="relative p-2.5 md:p-2 rounded-xl hover:bg-white/[0.03] transition-all duration-200 group"
          aria-label="Notifications"
        >
          <Bell size={18} className="text-slate-400 group-hover:text-white transition-colors" />
          <span
            className="absolute top-2 right-2 md:top-1.5 md:right-1.5 w-2 h-2 rounded-full"
            style={{ background: '#57B0AD', boxShadow: '0 0 6px rgba(87,176,173,0.6)' }}
          />
        </button>

        {/* Dropdown */}
        {showNotifications && (
          <>
            {/* Backdrop to close on mobile */}
            <div
              className="fixed inset-0 z-40 md:hidden"
              onClick={() => setShowNotifications(false)}
            />
            <div
              className="absolute top-12 right-0 w-[calc(100vw-2rem)] max-w-80 overflow-hidden z-50"
              style={{
                background: '#0E1225',
                border: '1px solid rgba(87,176,173,0.15)',
                borderRadius: '16px',
                boxShadow: '0 0 40px rgba(87,176,173,0.08)',
              }}
            >
              <div className="p-4" style={{ borderBottom: '1px solid rgba(87,176,173,0.08)' }}>
                <h3 className="font-semibold text-white text-sm">Notifications</h3>
              </div>
              <div className="p-4 text-center text-slate-500 text-sm">
                All caught up! No new notifications.
              </div>
            </div>
          </>
        )}
      </div>
    </header>
  )
}
