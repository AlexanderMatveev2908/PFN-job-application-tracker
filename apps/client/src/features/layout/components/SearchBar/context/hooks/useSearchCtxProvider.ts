import { useCallback, useReducer } from "react";
import { searchBarInitState } from "../etc/initState";
import { searchbarReducer } from "../etc/reducer";
import { PayloadPaginationT, PayloadSetBarT } from "../etc/actions";

export const useSearchCtxProvider = () => {
  const [state, dispatchRct] = useReducer(searchbarReducer, searchBarInitState);

  const setBar = useCallback(
    (payload: PayloadSetBarT) => dispatchRct({ type: "SET_BAR", payload }),
    []
  );

  const setCurrFilter = useCallback(
    (payload: { val: string }) =>
      dispatchRct({ type: "SET_CURR_FILTER", payload }),
    []
  );

  const setPagination = useCallback(
    (payload: PayloadPaginationT) =>
      dispatchRct({ type: "SET_PAGINATION", payload }),
    []
  );

  return {
    ...state,
    setBar,
    setCurrFilter,
    setPagination,
  };
};

export type SearchBarCtxT = ReturnType<typeof useSearchCtxProvider>;
