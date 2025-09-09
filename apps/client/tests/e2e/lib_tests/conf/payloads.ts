import { getDefValDatePicker } from "@/core/lib/dataStructure/formatters";
import { genLorem, pickRandom } from "@/core/lib/etc";
import { genPwd } from "@/core/lib/pwd";
import { ApplicationStatusT } from "@/features/jobApplications/types";
import { faker } from "@faker-js/faker";

export interface PayloadRegisterT {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
  confirm_password: string;
  terms: boolean;
}

export const genRegisterPayload = (): PayloadRegisterT => {
  const pwd = genPwd();

  return {
    first_name: faker.person.firstName(),
    last_name: faker.person.lastName(),
    email: faker.internet.email(),
    password: pwd,
    confirm_password: pwd,
    terms: true,
  };
};

export interface PayloadJobApplT {
  company_name: string;
  position_name: string;
  status: ApplicationStatusT;
  applied_at: string;
  notes?: string;
}

export const genPayloadJobAppl = (): PayloadJobApplT => ({
  company_name: faker.company.name(),
  position_name: faker.person.jobTitle(),
  applied_at: getDefValDatePicker(),
  status: pickRandom(Object.values(ApplicationStatusT)) as ApplicationStatusT,
  notes: genLorem(4),
});
