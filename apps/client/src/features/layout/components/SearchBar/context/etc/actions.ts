export type PayloadSetBarT = {
  bar: "filterBar" | "sortBar";
  val: boolean | null;
};

export type PayloadPaginationT = { key: "currPage" | "currBlock"; val: number };

export type SearchBarReducerActionsT =
  | {
      type: "SET_BAR";
      payload: PayloadSetBarT;
    }
  | {
      type: "SET_CURR_FILTER";
      payload: { val: string };
    }
  | {
      type: "SET_PAGINATION";
      payload: PayloadPaginationT;
    };
