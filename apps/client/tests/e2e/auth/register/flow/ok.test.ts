import test from "@playwright/test";
import { preAuthRegister } from "../pre";
import { faker } from "@faker-js/faker";
import { clickByID } from "../../../lib/click";
import { genPwd } from "@/core/lib/etc";
import { getByTxt } from "../../../lib/get";
import { genMailNoticeMsg } from "@/core/constants/etc";
import { waitURL } from "../../../lib/sideActions";

test("register ok", async ({ page }) => {
  const el = await preAuthRegister(page);

  await el.getByTestId("first_name").fill(faker.person.firstName());
  await el.getByTestId("last_name").fill(faker.person.lastName());
  await el.getByTestId("email").fill(faker.internet.email());

  await clickByID(el, "btns_swapper_next_swap");

  const pwd = genPwd();

  await el.getByTestId("password").fill(pwd);
  await el.getByTestId("confirm_password").fill(pwd);

  await clickByID(el, "body__form_terms");

  await clickByID(el, "register__footer_form__submit_btn");

  await waitURL(page, "/notice");

  await getByTxt(page, genMailNoticeMsg("to confirm the account"));

  // ? ... manual checked emails are ok
});
