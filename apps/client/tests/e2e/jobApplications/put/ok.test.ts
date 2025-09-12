/* eslint-disable @typescript-eslint/no-explicit-any */
import test, { expect } from "@playwright/test";
import {
  BASE_URL,
  clickByID,
  genPayloadJobAppl,
  getByID,
  getTokensLib,
} from "../../lib_tests/idx";
import { waitTmr, waitURL } from "../../lib_tests/shortcuts/wait";
import { JobApplicationT } from "@/features/jobApplications/types";

const relevantKeys = ["company_name", "position_name", "status"];

test("put appl ok", async ({ browser }) => {
  const { page, access_token } = await getTokensLib(browser, {});

  const originalPayload = genPayloadJobAppl();

  const resPost = await page.request.post(`${BASE_URL}/job-applications`, {
    data: originalPayload,
    headers: {
      authorization: `Bearer ${access_token}`,
    },
  });

  const { job_application } = (await resPost.json()) as {
    job_application: JobApplicationT;
  };

  for (const k of relevantKeys)
    await expect(
      (job_application as any)[k] === (originalPayload as any)[k]
    ).toBe(true);

  await page.goto(`/job-applications/put/${job_application.id}`);

  await waitTmr(page, 5000);

  const companyNameField = await getByID(page, "company_name");
  await expect(companyNameField).toHaveValue(job_application.company_name);

  const positionNameField = await getByID(page, "position_name");
  await expect(positionNameField).toHaveValue(job_application.position_name);

  const wrapBoxes = await getByID(page, "wrap_swap_boxes__application_status");
  const boxChosen = await getByID(
    wrapBoxes,
    `swap_boxes__${originalPayload.status}`
  );
  await expect(
    boxChosen.evaluate((el) => el.style.background === "var(--white__0)")
  ).toBeTruthy();

  const updatedPayload = genPayloadJobAppl();

  await companyNameField.fill(updatedPayload.company_name);
  await positionNameField.fill(updatedPayload.position_name);

  await clickByID(wrapBoxes, `swap_boxes__${updatedPayload.status}`);

  await waitTmr(page);

  await clickByID(page, "job_application__form__submit");

  await waitTmr(page, 10000);
  await waitURL(page, "/job-applications/read");
  await waitTmr(page, 10000);

  const cards = await page.getByTestId("job_appl__card");
  await expect((await cards.all()).length).toBe(1);

  const cardUpdated = await cards.nth(0);

  for (const k of relevantKeys)
    await expect(
      await (await getByID(cardUpdated, `card__${k}`)).innerText()
    ).toBe((updatedPayload as any)[k]);
});
