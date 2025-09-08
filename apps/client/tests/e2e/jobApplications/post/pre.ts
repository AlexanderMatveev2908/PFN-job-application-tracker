import { Browser } from "@playwright/test";
import { genPayloadJobAppl, getByID, getTokensLib } from "../../lib_tests/idx";
import { waitTmr } from "../../lib_tests/shortcuts/wait";

export const preJobAppl = async (browser: Browser) => {
  const { page, ...rst } = await getTokensLib(browser, {});

  await page.goto("/job-applications/post");
  await waitTmr(page);

  const form = await getByID(page, "job_application__form");

  const payload = genPayloadJobAppl();

  return {
    ...rst,
    page,
    payload,
    form,
  };
};
