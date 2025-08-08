import { AppEventT } from "@/common/types/api";
import { ToastStateT, ToastT } from "../types";
import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { v4 } from "uuid";
import { StoreStateT } from "@/core/store";

const initState: ToastStateT = {
  isShow: false,
  toast: { msg: "", type: "" as AppEventT },
  id: "",
};

export const toastSlice = createSlice({
  name: "toast",
  initialState: initState,
  reducers: {
    open: (state, action: PayloadAction<ToastT>) => {
      state.isShow = true;
      state.toast = action.payload;
      state.id = v4();
    },
    close: (state) => {
      state.isShow = false;
      state.id = "";
    },
    force: (state) => {
      // ? u already set state.toast above, is enough here just to trigger a rerender
      state.isShow = true;
      state.id = v4();
    },
  },
});

export const getToastState = (state: StoreStateT) => state.toast;
