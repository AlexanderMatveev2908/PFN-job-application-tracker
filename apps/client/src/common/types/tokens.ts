export type TokenT =
  | "REFRESH"
  | "CONF_EMAIL"
  | "RECOVER_PWD"
  | "RECOVER_PWD_2FA"
  | "CHANGE_EMAIL"
  | "CHANGE_EMAIL_2FA"
  | "CHANGE_PWD"
  | "MANAGE_ACC"
  | "LOGIN_2FA"
  | "MANAGE_ACC_2FA";

export interface AadCbcHmacT {
  alg: string;
  token_id: string;
  token_t: string;
  salt: string;
  user_id: string;
}
