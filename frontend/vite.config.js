import react from "@vitejs/plugin-react";
import { fileURLToPath, URL } from "url";
import { defineConfig } from "vite";
export default (function () {
    return defineConfig({
        plugins: [
            react(),
        ],
        resolve: {
            alias: [{ find: "@", replacement: fileURLToPath(new URL("./src", import.meta.url)) }],
        },
        server: {
            host: "0.0.0.0",
            port: 4000,
        },
        build: {
            reportCompressedSize: false,
            sourcemap: true,
            rollupOptions: {
                output: {
                    manualChunks: {
                        legacy: ["moment", "moment-timezone", "react-apexcharts", "jquery"],
                    },
                },
            },
        },
    });
});
