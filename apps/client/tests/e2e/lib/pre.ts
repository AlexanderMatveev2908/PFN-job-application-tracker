import { Page } from "@playwright/test";
import { waitTest } from "./sideActions";

export const preTest = async (page: Page, url: string) => {
  await page.goto(url);

  await waitTest(page, 1500);
};
