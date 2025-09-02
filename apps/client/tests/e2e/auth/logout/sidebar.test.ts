import test from "@playwright/test";
import { preAuthLogout } from "./pre";
import { clickByID } from "../../lib/shortcuts/click";
import { getByID, getByTxt } from "../../lib/shortcuts/get";
import { waitTmr, waitURL } from "../../lib/shortcuts/wait";

test("logout sidebar ok", async ({ browser }) => {
  const { payload, page } = await preAuthLogout(browser);

  await clickByID(page, "header__toggle_sidebar");

  await waitTmr(page);

  const span = await getByID(page, "sidebar__span_mail");

  await getByTxt(span, payload.email);

  await clickByID(page, "side_link__logout");

  await waitURL(page, "/");

  await waitTmr(page);

  await getByTxt(page, "logout successful");
});
