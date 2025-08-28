import { Page } from "@playwright/test";
import { getByTxt } from "../../lib/get";

export const pre = async (page: Page) => {
  await page.goto("/");

  await getByTxt(page, "Script worked ✌🏽");
};
