import { Page } from "@playwright/test";
import { clickByID } from "../shortcuts/click";
import { getByID } from "../shortcuts/get";

export const closeToast = async (page: Page): Promise<undefined> => {
  try {
    const toast = await getByID(page, "toast");

    if (toast) await clickByID(toast, "toast__close_btn");
  } catch {}
};
