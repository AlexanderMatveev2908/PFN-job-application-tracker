export const searchBarInitState = {
  bars: {
    filterBar: false,
    sortBar: false,
  },
  currFilter: "",
};

export type SearchBarStateT = typeof searchBarInitState;
