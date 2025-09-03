import { Browser } from "@playwright/test";
import { getTokensLib } from "./fullActions";
import { goPage } from "../shortcuts/go";
import { waitTmr, waitURL } from "../shortcuts/wait";
import { clickByID, getByID, getByTxt, isToastOk } from "../idx";
import { faker } from "@faker-js/faker";
import { genMailNoticeMsg } from "@/core/constants/etc";

export const getAccessManageAcc = async (browser: Browser) => {
  const { payload, page } = await getTokensLib(browser, {});

  await goPage(page, "/user/manage-account");

  await waitURL(page, "/user/access-manage-account");

  const form = await getByID(page, "manage_acc__form");

  const pwd = await getByID(form, "password");

  await pwd.fill(payload.password);
  await clickByID(form, "manage_acc__form__submit");

  await waitTmr(page);

  await waitURL(page, "/user/manage-account");

  await isToastOk(page);

  const container = await getByID(page, "manage_acc__form");

  return {
    payload,
    page,
    container,
  };
};
