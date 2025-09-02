import { Browser } from "@playwright/test";
import { waitTmr } from "../shortcuts/wait";

export const preTest = async (browser: Browser, url: string) => {
  const page = await (await browser.newContext()).newPage();

  await page.goto(url);

  await waitTmr(page, 2000);

  return page;
};
