import { Locator, Page } from "@playwright/test";
import { getByTxt } from "./get";

export const clickByID = async (loc: Page | Locator, id: string) => {
  const el = loc.getByTestId(id);
  await el.waitFor({ state: "visible" });

  await el.click();
};

export const clickByTxt = async (loc: Locator, txt: string) => {
  const el = await getByTxt(loc, txt);

  await el.click();
};
