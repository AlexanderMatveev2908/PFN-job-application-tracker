import { testSlice } from "@/features/test/slices/slice";
import { combineReducers, configureStore } from "@reduxjs/toolkit";
import { apiSlice } from "./api";
import { toastSlice } from "@/features/layout/components/Toast/slices";

const rootReducer = combineReducers({
  test: testSlice.reducer,
  apiApp: apiSlice.reducer,
  toast: toastSlice.reducer,
});

export const genStoreSSR = (
  preloadedState: Partial<ReturnType<typeof rootReducer>>
) =>
  configureStore({
    reducer: rootReducer,

    middleware: (getDefMdw) => getDefMdw().concat(apiSlice.middleware),
    preloadedState,
  });

export type StoreT = ReturnType<typeof genStoreSSR>;
export type StoreStateT = ReturnType<StoreT["getState"]>;
export type DispatchT = StoreT["dispatch"];
