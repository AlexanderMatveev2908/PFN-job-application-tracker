import test from "@playwright/test";
import { clickByID, getByID, isToastOk } from "../../../lib/idx";
import { waitTmr, waitURL } from "../../../lib/shortcuts/wait";
import { getAccessManageAcc } from "../../../lib/actions/user";

test("del acc ok", async ({ browser }) => {
  const { page, container } = await getAccessManageAcc(browser);

  await waitTmr(page);

  for (let i = 0; i < 3; i++) {
    await clickByID(container, "btns_swapper_next_swap");
    await waitTmr(page);
  }

  const form = await getByID(container, "delete_account__swap");

  await clickByID(form, "delete_account__btn");

  await waitTmr(page);

  await clickByID(page, "pop__delete__btn");

  await waitURL(page, "/notice");

  await isToastOk(page, "account deleted");
});
