import test from "@playwright/test";
import { preRequireEmail } from "./pre";
import { genMailNoticeMsg } from "@/core/constants/etc";
import { getByID, getByTxt } from "../../lib/shortcuts/get";
import { clickByID } from "../../lib/shortcuts/click";
import { waitTmr, waitURL } from "../../lib/shortcuts/wait";

test("ok", async ({ browser }) => {
  const {
    form,
    pageRequire: page,
    payload,
  } = await preRequireEmail(browser, true);

  await (await getByID(form, "email")).fill(payload.email);

  await clickByID(form, "conf_email__form__submit");

  await waitURL(page, "/notice");

  await waitTmr(page);

  await getByTxt(page, genMailNoticeMsg("to confirm the account"));

  await getByTxt(page, "email sent");
});
