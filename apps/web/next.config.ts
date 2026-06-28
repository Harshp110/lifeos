import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  transpilePackages: ["@lifeos/config", "@lifeos/types", "@lifeos/ui"],
};

export default nextConfig;
