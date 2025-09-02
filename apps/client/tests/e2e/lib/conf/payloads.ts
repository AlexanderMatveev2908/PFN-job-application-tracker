import { genPwd } from "@/core/lib/pwd";
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
