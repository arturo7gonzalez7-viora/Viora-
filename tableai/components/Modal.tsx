'use client'

import { useEffect } from 'react'
import { X, ChevronLeft } from 'lucide-react'

interface ModalProps {
  isOpen: boolean
  onClose: () => void
  title: string
  children: React.ReactNode
}

export default function Modal({ isOpen, onClose, title, children }: ModalProps) {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = ''
    }
    return () => { document.body.style.overflow = '' }
  }, [isOpen])

  if (!isOpen) return null

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div
          className="flex items-center justify-between p-4 md:p-6 sticky top-0 z-10"
          style={{
            borderBottom: '1px solid rgba(87,176,173,0.1)',
            background: '#0E1225',
          }}
        >
          {/* Mobile: back arrow, Desktop: title */}
          <button
            onClick={onClose}
            className="md:hidden p-1 -ml-1 rounded-lg hover:bg-white/[0.05] text-slate-400 hover:text-white transition-all"
            aria-label="Close"
          >
            <ChevronLeft size={22} />
          </button>
          <h2 className="text-base md:text-lg font-bold text-white md:flex-none flex-1 text-center md:text-left">
            {title}
          </h2>
          <button
            onClick={onClose}
            className="p-2 rounded-xl hover:bg-white/[0.05] text-slate-500 hover:text-white transition-all duration-200"
          >
            <X size={18} className="hidden md:block" />
            {/* Spacer on mobile for centering */}
            <span className="md:hidden w-5 block" />
          </button>
        </div>
        <div className="p-4 md:p-6">
          {children}
        </div>
      </div>
    </div>
  )
}
