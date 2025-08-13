import { Page } from "@playwright/test";
import { getByTxt } from "../../lib/get";
import { closeToast } from "../../lib/sideActions";

export const pre = async (page: Page) => {
  await page.goto("/");

  await closeToast(page);

  await getByTxt(page, "Script worked ✌🏽");
};
