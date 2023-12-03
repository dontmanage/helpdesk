module.exports = {
  mode: "jit",
  presets: [require("dontmanage-ui/src/utils/tailwind.config")],
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
    "./node_modules/dontmanage-ui/src/components/**/*.{vue,js,ts,jsx,tsx}",
    "../node_modules/dontmanage-ui/src/components/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      height: {
        18: "68px",
      },
      margin: {
        3.5: "14px",
      },
      padding: {
        2.5: "10px",
        3.5: "14px",
      },
    },
  },
  plugins: [
    require("@tailwindcss/line-clamp"),
    require("@tailwindcss/typography"),
  ],
};
