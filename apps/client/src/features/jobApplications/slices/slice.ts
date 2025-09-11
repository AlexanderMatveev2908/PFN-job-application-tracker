import { StoreStateT } from "@/core/store";
import {
  createEntityAdapter,
  createSlice,
  PayloadAction,
} from "@reduxjs/toolkit";
import { JobApplicationT } from "../types";

const jobApplicationsAdapter = createEntityAdapter<JobApplicationT>();

const initState = jobApplicationsAdapter.getInitialState({
  n_hits: 0,
  pages: 0,
});

export type PayloadSetState = {
  n_hits: number;
  pages: number;
  job_applications: JobApplicationT[];
};

export const jobApplicationsSlice = createSlice({
  name: "jobApplications",
  initialState: initState,
  reducers: {
    addJob: jobApplicationsAdapter.addOne,
    delJob: jobApplicationsAdapter.removeOne,
    patchJob: jobApplicationsAdapter.updateOne,
    setJobs: jobApplicationsAdapter.setAll,

    setData: (state, action: PayloadAction<PayloadSetState>) => {
      const { job_applications, n_hits, pages } = action.payload;

      state.n_hits = n_hits;
      state.pages = pages;

      jobApplicationsAdapter.setAll(state, job_applications);
    },
  },
});

export const getJobApplicationsState = (state: StoreStateT) =>
  state.jobApplications;

export const jobsSelectors = jobApplicationsAdapter.getSelectors(
  (state: StoreStateT) => state.jobApplications
);

export const getJobList = jobsSelectors.selectAll;
