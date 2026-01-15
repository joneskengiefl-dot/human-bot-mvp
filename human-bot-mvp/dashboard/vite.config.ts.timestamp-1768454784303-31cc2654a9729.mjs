// vite.config.ts
import { defineConfig } from "file:///E:/Test%20Project/2/human-bot-mvp/dashboard/node_modules/vite/dist/node/index.js";
import react from "file:///E:/Test%20Project/2/human-bot-mvp/dashboard/node_modules/@vitejs/plugin-react/dist/index.js";
var vite_config_default = defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    // Listen on all network interfaces
    port: 3e3,
    strictPort: false,
    // Try next available port if 3000 is taken
    open: true,
    // Automatically open browser
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true
      },
      "/ws": {
        target: "ws://localhost:8000",
        ws: true
      }
    }
  }
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcudHMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCJFOlxcXFxUZXN0IFByb2plY3RcXFxcMlxcXFxodW1hbi1ib3QtbXZwXFxcXGRhc2hib2FyZFwiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9maWxlbmFtZSA9IFwiRTpcXFxcVGVzdCBQcm9qZWN0XFxcXDJcXFxcaHVtYW4tYm90LW12cFxcXFxkYXNoYm9hcmRcXFxcdml0ZS5jb25maWcudHNcIjtjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfaW1wb3J0X21ldGFfdXJsID0gXCJmaWxlOi8vL0U6L1Rlc3QlMjBQcm9qZWN0LzIvaHVtYW4tYm90LW12cC9kYXNoYm9hcmQvdml0ZS5jb25maWcudHNcIjtpbXBvcnQgeyBkZWZpbmVDb25maWcgfSBmcm9tICd2aXRlJ1xyXG5pbXBvcnQgcmVhY3QgZnJvbSAnQHZpdGVqcy9wbHVnaW4tcmVhY3QnXHJcblxyXG5leHBvcnQgZGVmYXVsdCBkZWZpbmVDb25maWcoe1xyXG4gIHBsdWdpbnM6IFtyZWFjdCgpXSxcclxuICBzZXJ2ZXI6IHtcclxuICAgIGhvc3Q6ICcwLjAuMC4wJywgLy8gTGlzdGVuIG9uIGFsbCBuZXR3b3JrIGludGVyZmFjZXNcclxuICAgIHBvcnQ6IDMwMDAsXHJcbiAgICBzdHJpY3RQb3J0OiBmYWxzZSwgLy8gVHJ5IG5leHQgYXZhaWxhYmxlIHBvcnQgaWYgMzAwMCBpcyB0YWtlblxyXG4gICAgb3BlbjogdHJ1ZSwgLy8gQXV0b21hdGljYWxseSBvcGVuIGJyb3dzZXJcclxuICAgIHByb3h5OiB7XHJcbiAgICAgICcvYXBpJzoge1xyXG4gICAgICAgIHRhcmdldDogJ2h0dHA6Ly9sb2NhbGhvc3Q6ODAwMCcsXHJcbiAgICAgICAgY2hhbmdlT3JpZ2luOiB0cnVlLFxyXG4gICAgICB9LFxyXG4gICAgICAnL3dzJzoge1xyXG4gICAgICAgIHRhcmdldDogJ3dzOi8vbG9jYWxob3N0OjgwMDAnLFxyXG4gICAgICAgIHdzOiB0cnVlLFxyXG4gICAgICB9XHJcbiAgICB9XHJcbiAgfVxyXG59KVxyXG4iXSwKICAibWFwcGluZ3MiOiAiO0FBQXlULFNBQVMsb0JBQW9CO0FBQ3RWLE9BQU8sV0FBVztBQUVsQixJQUFPLHNCQUFRLGFBQWE7QUFBQSxFQUMxQixTQUFTLENBQUMsTUFBTSxDQUFDO0FBQUEsRUFDakIsUUFBUTtBQUFBLElBQ04sTUFBTTtBQUFBO0FBQUEsSUFDTixNQUFNO0FBQUEsSUFDTixZQUFZO0FBQUE7QUFBQSxJQUNaLE1BQU07QUFBQTtBQUFBLElBQ04sT0FBTztBQUFBLE1BQ0wsUUFBUTtBQUFBLFFBQ04sUUFBUTtBQUFBLFFBQ1IsY0FBYztBQUFBLE1BQ2hCO0FBQUEsTUFDQSxPQUFPO0FBQUEsUUFDTCxRQUFRO0FBQUEsUUFDUixJQUFJO0FBQUEsTUFDTjtBQUFBLElBQ0Y7QUFBQSxFQUNGO0FBQ0YsQ0FBQzsiLAogICJuYW1lcyI6IFtdCn0K
