import { Page } from "@playwright/test";
import { waitTmr } from "../shortcuts/wait";

export const preTest = async (page: Page, url: string) => {
  await page.goto(url);

  await waitTmr(page, 1500);
};
