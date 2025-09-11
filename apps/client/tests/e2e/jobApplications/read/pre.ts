import { Browser } from "@playwright/test";
import { getTokensLib } from "../../lib_tests/idx";

export const preJobApplRead = async (browser: Browser) => {
  await getTokensLib(browser, {});
};
