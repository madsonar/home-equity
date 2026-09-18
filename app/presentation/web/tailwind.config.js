/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eef8ff',
          100: '#d9efff',
          500: '#0a84ff',
          600: '#0069d6',
          700: '#0054ad',
          900: '#002b5c',
        },
      },
    },
  },
  plugins: [],
};
