import { Browser } from "@playwright/test";
import { loginUserOk } from "../../lib/actions/fullActions";
import { waitTmr } from "../../lib/shortcuts/wait";

export const preAuthLogout = async (browser: Browser) => {
  const { payload, page } = await loginUserOk(browser);

  await page.goto("/protected");
  await waitTmr(page, 2000);

  return {
    payload,
    page,
  };
};
