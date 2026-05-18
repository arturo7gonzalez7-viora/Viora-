'use client'

import { usePathname } from 'next/navigation'
import { LanguageProvider } from '@/lib/LanguageContext'
import Sidebar from '@/components/Sidebar'
import TopBar from '@/components/TopBar'
import HelpChat from '@/components/HelpChat'

export function ClientWrapper({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  const isPublicPage = pathname.startsWith('/feedback')

  if (isPublicPage) {
    return <>{children}</>
  }

  return (
    <LanguageProvider>
      <Sidebar />
      <div className="md:ml-64 min-h-screen flex flex-col relative">
        {/* Radial gradient glow — top right */}
        <div
          className="pointer-events-none fixed top-0 right-0 w-[600px] h-[600px] opacity-30"
          style={{
            background: 'radial-gradient(circle at top right, rgba(0,201,167,0.08), transparent 60%)',
          }}
        />
        {/* Dot grid overlay */}
        <div className="pointer-events-none fixed inset-0 dot-grid opacity-100" />

        <TopBar restaurantName="Casa Mariachi" />
        <main
          className="flex-1 px-4 pt-4 pb-24 md:px-8 md:py-8 md:pb-8 relative z-10 md:mt-16"
          style={{ marginTop: 'calc(56px + env(safe-area-inset-top, 0px) + 4px)' }}
        >
          {children}
        </main>
      </div>
      <HelpChat />
    </LanguageProvider>
  )
}
