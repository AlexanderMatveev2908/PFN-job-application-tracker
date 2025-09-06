import test from "@playwright/test";
import { getAccessManageAcc } from "../../../lib_tests/actions/user";
import { clickByID, getByID, isToastOk } from "../../../lib_tests/idx";
import { waitTmr } from "../../../lib_tests/shortcuts/wait";
import { genPwd } from "@/core/lib/pwd";

test("change pwd ok", async ({ browser }) => {
  const { page, container } = await getAccessManageAcc(browser);

  await clickByID(container, "btns_swapper_next_swap");

  await waitTmr(page);

  const form = await getByID(container, "change_password__form");

  const newPwd = genPwd();

  await (await getByID(form, "password")).fill(newPwd);
  await (await getByID(form, "confirm_password")).fill(newPwd);

  await clickByID(form, "change_password__form__submit");

  await waitTmr(page);

  await isToastOk(page, "password updated");
});
