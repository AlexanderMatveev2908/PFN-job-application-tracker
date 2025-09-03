import { Browser } from "@playwright/test";
import { genRegisterPayload, PayloadRegisterT } from "../../lib/conf/payloads";
import { preTest } from "../../lib/conf/pre";
import { getByID } from "../../lib/shortcuts/get";
import { registerUserOk } from "../../lib/actions/auth";

export const preRequireEmail = async (
  browser: Browser,
  mustExists?: boolean
) => {
  let payload: PayloadRegisterT;
  if (mustExists) payload = (await registerUserOk(browser)).payload;
  else payload = genRegisterPayload();

  const page = await preTest(browser, "/auth/require-email/confirm-email");

  const form = await getByID(page, "conf_email__form");

  return {
    payload,
    page,
    form,
  };
};
