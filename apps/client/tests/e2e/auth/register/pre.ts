import { Browser } from "@playwright/test";
import { getByID } from "../../lib/shortcuts/get";
import { preTest } from "../../lib/conf/pre";

export const preAuthRegister = async (browser: Browser) => {
  const page = await preTest(browser, "auth/register");

  return {
    form: await getByID(page, "register__form"),
    page,
  };
};
