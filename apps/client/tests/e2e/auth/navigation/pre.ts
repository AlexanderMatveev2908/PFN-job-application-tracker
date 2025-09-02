import { Page } from "@playwright/test";
import { closeToast, getByTxt, preTest } from "../../lib/idx";

export const preAuthNavigation = async (page: Page) => {
  await preTest(page, "/");

  await closeToast(page);

  await getByTxt(page, "Script worked ✌🏽");
};
