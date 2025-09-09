export type SearchBarStateT = {
  bars: {
    filterBar: null | boolean;
    sortBar: null | boolean;
  };
  currFilter: string;
};

export const searchBarInitState: SearchBarStateT = {
  bars: {
    filterBar: false,
    sortBar: null,
  },
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  currFilter: "" as any,
};
