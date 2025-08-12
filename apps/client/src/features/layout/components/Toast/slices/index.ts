// slices/toast.ts
import { AppEventT } from "@/common/types/api";
import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { StoreStateT } from "@/core/store";

export type ToastT = {
  msg: string;
  type: AppEventT;
};

export type ToastStateT = {
  isShow: boolean;
  toast: ToastT;
  seq: number;
};

const initState: ToastStateT = {
  isShow: false,
  toast: { msg: "", type: "" as AppEventT },
  seq: 0,
};

export const toastSlice = createSlice({
  name: "toast",
  initialState: initState,
  reducers: {
    open: (state, action: PayloadAction<ToastT>) => {
      state.isShow = true;
      state.toast = { ...action.payload };
      state.seq += 1;
    },
    close: (state) => {
      state.isShow = false;
    },
  },
});

export const getToastState = (state: StoreStateT) => state.toast;
