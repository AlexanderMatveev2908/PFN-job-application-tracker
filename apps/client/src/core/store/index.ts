import { testSlice } from "@/features/test/slices/slice";
import { combineReducers, configureStore } from "@reduxjs/toolkit";
import { apiSlice } from "./api";
import { toastSlice } from "@/features/layout/components/Toast/slices";
import { sideSlice } from "@/features/layout/components/Sidebar/slice";
import { noticeSlice } from "@/features/notice/slices/slice";
import { userSlice } from "@/features/user/slices/slice";

const rootReducer = combineReducers({
  test: testSlice.reducer,
  apiApp: apiSlice.reducer,
  toast: toastSlice.reducer,
  side: sideSlice.reducer,
  notice: noticeSlice.reducer,
  user: userSlice.reducer,
});

export const genStoreSSR = (
  preloadedState: Partial<ReturnType<typeof rootReducer>>
) =>
  configureStore({
    reducer: rootReducer,

    middleware: (getDefMdw) => getDefMdw().concat(apiSlice.middleware),
    preloadedState,
  });

type StoreT = ReturnType<typeof genStoreSSR>;
export type StoreStateT = ReturnType<StoreT["getState"]>;
export type DispatchT = StoreT["dispatch"];
