/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        navy: '#0B1F33',
        steel: '#1F4E79',
        electric: '#F5B400',
        mist: '#F4F6F8',
        carbon: '#111827',
      },
      fontFamily: {
        sans: ['Inter', 'Manrope', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        industrial: '0 18px 60px rgba(11, 31, 51, 0.14)',
      },
    },
  },
  plugins: [],
}
