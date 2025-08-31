import { ResApiT } from "@/common/types/api";
import { apiSlice } from "@/core/store/api";
import { RegisterFormT } from "../pages/register/paperwork";

const BASE = "/auth";

export type RegisterUserReturnT = { access_token: string };

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
  }),
});
