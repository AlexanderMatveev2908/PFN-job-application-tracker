import test from "@playwright/test";
import { getTokensLib } from "../../lib/actions/fullActions";
import { getByID, getByTxt } from "../../lib/shortcuts/get";
import { closeToast, waitTmr, waitURL } from "../../lib/actions/sideActions";
import { clickByID } from "../../lib/shortcuts/click";
import { genMailNoticeMsg } from "@/core/constants/etc";

test("ok", async ({ browser }) => {
  const { page, payload } = await getTokensLib(browser, {});

  await page.reload();

  await waitTmr(page);

  await closeToast(page);

  const drop = await getByID(page, "header__toggle_drop");

  await drop.click();

  await waitTmr(page, 2500);

  await clickByID(page, "header_link__confirm_email");

  await waitURL(page, "/user/require-email/confirm-email");

  const form = await getByID(page, "conf_email__form");

  await (await getByID(form, "email")).fill(payload.email + "abcd");

  await clickByID(form, "conf_email__form__submit");

  await waitTmr(page, 2000);

  await getByTxt(page, "email different from one declared at register time");

  await (await getByID(form, "email")).fill(payload.email);

  await clickByID(form, "conf_email__form__submit");

  await waitURL(page, "/notice");

  await getByTxt(page, genMailNoticeMsg("to confirm the account"));
});
