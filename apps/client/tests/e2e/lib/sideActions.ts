import { Page } from "@playwright/test";
import { getByID } from "./get";

export const closeToast = async (page: Page) => {
  try {
    const el = await getByID(page, "toast");

    (await el.getByTestId("toast_close_btn")).click();
  } catch {}
};
