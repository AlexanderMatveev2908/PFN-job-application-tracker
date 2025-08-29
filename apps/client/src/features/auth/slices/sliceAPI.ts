import { UnwrappedResApiT } from "@/common/types/api";
import { apiSlice } from "@/core/store/api";
import { RegisterFormT } from "../pages/register/schemas/register";

const BASE = "/auth";

export type RegisterUserReturnT = { access_token: string };

export const authSliceAPI = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    registerUser: builder.mutation<
      UnwrappedResApiT<RegisterUserReturnT>,
      RegisterFormT
    >({
      query: (data) => ({
        url: `${BASE}/register`,
        method: "POST",
        data,
      }),
    }),
  }),
});
