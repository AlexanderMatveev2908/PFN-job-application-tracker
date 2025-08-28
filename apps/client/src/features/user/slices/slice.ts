import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { UserT } from "../types";
import { StoreStateT } from "@/core/store";
import { getStorage } from "@/core/lib/storage";

export interface UserStateT {
  canManageAccount: boolean;
  access_token: string;
  cbc_hmac_token: string;
  user: UserT | null;
}

const initState: UserStateT = {
  canManageAccount: false,
  access_token: getStorage("access_token") ?? "",
  cbc_hmac_token: "",
  user: null,
};

export const userSlice = createSlice({
  name: "user",
  initialState: initState,
  reducers: {
    login: (state, action: PayloadAction<{ access_token: string }>) => {
      state.access_token = action.payload.access_token;
    },
    setUser: (state, action: PayloadAction<UserT>) => {
      state.user = action.payload;
    },
    logout: () => initState,
  },
});

export const getUserState = (state: StoreStateT) => state.user;
