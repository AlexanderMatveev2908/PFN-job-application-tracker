import { TokenT } from "@/common/types/tokens";
import test, { expect } from "@playwright/test";
import { getTokensLib } from "../../lib/fullActions";
import { waitURL } from "../../lib/sideActions";
import { getByID } from "../../lib/get";
import { genPwd } from "@/core/lib/pwd";
import { clickByID } from "../../lib/click";
import { REG_JWT } from "@/core/constants/regex";

test("ok", async ({ browser }) => {
  const { cbc_hmac_token } = await getTokensLib(browser, {
    tokenType: TokenT.RECOVER_PWD,
  });

  const page = await (await browser.newContext()).newPage();

  await page.goto(`/verify?cbc_hmac_token=${cbc_hmac_token}`);

  await waitURL(page, "/auth/recover-password");

  const form = await getByID(page, "recover_pwd__form");

  const newPwd = genPwd();
  await (await getByID(form, "password")).fill(newPwd);
  await (await getByID(form, "confirm_password")).fill(newPwd);

  await clickByID(form, "recover_pwd__footer_form__submit_btn");

  await waitURL(page, "/");

  const jwt = await page.evaluate(() => sessionStorage.getItem("access_token"));
  expect(REG_JWT.test(jwt ?? ""));
});
