import { Browser } from "@playwright/test";
import { registerUserOk } from "../../lib/actions/fullActions";
import { genRegisterPayload, PayloadRegisterT } from "../../lib/conf/payloads";
import { preTest } from "../../lib/conf/pre";
import { getByID } from "../../lib/shortcuts/get";

export const preRequireEmail = async (
  browser: Browser,
  mustExists?: boolean
) => {
  const ctxRegister = await browser.newContext();
  const pageRegister = await ctxRegister.newPage();

  let payload: PayloadRegisterT;
  if (mustExists) payload = (await registerUserOk(pageRegister)).payload;
  else payload = genRegisterPayload();

  const pageRequire = await (await browser.newContext()).newPage();

  await preTest(pageRequire, "/auth/require-email/confirm-email");

  const form = await getByID(pageRequire, "conf_email__form");

  return {
    payload,
    pageRequire,
    form,
  };
};
