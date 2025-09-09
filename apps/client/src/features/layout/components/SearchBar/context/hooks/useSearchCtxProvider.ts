import { useCallback, useReducer } from "react";
import { searchBarInitState } from "../etc/initState";
import { searchbarReducer } from "../etc/reducer";
import { PayloadSetBarT } from "../etc/actions";

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

  return {
    ...state,
    setBar,
    setCurrFilter,
  };
};

export type SearchBarCtxT = ReturnType<typeof useSearchCtxProvider>;
