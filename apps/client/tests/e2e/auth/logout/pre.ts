import { Browser } from "@playwright/test";
import { loginUserOk } from "../../lib/fullActions";
import { preTest } from "../../lib/pre";

export const preAuthLogout = async (browser: Browser) => {
  const { payload, loginPage: page } = await loginUserOk(browser);

  await preTest(page, "/protected");

  return {
    payload,
    page,
  };
};
