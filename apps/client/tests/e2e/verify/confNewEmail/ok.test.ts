import test from "@playwright/test";
import { getTokensLib, isToastOk, preTest } from "../../lib/idx";
import { TokenT } from "@/common/types/tokens";
import { changeEmailOk } from "../../lib/actions/user";
import { waitURL } from "../../lib/shortcuts/wait";

test("conf new email", async ({ browser }) => {
  const { payload } = await changeEmailOk(browser);

  const { cbc_hmac_token } = await getTokensLib(browser, {
    tokenType: TokenT.CHANGE_EMAIL,
    payload,
  });

  const page = await preTest(browser, "/");

  await page.goto(`/verify?cbc_hmac_token=${cbc_hmac_token}`);

  await waitURL(page, "/");

  await isToastOk(page, "email updated successfully");
});
