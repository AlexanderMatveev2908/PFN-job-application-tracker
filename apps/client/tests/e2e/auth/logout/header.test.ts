import test from "@playwright/test";
import { getByID, getByTxt } from "../../lib/get";
import { extractInitialsUser } from "@/core/lib/formatters";
import { waitTest, waitURL } from "../../lib/sideActions";
import { preAuthLogout } from "./pre";
import { clickByID } from "../../lib/click";

test("logout header ok", async ({ browser }) => {
  const { payload, page } = await preAuthLogout(browser);

  const drop = await getByID(page, "header__toggle_drop");

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  await getByTxt(drop, extractInitialsUser(payload as any).toLowerCase());

  await drop.click();

  await waitTest(page);

  await clickByID(page, "header_link__logout");

  await waitURL(page, "/");

  await waitTest(page);

  await getByTxt(page, "logout successful");
});
