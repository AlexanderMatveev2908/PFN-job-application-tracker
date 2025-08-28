import { SqlTableRoot } from "@/common/types/db";

export interface UserT extends SqlTableRoot {
  first_name: string;
  last_name: string;
  email: string;
  password?: string;
  confirm_password?: string;
  terms: boolean;
  totp_secret?: boolean;
  use_2FA: boolean;
}
