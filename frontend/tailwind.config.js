/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',  // Enable dark mode using the 'dark' class
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      screens: {
        '4k': '3840px', // Custom breakpoint for 4K monitors
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: 0 },
          '20%': { opacity: 0 },
          '100%': { opacity: 1 },
        },
        fadeInNoDelay: {
          '0%': { opacity: 0 },
          '100%': { opacity: 1 },
        },
      },
      animation: {
        fadeIn: 'fadeIn 0.6s ease-out forwards', // Creates a 0.5s fade-in animation
        fadeInNoDelay: 'fadeIn 0.5s ease-out forwards', // Creates a 0.5s fade-in animation
      },
    },
  },
  plugins: [],
}
