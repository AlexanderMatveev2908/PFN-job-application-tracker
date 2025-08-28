import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { AppEventT } from "@/common/types/api";
import { StoreStateT } from "@/core/store";

interface NoticeStateT {
  type: AppEventT;
  msg: string;
  keyCb: string;
}

const initState: NoticeStateT = {
  type: "NONE",
  msg: "",
  keyCb: "",
};

export const noticeSlice = createSlice({
  name: "notice",
  initialState: initState,
  reducers: {
    setNotice: (_, action: PayloadAction<NoticeStateT>) => action.payload,
  },
});

export const getNoticeState = (state: StoreStateT) => state.notice;
