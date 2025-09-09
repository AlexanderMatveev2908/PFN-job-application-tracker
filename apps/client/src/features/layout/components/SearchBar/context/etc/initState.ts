export type SearchBarStateT = {
  bars: {
    filterBar: null | boolean;
    sortBar: null | boolean;
  };
  currFilter: string;
  pagination: {
    currBlock: number;
    currPage: number;
  };
};

export const searchBarInitState: SearchBarStateT = {
  bars: {
    filterBar: false,
    sortBar: null,
  },
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  currFilter: "" as any,
  pagination: {
    currBlock: 0,
    currPage: 0,
  },
};
