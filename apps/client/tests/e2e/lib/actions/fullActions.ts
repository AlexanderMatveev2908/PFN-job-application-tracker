import { Browser, expect, Page } from "@playwright/test";
import { genRegisterPayload, PayloadRegisterT } from "../conf/payloads";
import { preTest } from "../conf/pre";
import { REG_CBC_HMAC } from "@/core/constants/regex";
import { TokenT } from "@/common/types/tokens";
import { UserT } from "@/features/user/types";
import { BASE_URL } from "../conf/constants";

export interface GetTokensReturnT {
  access_token: string;
  user: UserT;
  cbc_hmac_token: string;
  payload: PayloadRegisterT;
  page: Page;
}

export const getTokensLib = async (
  browser: Browser,
  {
    tokenType = TokenT.CONF_EMAIL,
    verifyUser = false,
    payload = genRegisterPayload(),
  }: { tokenType?: TokenT; verifyUser?: boolean; payload?: PayloadRegisterT }
): Promise<GetTokensReturnT> => {
  const page = await preTest(browser, "/");

  const res = await page.request.post(
    `${BASE_URL}/test/tokens-health?cbc_hmac_token_t=${tokenType}&verify_user=${verifyUser}`,
    { data: payload }
  );
  const data = await res.json();

  await page.evaluate((token: string) => {
    sessionStorage.setItem("access_token", token);
  }, data.access_token);

  expect(REG_CBC_HMAC.test(data.cbc_hmac_token));

  return { ...data, page: page };
};
