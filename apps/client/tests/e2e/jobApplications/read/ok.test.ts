import test, { expect } from "@playwright/test";
import { preJobApplRead } from "./pre";
import { clickByID, getByID } from "../../lib_tests/idx";
import { waitTmr } from "../../lib_tests/shortcuts/wait";
import { ApplicationStatusT } from "@/features/jobApplications/types";

test("read job appl filter by text inputs ok", async ({ browser }) => {
  const { searchBar, applications, page } = await preJobApplRead(browser);

  const [firstAppl] = applications;

  await (
    await getByID(searchBar, "primary_row__company_name")
  ).fill(firstAppl.company_name);

  const rowDrop = await getByID(searchBar, "search_bar__drop_row");
  await clickByID(rowDrop, "drop_row__btn");

  await waitTmr(page);

  const drop = await getByID(rowDrop, "drop_row__txt_fields");

  await clickByID(drop, `txt_fields__position_name`);

  const positionNameField = await getByID(
    searchBar,
    "primary_row__position_name"
  );

  await positionNameField.fill(firstAppl.position_name);

  await waitTmr(page, 5000);

  const cardsByTxt = await page.getByTestId("job_appl__card");
  const countByTxt = await cardsByTxt.count();

  await expect(countByTxt >= 1).toBeTruthy();

  let found = false;
  for (const c of await cardsByTxt.all()) {
    try {
      const companyName = await getByID(c, "card__company_name");
      await expect(firstAppl.company_name).toBe(await companyName.innerText());
      const positionName = await getByID(c, "card__position_name");
      await expect(firstAppl.position_name).toBe(
        await positionName.innerText()
      );

      found = true;
      break;
    } catch {}
  }

  await expect(found).toBe(true);
});

test("read job appl filter by status checkbox ok", async ({ browser }) => {
  const { searchBar, applications, page } = await preJobApplRead(browser);

  await clickByID(searchBar, "search_bar__btn__filterBar");
  await waitTmr(page);

  const filterBar = await getByID(page, "search_bar__filter_bar");
  const filterBarBodyVals = await getByID(
    await getByID(filterBar, "filter_bar__body"),
    "body__vals"
  );

  await clickByID(filterBar, "search_bar__btn__close_filter_bar");
  await waitTmr(page);

  for (const status of Object.values(ApplicationStatusT)) {
    await clickByID(searchBar, "tertiary_row__reset");

    await clickByID(searchBar, "search_bar__btn__filterBar");
    await waitTmr(page);

    await clickByID(filterBarBodyVals, `body__vals__${status}`);

    await clickByID(filterBar, "search_bar__btn__close_filter_bar");

    await waitTmr(page, 5000);

    const cardsByStatus = await page.getByTestId("job_appl__card");
    const countByStatus = await cardsByStatus.count();

    await expect(countByStatus).toBe(
      applications.filter((el) => el.status === status).length
    );
  }
});

test("read job appl sort by applied_at ok", async ({ browser }) => {
  const { searchBar, applications, page, spanHits } = await preJobApplRead(
    browser
  );

  await clickByID(searchBar, "search_bar__btn__sortBar");
  await waitTmr(page);

  const sortBar = await getByID(page, "search_bar__sort_bar");

  await clickByID(sortBar, "sort_bar__applied_at_sort__ASC");

  await clickByID(sortBar, "btn__close_popup");

  await waitTmr(page, 5000);

  const cardsSortedByApplDate = await page.getByTestId("job_appl__card");
  await expect(await spanHits.innerText()).toBe("5");

  const sorted = applications.sort((a, b) => a.applied_at - b.applied_at);

  let i = 0;
  while (i < 5) {
    const curr = await cardsSortedByApplDate.nth(i);

    await expect(
      await (await getByID(curr, "card__company_name")).innerText()
    ).toBe(sorted[i].company_name);

    await expect(
      await (await getByID(curr, "card__position_name")).innerText()
    ).toBe(sorted[i].position_name);

    await expect(await (await getByID(curr, "card__status")).innerText()).toBe(
      sorted[i].status
    );

    i++;
  }
});
