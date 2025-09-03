import test from "@playwright/test";
import { preAuthRecoverPwd } from "./pre";
import { clickByID, getByID, getByTxt } from "../../lib/idx";
import { waitTmr } from "../../lib/shortcuts/wait";

test("recover pwd err same pwd", async ({ browser }) => {
  const { page, form, payload } = await preAuthRecoverPwd(browser);

  await (await getByID(form, "password")).fill(payload.password);
  await (await getByID(form, "confirm_password")).fill(payload.password);

  await clickByID(form, "recover_pwd__form__submit");

  await waitTmr(page);

  await getByTxt(page, "new password must be different from old one");
});
