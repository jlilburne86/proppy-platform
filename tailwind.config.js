/** Tailwind build config for GitHub Pages */
module.exports = {
  darkMode: 'class',
  content: [
    './**/*.html',
    './assets/**/*.js'
  ],
  theme: {
    extend: {
      colors: {
        primary: '#000000',
        accent: '#6366f1',
        'background-light': '#fcfcfd',
        'background-dark': '#0a0a0a',
        'card-light': '#ffffff',
        'card-dark': '#161616'
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans','sans-serif'],
        display: ['Plus Jakarta Sans','sans-serif']
      },
      borderRadius: { DEFAULT: '1.5rem', '2xl': '2.5rem', '3xl':'3rem' },
      keyframes: {
        fadeIn: { '0%':{opacity:0, transform:'translateY(4px)'}, '100%':{opacity:1, transform:'translateY(0)'} },
        slideUp: { '0%':{opacity:0, transform:'translateY(8px)'}, '100%':{opacity:1, transform:'translateY(0)'} },
        pulseSoft: { '0%,100%':{opacity:0.4, transform:'scale(1)'}, '50%':{opacity:1, transform:'scale(1.05)'} }
      },
      animation: {
        fadeIn: 'fadeIn .35s ease-out both',
        slideUp: 'slideUp .45s ease-out both',
        pulseSoft: 'pulseSoft 2s ease-in-out infinite'
      }
    }
  },
  plugins: [require('@tailwindcss/forms'), require('@tailwindcss/typography')]
}

