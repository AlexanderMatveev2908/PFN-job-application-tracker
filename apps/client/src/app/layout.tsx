import type { Metadata } from "next";
import "../styles/globals.css";
import { Fira_Code } from "next/font/google";
import { genStoreSSR } from "@/core/store";
import Providers from "@/features/layout/shells/Providers";
import Toast from "@/features/layout/components/Toast/Toast";
import WrapWakeUp from "@/features/layout/shells/WrapWakeUp/WrapWakeUp";
import Header from "@/features/layout/components/Header/Header";
import Sidebar from "@/features/layout/components/Sidebar/Sidebar";

const fira_code = Fira_Code({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Replace App name...",
  description: "Fancy description app...",
  icons: {
    icon: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const store = genStoreSSR({});

  return (
    <html lang="en" data-scroll-behavior="smooth">
      <body
        className={`${fira_code.className} min-h-screen h-full w-full antialiased bg-neutral-950 text-neutral-200`}
      >
        <Providers
          {...{
            preloadedState: store.getState(),
          }}
        >
          <div
            id="portal-root"
            className="w-full max-w-full min-h-full  overflow-x-hidden absolute pointer-events-none"
          ></div>

          <Header />
          <Sidebar />
          <Toast />

          <WrapWakeUp>{children}</WrapWakeUp>
        </Providers>
      </body>
    </html>
  );
}
