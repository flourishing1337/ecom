import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  eslint: {
    ignoreDuringBuilds: true,  // ✅ Allow build even if ESLint errors exist
  },
};

export default nextConfig;
