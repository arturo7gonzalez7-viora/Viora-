import type { Metadata } from 'next'
import './globals.css'
import { ClientWrapper } from './ClientWrapper'

export const metadata: Metadata = {
  title: 'Table AI',
  description: 'Restaurant management so easy, your abuela could run it.',
  icons: {
    icon: [
      { url: '/favicon-32.png', sizes: '16x16', type: 'image/png' },
      { url: '/favicon-32.png', sizes: '32x32', type: 'image/png' },
    ],
    apple: '/apple-touch-icon.png',
  },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
        <meta name="mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-title" content="Table AI" />
        <meta name="theme-color" content="#050810" />
        <link rel="manifest" href="/manifest.json" />
      </head>
      <body className="min-h-screen overflow-x-hidden" style={{ background: '#050810' }}>
        <ClientWrapper>
          {children}
        </ClientWrapper>
      </body>
    </html>
  )
}
