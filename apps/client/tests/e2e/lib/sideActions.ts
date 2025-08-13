import { Page } from "@playwright/test";
import { getByID } from "./get";

export const closeToast = async (page: Page) => {
  try {
    const el = await getByID(page, "toast");

    await el.waitFor({ state: "visible" });

    await el.getByTestId("toast__close_btn").click();
  } catch {}
};
