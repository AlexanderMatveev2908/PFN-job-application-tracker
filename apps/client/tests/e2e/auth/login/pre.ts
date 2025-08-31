import { Page } from "@playwright/test";
import { getByID } from "../../lib/get";
import { preTest } from "../../lib/pre";

export const preAuthLogin = async (page: Page) => {
  await preTest(page, "auth/login");

  return await getByID(page, "login__form");
};
