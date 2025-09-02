import { Page } from "@playwright/test";
import { waitTmr } from "./sideActions";

export const preTest = async (page: Page, url: string) => {
  await page.goto(url);

  await waitTmr(page, 1500);
};
