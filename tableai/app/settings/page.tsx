'use client'

import { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'
import { useRestaurantId } from '@/lib/useRestaurantId'
import { Restaurant } from '@/lib/types'
import { LoadingSkeleton } from '@/components/LoadingState'
import { useLanguage } from '@/lib/LanguageContext'
import type { Language } from '@/lib/i18n'

export default function SettingsPage() {
  const { language, changeLanguage, t } = useLanguage()
  const restaurantId = useRestaurantId()
  const [restaurant, setRestaurant] = useState<Restaurant | null>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [saved, setSaved] = useState(false)
  const [form, setForm] = useState({
    name: '',
    phone: '',
    address: '',
    city: '',
    state: '',
    zip: '',
    timezone: 'America/Denver',
  })

  useEffect(() => {
    async function load() {
      const { data } = await supabase
        .from('restaurants')
        .select('*')
        .eq('id', restaurantId)
        .single()

      if (data) {
        setRestaurant(data)
        setForm({
          name: data.name || '',
          phone: data.phone || '',
          address: data.address || '',
          city: data.city || '',
          state: data.state || '',
          zip: data.zip || '',
          timezone: data.timezone || 'America/Denver',
        })
      }
      setLoading(false)
    }
    load()
  }, [restaurantId])

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setSaving(true)
    setSaved(false)
    const { error } = await supabase
      .from('restaurants')
      .update(form)
      .eq('id', restaurantId)

    if (!error) {
      setSaved(true)
      setTimeout(() => setSaved(false), 3000)
    }
    setSaving(false)
  }

  const languageOptions: { code: Language; flag: string; name: string }[] = [
    { code: 'en', flag: '🇺🇸', name: 'English' },
    { code: 'es', flag: '🇲🇽', name: 'Español' },
    { code: 'zh', flag: '🇨🇳', name: '中文' },
  ]

  if (loading) return <div className="space-y-6"><h1 className="text-xl md:text-3xl font-black tracking-tight text-white">{t('settings.title')}</h1><LoadingSkeleton rows={3} /></div>

  return (
    <div className="space-y-6 max-w-2xl">
      <h1 className="text-xl md:text-3xl font-black tracking-tight text-white">{t('settings.title')}</h1>

      {/* Language Selector */}
      <div className="card p-4 md:p-6">
        <h2 className="text-base md:text-lg font-semibold mb-1">{t('settings.language')}</h2>
        <p className="text-sm text-white/40 mb-4">{t('settings.language.subtitle')}</p>
        <div className="flex flex-col md:flex-row gap-2 md:gap-3">
          {languageOptions.map((opt) => (
            <button
              key={opt.code}
              onClick={() => changeLanguage(opt.code)}
              className={`flex items-center justify-center md:justify-start gap-2 px-5 py-3 rounded-xl border text-sm font-medium transition-all w-full md:w-auto ${
                language === opt.code
                  ? 'border-[#00C9A7] bg-[#00C9A7]/10 text-[#00C9A7]'
                  : 'border-white/10 text-white/50 hover:border-white/30 hover:text-white'
              }`}
            >
              <span className="text-lg">{opt.flag}</span>
              {opt.name}
            </button>
          ))}
        </div>
      </div>

      <div className="card p-4 md:p-6">
        <h2 className="text-base md:text-lg font-semibold mb-4 md:mb-6">{t('settings.restaurant')}</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm text-white/60 mb-1">{t('settings.name')}</label>
            <input
              type="text"
              value={form.name}
              onChange={e => setForm({ ...form, name: e.target.value })}
              className="input-field"
            />
          </div>
          <div>
            <label className="block text-sm text-white/60 mb-1">{t('settings.phone')}</label>
            <input
              type="tel"
              value={form.phone}
              onChange={e => setForm({ ...form, phone: e.target.value })}
              className="input-field"
            />
          </div>
          <div>
            <label className="block text-sm text-white/60 mb-1">{t('settings.address')}</label>
            <input
              type="text"
              value={form.address}
              onChange={e => setForm({ ...form, address: e.target.value })}
              className="input-field"
            />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3 md:gap-4">
            <div>
              <label className="block text-xs md:text-sm text-white/60 mb-1">{t('settings.city')}</label>
              <input
                type="text"
                value={form.city}
                onChange={e => setForm({ ...form, city: e.target.value })}
                className="input-field"
              />
            </div>
            <div>
              <label className="block text-sm text-white/60 mb-1">{t('settings.state')}</label>
              <input
                type="text"
                value={form.state}
                onChange={e => setForm({ ...form, state: e.target.value })}
                className="input-field"
              />
            </div>
            <div>
              <label className="block text-sm text-white/60 mb-1">{t('settings.zip')}</label>
              <input
                type="text"
                value={form.zip}
                onChange={e => setForm({ ...form, zip: e.target.value })}
                className="input-field"
              />
            </div>
          </div>
          <div>
            <label className="block text-sm text-white/60 mb-1">{t('settings.timezone')}</label>
            <select
              value={form.timezone}
              onChange={e => setForm({ ...form, timezone: e.target.value })}
              className="input-field"
            >
              <option value="America/New_York">Eastern</option>
              <option value="America/Chicago">Central</option>
              <option value="America/Denver">Mountain</option>
              <option value="America/Los_Angeles">Pacific</option>
            </select>
          </div>
          <div className="pt-4 flex flex-col md:flex-row items-stretch md:items-center gap-3 md:gap-4">
            <button type="submit" disabled={saving} className="btn-primary w-full md:w-auto">
              {saving ? t('settings.saving') : t('settings.save')}
            </button>
            {saved && (
              <span className="text-emerald-400 text-sm flex items-center gap-1">
                ✓ {t('settings.saved')}
              </span>
            )}
          </div>
        </form>
      </div>

      {/* Danger Zone */}
      <div className="card border-red-500/20 p-4 md:p-6">
        <h2 className="text-lg font-semibold text-red-400 mb-2">{t('settings.danger')}</h2>
        <p className="text-sm text-white/40 mb-4">{t('settings.danger.subtitle')}</p>
        <button className="px-4 py-2 rounded-xl border border-red-500/30 text-red-400 text-sm hover:bg-red-500/10 transition-colors">
          {t('settings.delete')}
        </button>
      </div>
    </div>
  )
}
