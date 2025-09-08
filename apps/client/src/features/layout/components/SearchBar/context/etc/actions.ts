export type SearchBarActionsT = "SET_BAR";

export type PayloadSetBarT = { bar: "filterBar" | "sortBar"; val: boolean };

export type SearchBarReducerActionsT = {
  payload: PayloadSetBarT;
  type: "SET_BAR";
};
