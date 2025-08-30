import { Page } from "@playwright/test";
import { getByID } from "../../lib/get";
import { preTest } from "../../lib/pre";

export const preAuthRegister = async (page: Page) => {
  await preTest(page, "auth/register");

  return await getByID(page, "register_form");
};
