import test from "@playwright/test";
import { changeEmailOk } from "../../../lib/actions/user";

test("change email ok", async ({ browser }) => {
  await changeEmailOk(browser);
});
