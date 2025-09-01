import test from "@playwright/test";
import { preRequireEmail } from "./pre";
import { getByID, getByTxt } from "../lib/get";
import { clickByID } from "../lib/click";
import { waitTest, waitURL } from "../lib/sideActions";
import { genMailNoticeMsg } from "@/core/constants/etc";

test("ok", async ({ browser }) => {
  const {
    form,
    pageRequire: page,
    payload,
  } = await preRequireEmail(browser, true);

  await (await getByID(form, "email")).fill(payload.email);

  await clickByID(form, "conf_email__form__submit");

  await waitURL(page, "/notice");

  await waitTest(page);

  await getByTxt(page, genMailNoticeMsg("to confirm the account"));

  await getByTxt(page, "email sent");
});
