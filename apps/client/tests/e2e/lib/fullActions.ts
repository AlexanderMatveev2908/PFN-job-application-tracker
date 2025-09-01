import { genMailNoticeMsg } from "@/core/constants/etc";
import { preAuthRegister } from "../auth/register/pre";
import { clickByID } from "./click";
import { getByID, getByTxt } from "./get";
import { waitTest, waitURL } from "./sideActions";
import { Browser, expect, Page } from "@playwright/test";
import { genRegisterPayload, PayloadRegisterT } from "./gen";
import { preAuthLogin } from "../auth/login/pre";
import { preTest } from "./pre";
import { instanceAxs } from "@/core/store/conf/baseQuery/axiosInstance";
import { REG_CBC_HMAC } from "@/core/constants/regex";
import { TokenT } from "@/common/types/tokens";
import { UserT } from "@/features/user/types";

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

  await waitTest(page);

  const pwd = await getByID(el, "password");
  await pwd.fill(payload.password);

  const confPwd = await getByID(el, "confirm_password");
  confPwd.fill(payload.password);

  await clickByID(el, "body__form_terms");

  await clickByID(el, "register__footer_form__submit_btn");

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

  await clickByID(el, "login__footer_form__submit_btn");

  await waitURL(loginPage, "/");

  await waitTest(loginPage);

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

  const { data } = await instanceAxs.post(
    `/test/tokens-health?cbc_hmac_token_t=${tokenType}&verify_user=${verifyUser}`,
    payload
  );

  expect(REG_CBC_HMAC.test(data.cbc_hmac_token));

  return data;
};
