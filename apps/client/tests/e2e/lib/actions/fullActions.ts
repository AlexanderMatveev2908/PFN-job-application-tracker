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
  browser: Browser,
  payload: PayloadRegisterT = genRegisterPayload()
) => {
  const { form, page } = await preAuthRegister(browser);

  const firstName = await getByID(form, "first_name");
  firstName.fill(payload.first_name);

  const lastName = await getByID(form, "last_name");
  lastName.fill(payload.last_name);

  const email = await getByID(form, "email");
  email.fill(payload.email);

  await clickByID(form, "btns_swapper_next_swap");

  await waitTmr(page);

  const pwd = await getByID(form, "password");
  await pwd.fill(payload.password);

  const confPwd = await getByID(form, "confirm_password");
  confPwd.fill(payload.password);

  await clickByID(form, "body__form_terms");

  await clickByID(form, "register__form__submit");

  await waitURL(page, "/notice");

  await getByTxt(page, genMailNoticeMsg("to confirm the account"));

  return {
    payload,
  };
};

export const loginUserOk = async (browser: Browser) => {
  const payload = genRegisterPayload();

  await registerUserOk(browser, payload);

  const { page, form } = await preAuthLogin(browser);

  const email = await getByID(form, "email");
  email.fill(payload.email);

  const pwd = await getByID(form, "password");
  pwd.fill(payload.password);

  await clickByID(form, "login__form__submit");

  await waitURL(page, "/");

  await waitTmr(page);

  await getByTxt(page, "operation successful");

  return {
    payload,
    page,
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
  const page = await preTest(browser, "/");

  const payload = genRegisterPayload();

  const res = await page.request.post(
    `${BASE_URL}/test/tokens-health?cbc_hmac_token_t=${tokenType}&verify_user=${verifyUser}`,
    { data: payload }
  );
  const data = await res.json();

  expect(REG_CBC_HMAC.test(data.cbc_hmac_token));

  return { ...data, page: page };
};
