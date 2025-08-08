const isDev = process.env.NEXT_PUBLIC_ENV === "development";

export const envApp = {
  isDev,
  ENV: process.env.NEXT_PUBLIC_ENV,
  BACK_URL:
    process.env.NEXT_PUBLIC_BACK_URL_TEST ??
    (isDev
      ? process.env.NEXT_PUBLIC_BACK_URL_DEV
      : process.env.NEXT_PUBLIC_BACK_URL),
};
