'use client'

import { useEffect, useState, useRef, useMemo } from 'react'
import { supabase } from '@/lib/supabase'
import { useRestaurantId } from '@/lib/useRestaurantId'
import { DailySale, Expense } from '@/lib/types'
import { formatCurrency, formatDate } from '@/lib/utils'
import { LoadingSkeleton, EmptyState, ErrorState } from '@/components/LoadingState'
import Modal from '@/components/Modal'
import { Camera, ChevronDown, ChevronRight, Sparkles, Loader2 } from 'lucide-react'

const CATEGORY_CONFIG: Record<string, { emoji: string; label: string; color: string }> = {
  food_cost: { emoji: '🥩', label: 'Food Cost', color: '#ef4444' },
  alcohol:   { emoji: '🍺', label: 'Alcohol', color: '#f59e0b' },
  labor:     { emoji: '👥', label: 'Labor', color: '#3b82f6' },
  rent:      { emoji: '🏠', label: 'Rent', color: '#8b5cf6' },
  utilities: { emoji: '⚡', label: 'Utilities', color: '#06b6d4' },
  marketing: { emoji: '📣', label: 'Marketing', color: '#ec4899' },
  supplies:  { emoji: '🧹', label: 'Supplies', color: '#10b981' },
  other:     { emoji: '📦', label: 'Other', color: '#6b7280' },
}

// Map old category names to new ones
function normalizeCategory(cat: string): string {
  const map: Record<string, string> = {
    food: 'food_cost',
    beverage: 'alcohol',
    equipment: 'supplies',
  }
  return map[cat] || cat
}

const CATEGORY_ORDER = ['food_cost', 'alcohol', 'labor', 'rent', 'utilities', 'marketing', 'supplies', 'other']

interface GroupedExpenses {
  [category: string]: {
    total: number
    vendors: {
      [vendor: string]: {
        total: number
        expenses: Expense[]
      }
    }
  }
}

export default function FinancePage() {
  const restaurantId = useRestaurantId()
  const [sales, setSales] = useState<DailySale[]>([])
  const [expenses, setExpenses] = useState<Expense[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showSaleModal, setShowSaleModal] = useState(false)
  const [showExpenseModal, setShowExpenseModal] = useState(false)
  const [saving, setSaving] = useState(false)
  const [activeTab, setActiveTab] = useState<'sales' | 'expenses'>('sales')
  const [scanning, setScanning] = useState(false)
  const [aiExtracted, setAiExtracted] = useState(false)
  const [collapsedCategories, setCollapsedCategories] = useState<Set<string>>(new Set())
  const fileInputRef = useRef<HTMLInputElement>(null)

  const [saleForm, setSaleForm] = useState({
    date: new Date().toISOString().split('T')[0],
    total_revenue: '',
    cash: '',
    card: '',
    online: '',
    covers: '',
    notes: '',
  })

  const [expenseForm, setExpenseForm] = useState({
    date: new Date().toISOString().split('T')[0],
    category: 'food_cost',
    description: '',
    amount: '',
    vendor: '',
  })

  async function loadData() {
    setLoading(true)
    setError(null)
    const [salesRes, expRes] = await Promise.all([
      supabase.from('daily_sales').select('*').eq('restaurant_id', restaurantId).order('date', { ascending: false }).limit(30),
      supabase.from('expenses').select('*').eq('restaurant_id', restaurantId).order('date', { ascending: false }).limit(50),
    ])

    if (salesRes.error) setError(salesRes.error.message)
    else setSales(salesRes.data || [])
    setExpenses(expRes.data || [])
    setLoading(false)
  }

  useEffect(() => { loadData() }, [restaurantId])

  const weekRevenue = sales.slice(0, 7).reduce((sum, s) => sum + (s.total_revenue || 0), 0)
  const weekExpenses = expenses.slice(0, 7).reduce((sum, e) => sum + (e.amount || 0), 0)

  // Group expenses by category then vendor
  const grouped = useMemo<GroupedExpenses>(() => {
    const result: GroupedExpenses = {}
    for (const cat of CATEGORY_ORDER) {
      result[cat] = { total: 0, vendors: {} }
    }
    for (const exp of expenses) {
      const cat = normalizeCategory(exp.category)
      if (!result[cat]) {
        result[cat] = { total: 0, vendors: {} }
      }
      result[cat].total += exp.amount || 0
      const vendor = exp.vendor || 'Uncategorized'
      if (!result[cat].vendors[vendor]) {
        result[cat].vendors[vendor] = { total: 0, expenses: [] }
      }
      result[cat].vendors[vendor].total += exp.amount || 0
      result[cat].vendors[vendor].expenses.push(exp)
    }
    return result
  }, [expenses])

  const totalExpenses = useMemo(() => {
    return Object.values(grouped).reduce((sum, g) => sum + g.total, 0)
  }, [grouped])

  function toggleCategory(cat: string) {
    setCollapsedCategories(prev => {
      const next = new Set(prev)
      if (next.has(cat)) next.delete(cat)
      else next.add(cat)
      return next
    })
  }

  async function handleScanReceipt(file: File) {
    setScanning(true)
    try {
      const formData = new FormData()
      formData.append('image', file)

      const res = await fetch('/api/scan-receipt', {
        method: 'POST',
        body: formData,
      })

      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.error || 'Failed to scan receipt')
      }

      const data = await res.json()

      setExpenseForm({
        date: data.date || new Date().toISOString().split('T')[0],
        category: data.category || 'other',
        description: data.description || '',
        amount: data.amount?.toString() || '',
        vendor: data.vendor || '',
      })
      setAiExtracted(true)
      setShowExpenseModal(true)
    } catch (err) {
      console.error('Scan failed:', err)
      alert('Could not read receipt. Try a clearer photo or add the expense manually.')
    } finally {
      setScanning(false)
      if (fileInputRef.current) fileInputRef.current.value = ''
    }
  }

  async function handleSaleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setSaving(true)
    await supabase.from('daily_sales').insert({
      restaurant_id: restaurantId,
      date: saleForm.date,
      total_revenue: parseFloat(saleForm.total_revenue) || 0,
      cash: parseFloat(saleForm.cash) || 0,
      card: parseFloat(saleForm.card) || 0,
      online: parseFloat(saleForm.online) || 0,
      covers: parseInt(saleForm.covers) || 0,
      notes: saleForm.notes || null,
    })
    setSaving(false)
    setShowSaleModal(false)
    setSaleForm({ date: new Date().toISOString().split('T')[0], total_revenue: '', cash: '', card: '', online: '', covers: '', notes: '' })
    loadData()
  }

  async function handleExpenseSubmit(e: React.FormEvent) {
    e.preventDefault()
    setSaving(true)
    await supabase.from('expenses').insert({
      restaurant_id: restaurantId,
      date: expenseForm.date,
      category: expenseForm.category,
      description: expenseForm.description,
      amount: parseFloat(expenseForm.amount) || 0,
      vendor: expenseForm.vendor || null,
    })
    setSaving(false)
    setShowExpenseModal(false)
    setExpenseForm({ date: new Date().toISOString().split('T')[0], category: 'food_cost', description: '', amount: '', vendor: '' })
    setAiExtracted(false)
    loadData()
  }

  function AiBadge() {
    return (
      <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-medium bg-teal/20 text-teal ml-2">
        <Sparkles className="w-3 h-3" /> AI extracted
      </span>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
        <h1 className="text-xl md:text-3xl font-black tracking-tight text-white">Finance</h1>
        <div className="flex flex-col sm:flex-row gap-2">
          <div className="flex gap-2">
            <button onClick={() => setShowSaleModal(true)} className="btn-primary text-sm flex-1 md:flex-none">
              💵 Log Sale
            </button>
            <button onClick={() => { setAiExtracted(false); setExpenseForm({ date: new Date().toISOString().split('T')[0], category: 'food_cost', description: '', amount: '', vendor: '' }); setShowExpenseModal(true) }} className="btn-secondary text-sm flex-1 md:flex-none">
              ➕ Add Expense
            </button>
          </div>
          <button
            onClick={() => fileInputRef.current?.click()}
            disabled={scanning}
            className="flex items-center justify-center gap-2 px-4 py-2 rounded-xl text-sm font-medium border border-teal text-teal hover:bg-teal/10 transition-colors disabled:opacity-50"
          >
            {scanning ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Reading receipt...
              </>
            ) : (
              <>
                <Camera className="w-4 h-4" />
                Scan Receipt
              </>
            )}
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            capture="environment"
            className="hidden"
            onChange={(e) => {
              const file = e.target.files?.[0]
              if (file) handleScanReceipt(file)
            }}
          />
        </div>
      </div>

      {/* Summary */}
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 md:gap-4">
        <div className="stat-card !p-4 md:!p-6">
          <p className="text-white/40 text-xs md:text-sm">This Week Revenue</p>
          <p className="text-2xl md:text-3xl font-bold mt-1 text-emerald-400">{formatCurrency(weekRevenue)}</p>
        </div>
        <div className="stat-card !p-4 md:!p-6">
          <p className="text-white/40 text-xs md:text-sm">This Week Expenses</p>
          <p className="text-2xl md:text-3xl font-bold mt-1 text-red-400">{formatCurrency(weekExpenses)}</p>
        </div>
        <div className="stat-card !p-4 md:!p-6 col-span-2 sm:col-span-1">
          <p className="text-white/40 text-xs md:text-sm">Net</p>
          <p className={`text-3xl font-bold mt-1 ${weekRevenue - weekExpenses >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
            {formatCurrency(weekRevenue - weekExpenses)}
          </p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 bg-navy-50 rounded-xl p-1 w-full md:w-fit">
        <button
          onClick={() => setActiveTab('sales')}
          className={`flex-1 md:flex-none px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeTab === 'sales' ? 'bg-teal text-navy' : 'text-white/40 hover:text-white'}`}
        >
          Daily Sales
        </button>
        <button
          onClick={() => setActiveTab('expenses')}
          className={`flex-1 md:flex-none px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeTab === 'expenses' ? 'bg-teal text-navy' : 'text-white/40 hover:text-white'}`}
        >
          Expenses
        </button>
      </div>

      {loading ? (
        <LoadingSkeleton />
      ) : error ? (
        <ErrorState message={error} onRetry={loadData} />
      ) : activeTab === 'sales' ? (
        sales.length === 0 ? (
          <EmptyState icon="💰" title="No sales logged" description="Log your first daily sale to start tracking revenue." />
        ) : (
          <div className="card divide-y divide-white/5">
            {sales.map((sale) => (
              <div key={sale.id} className="table-row">
                <div className="flex-1">
                  <p className="font-medium text-white">{formatDate(sale.date)}</p>
                  <p className="text-sm text-white/40">
                    {sale.covers} covers · Cash {formatCurrency(sale.cash)} · Card {formatCurrency(sale.card)}
                  </p>
                </div>
                <p className="font-semibold text-emerald-400">{formatCurrency(sale.total_revenue)}</p>
              </div>
            ))}
          </div>
        )
      ) : (
        expenses.length === 0 ? (
          <EmptyState icon="🧾" title="No expenses logged" description="Track your expenses to see where money goes." />
        ) : (
          <div className="space-y-4">
            {/* Category summary bar */}
            <div className="flex flex-wrap gap-2 items-center">
              {CATEGORY_ORDER.map(cat => {
                const config = CATEGORY_CONFIG[cat]
                const catTotal = grouped[cat]?.total || 0
                if (catTotal === 0) return null
                return (
                  <span key={cat} className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-medium bg-white/5 text-white/70">
                    {config.emoji} {formatCurrency(catTotal)}
                  </span>
                )
              })}
              <span className="inline-flex items-center gap-1 px-3 py-1 rounded-lg text-xs font-bold bg-teal/20 text-teal">
                Total: {formatCurrency(totalExpenses)}
              </span>
            </div>

            {/* Category sections */}
            {CATEGORY_ORDER.map(cat => {
              const config = CATEGORY_CONFIG[cat]
              const group = grouped[cat]
              if (!group || group.total === 0) return null
              const isCollapsed = collapsedCategories.has(cat)
              const vendorEntries = Object.entries(group.vendors).sort((a, b) => b[1].total - a[1].total)

              return (
                <div
                  key={cat}
                  className="card !p-0 overflow-hidden"
                  style={{ borderLeft: `3px solid ${config.color}` }}
                >
                  {/* Category header */}
                  <button
                    onClick={() => toggleCategory(cat)}
                    className="w-full flex items-center justify-between px-4 py-3 hover:bg-white/5 transition-colors"
                  >
                    <div className="flex items-center gap-2">
                      {isCollapsed ? <ChevronRight className="w-4 h-4 text-white/40" /> : <ChevronDown className="w-4 h-4 text-white/40" />}
                      <span className="text-lg">{config.emoji}</span>
                      <span className="font-bold text-white">{config.label}</span>
                    </div>
                    <span className="font-semibold text-teal">{formatCurrency(group.total)}</span>
                  </button>

                  {/* Vendor groups */}
                  {!isCollapsed && (
                    <div className="divide-y divide-white/5">
                      {vendorEntries.map(([vendor, vData]) => (
                        <div key={vendor} className="px-4 py-2">
                          {/* Vendor subheader */}
                          <div className="flex items-center justify-between pl-6 pb-1">
                            <span className="text-sm text-white/50 font-medium">{vendor}</span>
                            <span className="text-sm text-white/50 font-medium">{formatCurrency(vData.total)}</span>
                          </div>
                          {/* Individual expenses */}
                          {vData.expenses.map(exp => (
                            <div key={exp.id} className="flex items-center justify-between pl-10 py-1.5">
                              <span className="text-xs text-white/30 w-20 shrink-0">{formatDate(exp.date)}</span>
                              <span className="text-sm text-white/70 flex-1 px-2 truncate">{exp.description}</span>
                              <span className="text-sm font-medium text-red-400 shrink-0">{formatCurrency(exp.amount)}</span>
                            </div>
                          ))}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        )
      )}

      {/* Log Sale Modal */}
      <Modal isOpen={showSaleModal} onClose={() => setShowSaleModal(false)} title="Log Daily Sales">
        <form onSubmit={handleSaleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm text-white/60 mb-1">Date</label>
            <input type="date" required value={saleForm.date} onChange={e => setSaleForm({...saleForm, date: e.target.value})} className="input-field" />
          </div>
          <div>
            <label className="block text-xs md:text-sm text-white/60 mb-1">Total Revenue</label>
            <input type="number" step="0.01" inputMode="decimal" required value={saleForm.total_revenue} onChange={e => setSaleForm({...saleForm, total_revenue: e.target.value})} className="input-field" placeholder="0.00" />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            <div>
              <label className="block text-xs md:text-sm text-white/60 mb-1">Cash</label>
              <input type="number" step="0.01" inputMode="decimal" value={saleForm.cash} onChange={e => setSaleForm({...saleForm, cash: e.target.value})} className="input-field" placeholder="0.00" />
            </div>
            <div>
              <label className="block text-xs md:text-sm text-white/60 mb-1">Card</label>
              <input type="number" step="0.01" inputMode="decimal" value={saleForm.card} onChange={e => setSaleForm({...saleForm, card: e.target.value})} className="input-field" placeholder="0.00" />
            </div>
            <div>
              <label className="block text-xs md:text-sm text-white/60 mb-1">Online</label>
              <input type="number" step="0.01" inputMode="decimal" value={saleForm.online} onChange={e => setSaleForm({...saleForm, online: e.target.value})} className="input-field" placeholder="0.00" />
            </div>
          </div>
          <div>
            <label className="block text-sm text-white/60 mb-1">Covers (guests served)</label>
            <input type="number" value={saleForm.covers} onChange={e => setSaleForm({...saleForm, covers: e.target.value})} className="input-field" placeholder="0" />
          </div>
          <div>
            <label className="block text-sm text-white/60 mb-1">Notes (optional)</label>
            <textarea value={saleForm.notes} onChange={e => setSaleForm({...saleForm, notes: e.target.value})} className="input-field" rows={2} placeholder="Private event, slow night..." />
          </div>
          <div className="flex flex-col-reverse md:flex-row gap-3 pt-2">
            <button type="button" onClick={() => setShowSaleModal(false)} className="btn-secondary flex-1 text-sm">Cancel</button>
            <button type="submit" disabled={saving} className="btn-primary flex-1 text-sm">{saving ? 'Saving...' : 'Log Sale'}</button>
          </div>
        </form>
      </Modal>

      {/* Add Expense Modal */}
      <Modal isOpen={showExpenseModal} onClose={() => { setShowExpenseModal(false); setAiExtracted(false) }} title={aiExtracted ? '🧾 Scanned Expense' : 'Add Expense'}>
        <form onSubmit={handleExpenseSubmit} className="space-y-4">
          <div>
            <label className="block text-sm text-white/60 mb-1">
              Date
              {aiExtracted && <AiBadge />}
            </label>
            <input type="date" required value={expenseForm.date} onChange={e => setExpenseForm({...expenseForm, date: e.target.value})} className="input-field" />
          </div>
          <div>
            <label className="block text-sm text-white/60 mb-1">
              Category
              {aiExtracted && <AiBadge />}
            </label>
            <select value={expenseForm.category} onChange={e => setExpenseForm({...expenseForm, category: e.target.value})} className="input-field">
              <option value="food_cost">🥩 Food Cost</option>
              <option value="alcohol">🍺 Alcohol</option>
              <option value="labor">👥 Labor</option>
              <option value="rent">🏠 Rent</option>
              <option value="utilities">⚡ Utilities</option>
              <option value="marketing">📣 Marketing</option>
              <option value="supplies">🧹 Supplies</option>
              <option value="other">📦 Other</option>
            </select>
          </div>
          <div>
            <label className="block text-sm text-white/60 mb-1">
              Description
              {aiExtracted && <AiBadge />}
            </label>
            <input type="text" required value={expenseForm.description} onChange={e => setExpenseForm({...expenseForm, description: e.target.value})} className="input-field" placeholder="What was it for?" />
          </div>
          <div>
            <label className="block text-xs md:text-sm text-white/60 mb-1">
              Amount
              {aiExtracted && <AiBadge />}
            </label>
            <input type="number" step="0.01" inputMode="decimal" required value={expenseForm.amount} onChange={e => setExpenseForm({...expenseForm, amount: e.target.value})} className="input-field" placeholder="0.00" />
          </div>
          <div>
            <label className="block text-sm text-white/60 mb-1">
              Vendor
              {aiExtracted && <AiBadge />}
            </label>
            <input type="text" value={expenseForm.vendor} onChange={e => setExpenseForm({...expenseForm, vendor: e.target.value})} className="input-field" placeholder="Sysco, US Foods..." />
          </div>
          <div className="flex flex-col-reverse md:flex-row gap-3 pt-2">
            <button type="button" onClick={() => { setShowExpenseModal(false); setAiExtracted(false) }} className="btn-secondary flex-1 text-sm">Cancel</button>
            <button type="submit" disabled={saving} className="btn-primary flex-1 text-sm">{saving ? 'Saving...' : 'Add Expense'}</button>
          </div>
        </form>
      </Modal>
    </div>
  )
}
