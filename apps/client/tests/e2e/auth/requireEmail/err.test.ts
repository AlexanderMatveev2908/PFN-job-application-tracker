import test from "@playwright/test";
import { preRequireEmail } from "./pre";
import { getByID, getByTxt } from "../../lib/shortcuts/get";
import { waitTmr } from "../../lib/actions/sideActions";
import { clickByID } from "../../lib/shortcuts/click";

test("invalid email", async ({ browser }) => {
  const { form, pageRequire: page } = await preRequireEmail(browser);

  await (await getByID(form, "email")).fill("<>@<>");

  await waitTmr(page);

  await getByTxt(page, "invalid email");
});

test("non existent", async ({ browser }) => {
  const { form, pageRequire: page, payload } = await preRequireEmail(browser);

  await (await getByID(form, "email")).fill(payload.email);

  await clickByID(form, "conf_email__form__submit");

  await waitTmr(page);

  await getByTxt(page, "user not found");
});
