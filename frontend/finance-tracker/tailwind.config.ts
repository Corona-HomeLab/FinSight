import type { Config } from "tailwindcss";

export default {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: 'var(--primary)',
          dark: 'var(--primary-dark)',
          light: 'var(--primary-light)',
        },
        success: {
          DEFAULT: 'var(--success)',
          dark: 'var(--success-dark)',
          light: 'var(--success-light)',
        },
        accent: {
          gold: 'var(--accent-gold)',
          purple: 'var(--accent-purple)',
          orange: 'var(--accent-orange)',
        },
        background: 'var(--background)',
        foreground: 'var(--foreground)',
        gray: {
          medium: 'var(--gray-medium)',
        },
        error: 'var(--error)',
        warning: 'var(--warning)',
      },
    },
  },
  plugins: [],
} satisfies Config;
