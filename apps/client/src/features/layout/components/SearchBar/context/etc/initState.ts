import { getNumCardsForPage } from "../../sideComponents/PageCounter/uiFactory";

export type SearchBarStateT = {
  bars: {
    filterBar: null | boolean;
    sortBar: null | boolean;
  };
  currFilter: string;
  pagination: {
    currBlock: number;
    currPage: number;
    limit: number;
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
    limit: getNumCardsForPage(),
  },
};
