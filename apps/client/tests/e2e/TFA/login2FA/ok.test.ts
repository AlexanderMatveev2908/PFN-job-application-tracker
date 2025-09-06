import test, { expect } from "@playwright/test";
import { checkIsFocused, clickByID, getByID, isToastOk } from "../../lib/idx";
import { waitTmr, waitURL } from "../../lib/shortcuts/wait";
import { REG_JWT } from "@/core/constants/regex";
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { authenticator, totp } from "otplib";
import { preLogin2FA } from "./pre";
import { b32ToHex } from "@/core/lib/dataStructure";

test("login 2FA TOTP ok", async ({ browser }) => {
  const { page, totp_secret } = await preLogin2FA(browser);

  const form = await getByID(page, "totp_code__form");

  const firstSquare = await getByID(form, "totp_code.0");
  await firstSquare.click();

  await expect(firstSquare).toBeFocused();

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  totp.options = { encoding: "hex" as any };

  const code = totp.generate(b32ToHex(totp_secret));

  // const code = authenticator.generate(totp_secret);

  await page.evaluate((c) => navigator.clipboard.writeText(c), code);
  await page.keyboard.press("Control+V");

  await clickByID(form, "totp_code__form__submit");

  await waitURL(page, "/");
  await isToastOk(page);

  await expect(
    await page.evaluate(() => sessionStorage.getItem("access_token"))
  ).toMatch(REG_JWT);
});

test("login 2FA backup code ok", async ({ browser }) => {
  const { page, backup_codes } = await preLogin2FA(browser);

  await clickByID(page, "btns_swapper_next_swap");
  await waitTmr(page);

  const form = await getByID(page, "backup_code__form");
  const codeInput = await getByID(form, "backup_code");

  await checkIsFocused(codeInput);

  await codeInput.fill(backup_codes[0]);

  await clickByID(form, "backup_code__form__submit");

  await waitURL(page, "/");
  await isToastOk(page);

  await expect(
    await page.evaluate(() => sessionStorage.getItem("access_token"))
  ).toMatch(REG_JWT);
});
