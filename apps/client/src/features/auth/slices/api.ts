import { ResApiT } from "@/common/types/api";
import { apiSlice } from "@/core/store/api";
import { RegisterFormT } from "../pages/register/paperwork";
import { LoginFormT } from "../pages/login/paperwork";

const BASE = "/auth";

export type RegisterUserReturnT = { access_token: string };

export type LoginUserReturnT = {
  access_token?: string;
  cbc_hmac_token?: string;
};
export const authSliceAPI = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    registerUser: builder.mutation<ResApiT<RegisterUserReturnT>, RegisterFormT>(
      {
        query: (data) => ({
          url: `${BASE}/register`,
          method: "POST",
          data,
        }),
      }
    ),
    loginUser: builder.mutation<ResApiT<LoginUserReturnT>, LoginFormT>({
      query: (data) => ({
        url: `${BASE}/login`,
        method: "POST",
        data,
      }),
    }),
  }),
});
