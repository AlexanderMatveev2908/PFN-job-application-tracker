import { Page } from "@playwright/test";
import { getByTxt } from "../../lib/get";
import { closeToast } from "../../lib/sideActions";
import { preTest } from "../../lib/pre";

export const preAuthNavigation = async (page: Page) => {
  await preTest(page, "/");

  await closeToast(page);

  await getByTxt(page, "Script worked ✌🏽");
};
