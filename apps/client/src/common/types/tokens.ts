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

export type CbcHmacTokenT = Exclude<TokenT, "REFRESH">;

export interface AadCbcHmacT {
  alg: string;
  token_id: string;
  token_t: TokenT;
  salt: string;
  user_id: string;
}
