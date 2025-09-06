import test from "@playwright/test";
import { getAccessManageAcc2FA } from "../../lib/actions/user";

test("manage acc 2FA TOTP ok", async ({ browser }) => {
  const { form2FA, totp_secret } = await getAccessManageAcc2FA(browser);
});
