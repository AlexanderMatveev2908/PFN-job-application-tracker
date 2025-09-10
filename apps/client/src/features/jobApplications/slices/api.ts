import { ResApiT, TagAPI } from "@/common/types/api";
import { apiSlice } from "@/core/store/api";
import { JobApplicationT } from "../types";
import { jobApplicationsSlice } from "./slice";

const BASE = "/job-applications";

export const jobApplicationSliceAPI = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    addJobApplication: builder.mutation<
      ResApiT<{ job_application: JobApplicationT }>,
      FormData
    >({
      query: (data) => ({
        url: `${BASE}/`,
        method: "POST",
        data,
      }),

      invalidatesTags: [TagAPI.JOB_APPLICATIONS],
    }),

    readJobApplications: builder.query<
      ResApiT<{
        job_applications: JobApplicationT[];
        n_hits: number;
        pages: number;
      }>,
      string
    >({
      query: (data) => ({
        url: `${BASE}/?${data}`,
        method: "GET",
      }),

      providesTags: (res) => {
        return [
          ...(res?.job_applications?.length
            ? res.job_applications.map((el) => ({
                type: TagAPI.JOB_APPLICATIONS,
                id: el.id,
              }))
            : []),

          { type: TagAPI.JOB_APPLICATIONS, id: "LIST" },
        ];
      },

      async onQueryStarted(_, { dispatch, queryFulfilled }) {
        try {
          const {
            data: { n_hits, job_applications, pages },
          } = await queryFulfilled;

          dispatch(
            jobApplicationsSlice.actions.setData({
              n_hits,
              pages,
              job_applications,
            })
          );
        } catch {}
      },
    }),
  }),
});
