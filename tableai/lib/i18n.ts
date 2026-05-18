'use client'

export type Language = 'en' | 'es' | 'zh'

export const translations: Record<Language, Record<string, string>> = {
  en: {
    // Nav
    'nav.dashboard': 'Dashboard',
    'nav.reservations': 'Reservations',
    'nav.calls': 'Calls',
    'nav.reviews': 'Reviews',
    'nav.loyalty': 'Loyalty',
    'nav.inventory': 'Inventory',
    'nav.compliance': 'Compliance',
    'nav.finance': 'Finance',
    'nav.marketing': 'Marketing',
    'nav.settings': 'Settings',
    // Dashboard
    'dashboard.greeting.morning': 'Good morning,',
    'dashboard.greeting.afternoon': 'Good afternoon,',
    'dashboard.greeting.evening': 'Good evening,',
    'dashboard.subtitle': "Here's what's happening today",
    'dashboard.stat.reservations': "Today's Reservations",
    'dashboard.stat.calls': 'Calls Answered',
    'dashboard.stat.reviews': 'New Reviews',
    'dashboard.stat.loyalty': 'Loyalty Members',
    'dashboard.quickactions': 'Quick Actions',
    'dashboard.action.reservation': 'Add Reservation',
    'dashboard.action.sale': 'Log Sale',
    'dashboard.action.calls': 'View Calls',
    'dashboard.activity': 'Recent Activity',
    // Settings
    'settings.title': 'Settings',
    'settings.restaurant': 'Restaurant Info',
    'settings.language': 'Language',
    'settings.language.subtitle': 'Choose your preferred language for the entire platform',
    'settings.save': 'Save Changes',
    'settings.saving': 'Saving...',
    'settings.saved': 'Saved successfully',
    'settings.name': 'Restaurant Name',
    'settings.phone': 'Phone',
    'settings.address': 'Address',
    'settings.city': 'City',
    'settings.state': 'State',
    'settings.zip': 'ZIP',
    'settings.timezone': 'Timezone',
    'settings.danger': 'Danger Zone',
    'settings.danger.subtitle': 'These actions cannot be undone.',
    'settings.delete': 'Delete Restaurant',
    // Common
    'common.owner': 'Owner',
    'common.today': 'Today',
    'common.loading': 'Loading...',
    'common.empty': 'No data yet',
  },
  es: {
    // Nav
    'nav.dashboard': 'Panel',
    'nav.reservations': 'Reservaciones',
    'nav.calls': 'Llamadas',
    'nav.reviews': 'Reseñas',
    'nav.loyalty': 'Lealtad',
    'nav.inventory': 'Inventario',
    'nav.compliance': 'Cumplimiento',
    'nav.finance': 'Finanzas',
    'nav.marketing': 'Marketing',
    'nav.settings': 'Configuración',
    // Dashboard
    'dashboard.greeting.morning': 'Buenos días,',
    'dashboard.greeting.afternoon': 'Buenas tardes,',
    'dashboard.greeting.evening': 'Buenas noches,',
    'dashboard.subtitle': 'Esto es lo que está pasando hoy',
    'dashboard.stat.reservations': 'Reservaciones de Hoy',
    'dashboard.stat.calls': 'Llamadas Atendidas',
    'dashboard.stat.reviews': 'Reseñas Nuevas',
    'dashboard.stat.loyalty': 'Miembros de Lealtad',
    'dashboard.quickactions': 'Acciones Rápidas',
    'dashboard.action.reservation': 'Agregar Reservación',
    'dashboard.action.sale': 'Registrar Venta',
    'dashboard.action.calls': 'Ver Llamadas',
    'dashboard.activity': 'Actividad Reciente',
    // Settings
    'settings.title': 'Configuración',
    'settings.restaurant': 'Información del Restaurante',
    'settings.language': 'Idioma',
    'settings.language.subtitle': 'Elige tu idioma preferido para toda la plataforma',
    'settings.save': 'Guardar Cambios',
    'settings.saving': 'Guardando...',
    'settings.saved': 'Guardado correctamente',
    'settings.name': 'Nombre del Restaurante',
    'settings.phone': 'Teléfono',
    'settings.address': 'Dirección',
    'settings.city': 'Ciudad',
    'settings.state': 'Estado',
    'settings.zip': 'Código Postal',
    'settings.timezone': 'Zona Horaria',
    'settings.danger': 'Zona de Peligro',
    'settings.danger.subtitle': 'Estas acciones no se pueden deshacer.',
    'settings.delete': 'Eliminar Restaurante',
    // Common
    'common.owner': 'Dueño',
    'common.today': 'Hoy',
    'common.loading': 'Cargando...',
    'common.empty': 'Sin datos aún',
  },
  zh: {
    // Nav
    'nav.dashboard': '控制台',
    'nav.reservations': '预订',
    'nav.calls': '电话',
    'nav.reviews': '评价',
    'nav.loyalty': '会员',
    'nav.inventory': '库存',
    'nav.compliance': '合规',
    'nav.finance': '财务',
    'nav.marketing': '营销',
    'nav.settings': '设置',
    // Dashboard
    'dashboard.greeting.morning': '早上好，',
    'dashboard.greeting.afternoon': '下午好，',
    'dashboard.greeting.evening': '晚上好，',
    'dashboard.subtitle': '今天的业务概况',
    'dashboard.stat.reservations': '今日预订',
    'dashboard.stat.calls': '接听电话',
    'dashboard.stat.reviews': '新评价',
    'dashboard.stat.loyalty': '会员数量',
    'dashboard.quickactions': '快捷操作',
    'dashboard.action.reservation': '添加预订',
    'dashboard.action.sale': '记录销售',
    'dashboard.action.calls': '查看电话',
    'dashboard.activity': '最近动态',
    // Settings
    'settings.title': '设置',
    'settings.restaurant': '餐厅信息',
    'settings.language': '语言',
    'settings.language.subtitle': '选择整个平台的首选语言',
    'settings.save': '保存更改',
    'settings.saving': '保存中...',
    'settings.saved': '保存成功',
    'settings.name': '餐厅名称',
    'settings.phone': '电话',
    'settings.address': '地址',
    'settings.city': '城市',
    'settings.state': '州',
    'settings.zip': '邮编',
    'settings.timezone': '时区',
    'settings.danger': '危险区域',
    'settings.danger.subtitle': '这些操作无法撤销。',
    'settings.delete': '删除餐厅',
    // Common
    'common.owner': '店主',
    'common.today': '今天',
    'common.loading': '加载中...',
    'common.empty': '暂无数据',
  },
}

export function getLanguage(): Language {
  if (typeof window === 'undefined') return 'en'
  return (localStorage.getItem('tableai_language') as Language) || 'en'
}

export function setLanguage(lang: Language) {
  if (typeof window === 'undefined') return
  localStorage.setItem('tableai_language', lang)
  window.location.reload()
}

export function t(key: string): string {
  const lang = getLanguage()
  return translations[lang][key] || translations['en'][key] || key
}
