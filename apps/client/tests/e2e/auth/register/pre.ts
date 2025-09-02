import { Page } from "@playwright/test";
import { getByID } from "../../lib/shortcuts/get";
import { preTest } from "../../lib/conf/pre";

export const preAuthRegister = async (page: Page) => {
  await preTest(page, "auth/register");

  return await getByID(page, "register__form");
};
