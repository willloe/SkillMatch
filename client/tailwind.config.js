/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      boxShadow: {
        neumorphism: "8px 8px 16px #d1d9e6, -8px -8px 16px #ffffff",
        'inner-neumorphism': "inset 4px 4px 8px #d1d9e6, inset -4px -4px 8px #ffffff",
        'neumorphism-button': "4px 4px 6px #c5ccd9, -2px -2px 4px #ffffff",
      },
    },
  },
  plugins: [],
};