'use client'

import { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'
import { useRestaurantId } from '@/lib/useRestaurantId'
import { LoadingSkeleton, EmptyState } from '@/components/LoadingState'

interface ChecklistTemplate {
  id: string
  restaurant_id: string
  name: string
  category: string
  items: string[]
  frequency: string
  created_at: string
}

interface ChecklistCompletion {
  id: string
  template_id: string
  completed_by: string
  completed_at: string
  notes: string | null
}

export default function CompliancePage() {
  const restaurantId = useRestaurantId()
  const [templates, setTemplates] = useState<ChecklistTemplate[]>([])
  const [completions, setCompletions] = useState<ChecklistCompletion[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      const [tRes, cRes] = await Promise.all([
        supabase.from('checklist_templates').select('*').eq('restaurant_id', restaurantId),
        supabase.from('checklist_completions').select('*').order('completed_at', { ascending: false }).limit(20),
      ])
      setTemplates(tRes.data || [])
      setCompletions(cRes.data || [])
      setLoading(false)
    }
    load()
  }, [restaurantId])

  if (loading) return <div className="space-y-6"><h1 className="text-xl md:text-3xl font-black tracking-tight text-white">Compliance</h1><LoadingSkeleton /></div>

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-xl md:text-3xl font-black tracking-tight text-white">Compliance</h1>
      </div>

      {/* Checklist Overview */}
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 md:gap-4">
        <div className="stat-card">
          <p className="text-white/40 text-sm">Checklists</p>
          <p className="text-3xl font-bold mt-1">{templates.length}</p>
        </div>
        <div className="stat-card">
          <p className="text-white/40 text-sm">Completions This Week</p>
          <p className="text-3xl font-bold mt-1">{completions.length}</p>
        </div>
        <div className="stat-card">
          <p className="text-white/40 text-sm">Status</p>
          <p className="text-3xl font-bold mt-1 text-emerald-400">✓</p>
        </div>
      </div>

      {templates.length === 0 ? (
        <EmptyState icon="✅" title="No checklists yet" description="Set up daily opening/closing checklists, health inspections, and more." />
      ) : (
        <div className="space-y-4">
          {templates.map((template) => (
            <div key={template.id} className="card p-4 md:p-6">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="font-semibold text-white">{template.name}</h3>
                  <p className="text-sm text-white/40">{template.category} · {template.frequency}</p>
                </div>
                <span className="badge bg-white/5 text-white/40">
                  {(template.items || []).length} items
                </span>
              </div>
              {template.items && (
                <div className="space-y-2">
                  {template.items.slice(0, 5).map((item, i) => (
                    <div key={i} className="flex items-center gap-3 text-sm min-h-[44px]">
                      <div className="w-6 h-6 md:w-5 md:h-5 rounded border border-white/20 flex items-center justify-center flex-shrink-0">
                        <span className="text-xs text-white/20">○</span>
                      </div>
                      <span className="text-white/60">{item}</span>
                    </div>
                  ))}
                  {template.items.length > 5 && (
                    <p className="text-xs text-white/30 pl-8">+{template.items.length - 5} more items</p>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
