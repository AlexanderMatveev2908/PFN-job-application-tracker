import { useCallback, useReducer, useRef } from "react";
import { searchBarInitState } from "../etc/initState";
import { searchbarReducer } from "../etc/reducer";
import {
  PayloadPaginationT,
  PayloadPendingT,
  PayloadSetBarT,
} from "../etc/actions";

export const useSearchCtxProvider = <T>() => {
  const [state, dispatchRct] = useReducer(searchbarReducer, searchBarInitState);
  const prevForm = useRef<T | null>(null);

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

  const setPending = useCallback(
    (payload: PayloadPendingT) => dispatchRct({ type: "SET_PENDING", payload }),
    []
  );

  return {
    ...state,
    setBar,
    setCurrFilter,
    setPagination,
    setPending,
    prevForm,
  };
};

export type SearchBarCtxT = ReturnType<typeof useSearchCtxProvider>;
