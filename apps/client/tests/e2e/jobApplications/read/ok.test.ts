import test from "@playwright/test";
import { preJobApplRead } from "./pre";

test("read job appl ok", async ({ browser }) => {
  const { page } = await preJobApplRead(browser);
});
