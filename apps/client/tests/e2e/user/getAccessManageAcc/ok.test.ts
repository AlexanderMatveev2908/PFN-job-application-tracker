import test from "@playwright/test";
import { preUserAccessAcc } from "./pre";
import { clickByID, getByID, getByTxt } from "../../lib/idx";
import { genPwd } from "@/core/lib/pwd";
import { waitTmr, waitURL } from "../../lib/shortcuts/wait";

test("ok", async ({ browser }) => {
  const { form, page, payload } = await preUserAccessAcc(browser);

  const pwd = await getByID(form, "password");
  await pwd.fill(genPwd());

  await clickByID(form, "manage_acc__form__submit");

  const toast = await getByID(page, "toast");
  await getByTxt(toast, "err");

  await pwd.fill(payload.password);
  await clickByID(form, "manage_acc__form__submit");

  await waitTmr(page);

  await waitURL(page, "/user/manage-account");
  await getByTxt(toast, "ok");
});
