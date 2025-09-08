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

  return {
    ...state,
    setBar,
  };
};

export type SearchBarCtxT = ReturnType<typeof useSearchCtxProvider>;
