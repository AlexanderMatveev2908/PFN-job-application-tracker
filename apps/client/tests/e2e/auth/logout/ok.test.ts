import test from "@playwright/test";
import { loginUserOk } from "../../lib/fullActions";
import { preTest } from "../../lib/pre";
import { getByID, getByTxt } from "../../lib/get";
import { extractInitialsUser } from "@/core/lib/formatters";
import { waitTest, waitURL } from "../../lib/sideActions";

test("logout ok", async ({ browser }) => {
  const { payload, loginPage: page } = await loginUserOk(browser);

  await preTest(page, "/protected");

  const drop = await getByID(page, "header__toggle_drop");

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  await getByTxt(drop, extractInitialsUser(payload as any).toLowerCase());

  await drop.click();

  await waitTest(page);

  await page.pause();

  const logoutBtn = await getByID(page, "header_link__logout");

  await logoutBtn.click();

  await waitURL(page, "/");

  await waitTest(page);

  await getByTxt(page, "logout successful");
});
