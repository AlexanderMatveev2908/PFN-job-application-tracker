export interface UserT {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  password?: string;
  confirm_password?: string;
  terms: boolean;
  totp_secret?: boolean;
  use_2FA: boolean;
}
