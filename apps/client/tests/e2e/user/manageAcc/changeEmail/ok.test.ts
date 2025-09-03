import test from "@playwright/test";
import { getAccessManageAcc } from "../../../lib/actions/user";
import { clickByID, getByID, getByTxt, isToastOk } from "../../../lib/idx";
import { faker } from "@faker-js/faker";
import { waitURL } from "../../../lib/shortcuts/wait";
import { genMailNoticeMsg } from "@/core/constants/etc";

test("change email ok", async ({ browser }) => {
  const { page, container } = await getAccessManageAcc(browser);

  const form = await getByID(container, "change_email__form");
  await (await getByID(form, "email")).fill(faker.internet.email());

  await clickByID(form, "change_email__form__submit");

  await waitURL(page, "/notice");

  await isToastOk(page, "email sent to new address");

  await getByTxt(page, genMailNoticeMsg("to change your email address"));
});
