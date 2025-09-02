import { genMailNoticeMsg } from "@/core/constants/etc";
import { preAuthRegister } from "../../auth/register/pre";
import { clickByID } from "../shortcuts/click";
import { getByID, getByTxt } from "../shortcuts/get";
import { Browser, expect, Page } from "@playwright/test";
import { genRegisterPayload, PayloadRegisterT } from "../conf/payloads";
import { preAuthLogin } from "../../auth/login/pre";
import { preTest } from "../conf/pre";
import { REG_CBC_HMAC } from "@/core/constants/regex";
import { TokenT } from "@/common/types/tokens";
import { UserT } from "@/features/user/types";
import { BASE_URL } from "../conf/constants";
import { waitTmr, waitURL } from "../shortcuts/wait";

export const registerUserOk = async (
  page: Page,
  payload: PayloadRegisterT = genRegisterPayload()
) => {
  const el = await preAuthRegister(page);

  const firstName = await getByID(el, "first_name");
  firstName.fill(payload.first_name);

  const lastName = await getByID(el, "last_name");
  lastName.fill(payload.last_name);

  const email = await getByID(el, "email");
  email.fill(payload.email);

  await clickByID(el, "btns_swapper_next_swap");

  await waitTmr(page);

  const pwd = await getByID(el, "password");
  await pwd.fill(payload.password);

  const confPwd = await getByID(el, "confirm_password");
  confPwd.fill(payload.password);

  await clickByID(el, "body__form_terms");

  await clickByID(el, "register__form__submit");

  await waitURL(page, "/notice");

  await getByTxt(page, genMailNoticeMsg("to confirm the account"));

  return {
    payload,
  };
};

export const loginUserOk = async (browser: Browser) => {
  const payload = genRegisterPayload();

  const registerCtx = await browser.newContext();
  const registerPage = await registerCtx.newPage();
  await registerUserOk(registerPage, payload);

  const loginCtx = await browser.newContext();
  const loginPage = await loginCtx.newPage();

  const el = await preAuthLogin(loginPage);

  const email = await getByID(el, "email");
  email.fill(payload.email);

  const pwd = await getByID(el, "password");
  pwd.fill(payload.password);

  await clickByID(el, "login__form__submit");

  await waitURL(loginPage, "/");

  await waitTmr(loginPage);

  await getByTxt(loginPage, "operation successful");

  return {
    payload,
    loginPage,
  };
};

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
  }: { tokenType?: TokenT; verifyUser?: boolean }
): Promise<GetTokensReturnT> => {
  const pageTokens = await (await browser.newContext()).newPage();

  await preTest(pageTokens, "/");

  const payload = genRegisterPayload();

  const res = await pageTokens.request.post(
    `${BASE_URL}/test/tokens-health?cbc_hmac_token_t=${tokenType}&verify_user=${verifyUser}`,
    { data: payload }
  );
  const data = await res.json();

  expect(REG_CBC_HMAC.test(data.cbc_hmac_token));

  return { ...data, page: pageTokens };
};
