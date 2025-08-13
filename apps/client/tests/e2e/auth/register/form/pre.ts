import { Page } from "@playwright/test";
import { closeToast } from "../../../lib/sideActions";
import { getByID } from "../../../lib/get";

export const pre = async (page: Page) => {
  await page.goto("/auth/register");

  await closeToast(page);

  await getByID(page, "register_form");
};
