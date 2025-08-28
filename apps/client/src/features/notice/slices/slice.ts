import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { AppEventT } from "@/common/types/api";
import { StoreStateT } from "@/core/store";

export type KeyCbT = "LOGIN";

export interface NoticeStateT {
  type: AppEventT;
  msg: string;
  keyCb: KeyCbT;
}

const initState: NoticeStateT = {
  type: "NONE",
  msg: "",
  keyCb: "" as KeyCbT,
};

export const noticeSlice = createSlice({
  name: "notice",
  initialState: initState,
  reducers: {
    setNotice: (state, action: PayloadAction<Partial<NoticeStateT>>) => {
      const { keyCb, msg, type } = action.payload;

      state.msg = msg ?? "";
      state.type = type ?? "NONE";
      state.keyCb = keyCb ?? ("" as KeyCbT);
    },
  },
});

export const getNoticeState = (state: StoreStateT) => state.notice;
