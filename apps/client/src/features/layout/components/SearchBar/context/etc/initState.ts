export const searchBarInitState = {
  bars: {
    filterBar: false,
    sortBar: null,
  },
  currFilter: "",
};

export type SearchBarStateT = {
  bars: {
    filterBar: null | boolean;
    sortBar: null | boolean;
  };
  currFilter: "filterBar" | "sortBar";
};
