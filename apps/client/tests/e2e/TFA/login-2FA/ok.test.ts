import test, { expect } from "@playwright/test";
import {
  clickByID,
  getByID,
  getByTxt,
  getUser2FA,
  isToastOk,
  preTest,
} from "../../lib/idx";
import { waitURL } from "../../lib/shortcuts/wait";
import { REG_JWT } from "@/core/constants/regex";
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { authenticator, totp } from "otplib";
import base32Decode from "base32-decode";

test("login 2FA ok", async ({ browser }) => {
  const { payload, totp_secret } = await getUser2FA(browser, {});

  const page = await preTest(browser, "/auth/login");

  const formLogin = await getByID(page, "login__form");

  await (await getByID(formLogin, "email")).fill(payload.email);
  await (await getByID(formLogin, "password")).fill(payload.password);

  await clickByID(formLogin, "login__form__submit");

  await waitURL(page, "/auth/login-2FA");

  const form2FA = await getByID(page, "2FA__form");

  await getByTxt(form2FA, "totp code");

  const firstSquare = await getByID(form2FA, "totp_code.0");
  await firstSquare.click();

  await expect(firstSquare).toBeFocused();

  const hexSecret = Buffer.from(base32Decode(totp_secret, "RFC4648")).toString(
    "hex"
  );

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  totp.options = { encoding: "hex" as any };

  const code = totp.generate(hexSecret);

  // const code = authenticator.generate(totp_secret);

  await page.evaluate((c) => navigator.clipboard.writeText(c), code);
  await page.keyboard.press("Control+V");

  await clickByID(form2FA, "totp_code__form__submit");

  await waitURL(page, "/");
  await isToastOk(page);

  await expect(
    await page.evaluate(() => sessionStorage.getItem("access_token"))
  ).toMatch(REG_JWT);
});
