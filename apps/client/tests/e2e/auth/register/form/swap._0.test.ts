import test from "@playwright/test";
import { checkTxtList } from "../../../lib/check";
import { checkTxtListOpc } from "../../../lib/style";
import { pre } from "./pre";
import { waitTest } from "../../../lib/sideActions";

test("swap 0", async ({ page }) => {
  const el = await pre(page);

  const firstName = el.getByTestId("first_name");
  const lastName = el.getByTestId("last_name");
  const email = el.getByTestId("email");

  await firstName.fill("<>!");
  await lastName.fill("...");
  await lastName.fill("");
  await email.fill("invalid@@@...");

  const msgs = ["invalid characters", "last name is required", "invalid email"];

  await waitTest(page);

  await checkTxtList(page, msgs);

  await firstName.fill("John");
  await lastName.fill("Doe");
  await email.fill("john@gmail.com");

  await waitTest(page);

  await checkTxtListOpc(page, msgs);
});
