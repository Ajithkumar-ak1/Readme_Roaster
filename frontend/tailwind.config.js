/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ember: "#ff6a3d",
        coal: "#101013",
        smoke: "#b7b6bb",
        panel: "#1a1a21",
      },
      boxShadow: {
        glow: "0 0 50px rgba(255, 106, 61, 0.18)",
      },
    },
  },
  plugins: [],
};
