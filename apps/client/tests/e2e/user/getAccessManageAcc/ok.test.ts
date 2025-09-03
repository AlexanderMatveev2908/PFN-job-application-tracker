import test from "@playwright/test";
import { getAccessManageAcc } from "../../lib/actions/user";

test("get access mng acc ok", async ({ browser }) => {
  await getAccessManageAcc(browser);
});
