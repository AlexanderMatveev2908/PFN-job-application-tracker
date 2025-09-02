import { ResApiT, TagAPI, UnwrappedResT } from "@/common/types/api";
import { apiSlice } from "@/core/store/api";
import { UserT } from "../types";
import { userSlice } from "./slice";
import { PwdFormT } from "@/core/paperwork";

const BASE = "/user";

export type GainAccessManageAccReturnT = {
  cbc_hmac_token: string;
};

export const userSliceAPI = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getProfile: builder.query<UnwrappedResT<{ user: UserT }>, void>({
      query: () => ({
        url: `${BASE}/profile`,
        method: "GET",
      }),
      providesTags: [TagAPI.USER],

      async onQueryStarted(_: undefined, { dispatch, queryFulfilled }) {
        try {
          const res = await queryFulfilled;

          dispatch(userSlice.actions.setUser(res.data.user));
        } catch {
          dispatch(userSlice.actions.setUser(null));
        }
      },
    }),

    gainAccessManageAcc: builder.mutation<
      ResApiT<GainAccessManageAccReturnT>,
      PwdFormT
    >({
      query: (data) => ({
        url: `${BASE}/manage-account`,
        method: "POST",
        data,
      }),
    }),
  }),
});
