export type PayloadSetBarT = {
  bar: "filterBar" | "sortBar";
  val: boolean | null;
};

export type SearchBarReducerActionsT =
  | {
      type: "SET_BAR";
      payload: PayloadSetBarT;
    }
  | {
      type: "SET_CURR_FILTER";
      payload: { val: string };
    };
