import { TagAPI, UnwrappedResT } from "@/common/types/api";
import { apiSlice } from "@/core/store/api";
import { UserT } from "../types";
import { userSlice } from "./slice";

const BASE_URL = "/user";

export const userSliceAPI = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getProfile: builder.query<UnwrappedResT<{ user: UserT }>, void>({
      query: () => ({
        url: `${BASE_URL}/profile`,
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
  }),
});
