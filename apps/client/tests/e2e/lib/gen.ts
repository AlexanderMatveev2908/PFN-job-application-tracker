import { genPwd } from "@/core/lib/pwd";
import { faker } from "@faker-js/faker";

export interface PayloadRegisterT {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
}

export const genRegisterPayload = (): PayloadRegisterT => ({
  first_name: faker.person.firstName(),
  last_name: faker.person.lastName(),
  email: faker.internet.email(),
  password: genPwd(),
});
