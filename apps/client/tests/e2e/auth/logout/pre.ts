import { Browser } from "@playwright/test";
import { loginUserOk } from "../../lib/actions/auth";
import { goPage } from "../../lib/shortcuts/go";

export const preAuthLogout = async (browser: Browser) => {
  const { payload, page } = await loginUserOk(browser);

  await goPage(page, "/protected");

  return {
    payload,
    page,
  };
};
