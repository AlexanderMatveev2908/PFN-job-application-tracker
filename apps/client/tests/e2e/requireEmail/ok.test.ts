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

  await clickByID(form, "conf_email__footer_form__submit_btn");

  await waitURL(page, "/notice");

  await waitTest(page);

  await getByTxt(page, genMailNoticeMsg("to confirm the account"));

  await getByTxt(page, "email sent");

  // ? ... tested manually verify part including part of opening gmail using btn helper that search by my domain that use no-reply as subdomain
});
