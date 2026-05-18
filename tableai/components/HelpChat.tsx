'use client'

import { useState, useRef, useEffect } from 'react'
import { MessageCircle, X, Send } from 'lucide-react'

interface Message {
  role: 'assistant' | 'user'
  content: string
}

const WELCOME_MESSAGE =
  "Hi! I'm your Table AI assistant. I can help you with anything in the dashboard \u2014 from adding reservations to understanding your reports. What do you need help with?"

const QUICK_REPLIES = [
  'How do I add a reservation?',
  'How does loyalty work?',
  'Where can I see my sales?',
  'How do I add a new restaurant?',
]

export default function HelpChat() {
  const [open, setOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [showQuickReplies, setShowQuickReplies] = useState(true)
  const scrollRef = useRef<HTMLDivElement>(null)

  // Initialize with welcome message when opened
  useEffect(() => {
    if (open && messages.length === 0) {
      setMessages([{ role: 'assistant', content: WELCOME_MESSAGE }])
      setShowQuickReplies(true)
    }
  }, [open, messages.length])

  // Auto-scroll to bottom
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages, loading])

  const sendMessage = async (text: string) => {
    if (!text.trim() || loading) return

    setShowQuickReplies(false)
    const userMsg: Message = { role: 'user', content: text.trim() }
    const updated = [...messages, userMsg].slice(-10)
    setMessages(updated)
    setInput('')
    setLoading(true)

    try {
      const res = await fetch('/api/help', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text.trim(),
          history: updated.slice(0, -1), // exclude the current user message (API adds it)
        }),
      })
      const data = await res.json()
      setMessages((prev) => [...prev, { role: 'assistant' as const, content: data.reply }].slice(-10))
    } catch {
      setMessages((prev) =>
        [...prev, { role: 'assistant' as const, content: 'Sorry, something went wrong. Please try again.' }].slice(-10)
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      {/* Chat Window */}
      {open && (
        <div
          className="fixed z-50 flex flex-col
            inset-0 md:inset-auto
            md:bottom-24 md:right-6
            md:w-[400px] md:h-[500px] md:rounded-2xl
            overflow-hidden border border-white/10"
          style={{
            background: 'rgba(15, 20, 30, 0.95)',
            backdropFilter: 'blur(20px)',
          }}
        >
          {/* Header */}
          <div className="flex items-center gap-3 px-4 py-3 border-b border-white/10">
            <div className="w-8 h-8 rounded-full bg-[#00C9A7] flex items-center justify-center text-xs font-bold text-black shrink-0">
              AI
            </div>
            <span className="text-white font-semibold text-sm flex-1">Table AI Help</span>
            <button
              onClick={() => setOpen(false)}
              className="w-8 h-8 rounded-full flex items-center justify-center hover:bg-white/10 transition-colors"
            >
              <X size={18} className="text-gray-400" />
            </button>
          </div>

          {/* Messages */}
          <div ref={scrollRef} className="flex-1 overflow-y-auto px-4 py-4 space-y-3">
            {messages.map((msg, i) => (
              <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                {msg.role === 'assistant' && (
                  <div className="w-6 h-6 rounded-full bg-[#00C9A7] flex items-center justify-center text-[10px] font-bold text-black shrink-0 mt-1 mr-2">
                    AI
                  </div>
                )}
                <div
                  className={`max-w-[80%] px-3 py-2 rounded-xl text-sm leading-relaxed ${
                    msg.role === 'user'
                      ? 'bg-[#00C9A7] text-black'
                      : 'bg-white/5 border border-white/10 text-gray-200'
                  }`}
                >
                  {msg.content}
                </div>
              </div>
            ))}

            {/* Quick replies */}
            {showQuickReplies && messages.length === 1 && !loading && (
              <div className="flex flex-wrap gap-2 pt-1">
                {QUICK_REPLIES.map((q) => (
                  <button
                    key={q}
                    onClick={() => sendMessage(q)}
                    className="text-xs px-3 py-1.5 rounded-full border border-[#00C9A7]/40 text-[#00C9A7] hover:bg-[#00C9A7]/10 transition-colors"
                  >
                    {q}
                  </button>
                ))}
              </div>
            )}

            {/* Loading dots */}
            {loading && (
              <div className="flex justify-start">
                <div className="w-6 h-6 rounded-full bg-[#00C9A7] flex items-center justify-center text-[10px] font-bold text-black shrink-0 mt-1 mr-2">
                  AI
                </div>
                <div className="bg-white/5 border border-white/10 px-4 py-3 rounded-xl flex gap-1">
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            )}
          </div>

          {/* Input */}
          <div className="px-4 py-3 border-t border-white/10">
            <form
              onSubmit={(e) => {
                e.preventDefault()
                sendMessage(input)
              }}
              className="flex gap-2"
            >
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask a question..."
                className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-2 text-sm text-white placeholder-gray-500 outline-none focus:border-[#00C9A7]/50 transition-colors"
                disabled={loading}
              />
              <button
                type="submit"
                disabled={!input.trim() || loading}
                className="w-10 h-10 rounded-xl bg-[#00C9A7] flex items-center justify-center hover:bg-[#00C9A7]/80 transition-colors disabled:opacity-40 disabled:cursor-not-allowed shrink-0"
              >
                <Send size={16} className="text-black" />
              </button>
            </form>
          </div>
        </div>
      )}

      {/* Floating Button */}
      <button
        onClick={() => setOpen((v) => !v)}
        className="fixed z-50 w-14 h-14 rounded-full bg-[#00C9A7] flex items-center justify-center transition-transform hover:scale-110
          bottom-28 right-4 md:bottom-6 md:right-6"
        style={{
          boxShadow: '0 0 20px rgba(0,201,167,0.4)',
        }}
      >
        {open ? (
          <X size={24} className="text-black" />
        ) : (
          <>
            <MessageCircle size={24} className="text-black" />
            <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full flex items-center justify-center text-[10px] font-bold text-white">
              ?
            </span>
          </>
        )}
      </button>
    </>
  )
}
