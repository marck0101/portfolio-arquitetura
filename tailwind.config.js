/** @type {import('tailwindcss').Config} */
// Mesma configuração que antes ficava inline com o CDN do Tailwind.
// Depois de mudar classes no HTML, rode: npm run build:css
module.exports = {
  content: ['./*.html', './assets/js/**/*.js'],
  theme: {
    extend: {
      colors: {
        brand: { DEFAULT: '#D4A373', 50: '#FBF6EE', 100: '#F7EEDD', 200: '#EAD7BB', 300: '#DCC1A0', 400: '#D4A373', 500: '#B88556' }
      },
      fontFamily: {
        display: ['Sora', 'sans-serif'],
        sans: ['Inter', 'system-ui', 'Avenir', 'Helvetica', 'Arial', 'sans-serif']
      },
      boxShadow: { soft: '0 10px 40px rgba(0,0,0,.06)' }
    }
  }
}
