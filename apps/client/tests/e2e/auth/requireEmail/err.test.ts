import test from "@playwright/test";
import { preRequireEmail } from "./pre";
import { getByID, getByTxt } from "../../lib/shortcuts/get";
import { clickByID } from "../../lib/shortcuts/click";
import { waitTmr } from "../../lib/shortcuts/wait";

test("invalid email", async ({ browser }) => {
  const { form, page } = await preRequireEmail(browser);

  await (await getByID(form, "email")).fill("<>@<>");

  await waitTmr(page);

  await getByTxt(page, "invalid email");
});

test("non existent", async ({ browser }) => {
  const { form, page, payload } = await preRequireEmail(browser);

  await (await getByID(form, "email")).fill(payload.email);

  await clickByID(form, "conf_email__form__submit");

  await waitTmr(page);

  await getByTxt(page, "user not found");
});
