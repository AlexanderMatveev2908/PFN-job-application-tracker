import { TokenT } from "@/common/types/tokens";
import { getByID } from "../../lib/get";
import { waitURL } from "../../lib/sideActions";
import { getTokensLib } from "../../lib/fullActions";
import { Browser } from "@playwright/test";

export const preAuthRecoverPwd = async (browser: Browser) => {
  const { cbc_hmac_token, payload } = await getTokensLib(browser, {
    tokenType: TokenT.RECOVER_PWD,
  });

  const page = await (await browser.newContext()).newPage();

  await page.goto(`/verify?cbc_hmac_token=${cbc_hmac_token}`);

  await waitURL(page, "/auth/recover-password");

  const form = await getByID(page, "recover_pwd__form");

  return {
    form,
    page,
    payload,
  };
};
