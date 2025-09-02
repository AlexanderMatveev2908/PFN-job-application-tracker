import { Page } from "@playwright/test";
import { getByID, preTest } from "../../lib/idx";

export const preAuthLogin = async (page: Page) => {
  await preTest(page, "auth/login");

  return await getByID(page, "login__form");
};
