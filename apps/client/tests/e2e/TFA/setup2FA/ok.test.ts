import test, { expect } from "@playwright/test";
import {
  clickByID,
  getAccessManageAccVerified,
  getByID,
  isToastOk,
} from "../../lib/idx";
import { waitTmr } from "../../lib/shortcuts/wait";

test("setup 2FA ok", async ({ browser }) => {
  const { swap, page } = await getAccessManageAccVerified(browser);

  await clickByID(swap, "setup_2FA__btn");

  await waitTmr(page);

  await isToastOk(page);

  const qrLk = await getByID(swap, "qr_code_resul");
  const zipBtn = await getByID(swap, "setup_2FA__link");

  const [imgFile] = await Promise.all([
    page.waitForEvent("download"),
    qrLk.click(),
  ]);

  await expect(imgFile.suggestedFilename()).toMatch(/^qrcode.*\.png$/);

  const [zipFile] = await Promise.all([
    page.waitForEvent("download"),
    zipBtn.click(),
  ]);

  await expect(zipFile.suggestedFilename()).toMatch(/^2FA.*\.zip$/);
});
