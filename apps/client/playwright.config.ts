import { defineConfig } from "@playwright/test";
import "dotenv/config";

export default defineConfig({
  testDir: "./tests/e2e",
  timeout: 60 * 1000,
  expect: {
    timeout: 30 * 1000,
  },
  retries: 0,
  workers: 8,
  use: {
    baseURL:
      process.env.NEXT_PUBLIC_ENV === "test"
        ? process.env.NEXT_PUBLIC_FRONT_URL_TEST
        : process.env.NEXT_PUBLIC_FRONT_URL_DEV,
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true,
    video: "retain-on-failure",
    screenshot: "only-on-failure",
  },
  reporter: [["html", { open: "never" }]],
  testMatch: ["**/*.test.ts"],

  projects: [
    { name: "chromium", use: { browserName: "chromium" } },
    { name: "firefox", use: { browserName: "firefox" } },
  ],
});
