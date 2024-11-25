import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  env: {
    API_BASE: process.env.API_BASE,
    NEXT_PUBLIC_API_BASE: process.env.NEXT_PUBLIC_API_BASE,
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:5000/api/:path*',
      },
    ]
  }
};

export default nextConfig;
