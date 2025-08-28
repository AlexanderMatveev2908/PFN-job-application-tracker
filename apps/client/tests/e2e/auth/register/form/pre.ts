import { Page } from "@playwright/test";
import { getByID } from "../../../lib/get";

export const pre = async (page: Page) => {
  await page.goto("/auth/register");

  return await getByID(page, "register_form");
};
