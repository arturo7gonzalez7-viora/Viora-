import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './lib/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          DEFAULT: '#050810',
          50: '#0E1225',
          100: '#080D1A',
          200: '#070B17',
          300: '#060914',
          400: '#050810',
          500: '#04060C',
          600: '#030508',
          700: '#020304',
          800: '#010102',
          900: '#000000',
        },
        teal: {
          DEFAULT: '#00C9A7',
          50: '#E6FFF9',
          100: '#B3FFE9',
          200: '#80FFD9',
          300: '#4DFFC9',
          400: '#1AFFB9',
          500: '#00C9A7',
          600: '#00A88C',
          700: '#008770',
          800: '#006655',
          900: '#004539',
        },
        surface: 'rgba(255,255,255,0.03)',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        '2xl': '16px',
      },
      boxShadow: {
        'glow': '0 0 40px rgba(0,201,167,0.05), inset 0 1px 0 rgba(255,255,255,0.05)',
        'glow-hover': '0 0 40px rgba(0,201,167,0.15), inset 0 1px 0 rgba(255,255,255,0.08)',
        'glow-btn': '0 0 20px rgba(0,201,167,0.3)',
      },
      keyframes: {
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        pulse_glow: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.5' },
        },
      },
      animation: {
        shimmer: 'shimmer 1.5s infinite',
        'pulse-glow': 'pulse_glow 2s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}
export default config
