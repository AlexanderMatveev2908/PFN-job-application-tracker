import type { Metadata } from "next";
import "../styles/globals.css";
import { Fira_Code } from "next/font/google";
import { genStoreSSR } from "@/core/store";
import Providers from "@/features/layout/shells/Providers";
import Toast from "@/features/layout/components/Toast/Toast";
import WrapWakeUp from "@/features/layout/shells/WrapWakeUp/WrapWakeUp";
import Header from "@/features/layout/components/Header/Header";

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
        className={`${fira_code.className} min-h-screen h-full w-full antialiased bg-neutral-950`}
      >
        <Providers
          {...{
            preloadedState: store.getState(),
          }}
        >
          <Header />
          <Toast />

          <WrapWakeUp>{children}</WrapWakeUp>
        </Providers>
      </body>
    </html>
  );
}
