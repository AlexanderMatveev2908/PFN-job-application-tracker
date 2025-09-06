import test, { expect } from "@playwright/test";
import { genPwd } from "@/core/lib/pwd";
import { REG_JWT } from "@/core/constants/regex";
import { preAuthRecoverPwd } from "./pre";
import { clickByID, getByID } from "../../lib_tests/idx";
import { waitURL } from "../../lib_tests/shortcuts/wait";

test("recover pwd ok", async ({ browser }) => {
  const { form, page } = await preAuthRecoverPwd(browser);

  const newPwd = genPwd();
  await (await getByID(form, "password")).fill(newPwd);
  await (await getByID(form, "confirm_password")).fill(newPwd);

  await clickByID(form, "recover_pwd__form__submit");

  await waitURL(page, "/");

  const jwt = await page.evaluate(() => sessionStorage.getItem("access_token"));
  expect(REG_JWT.test(jwt ?? ""));
});
