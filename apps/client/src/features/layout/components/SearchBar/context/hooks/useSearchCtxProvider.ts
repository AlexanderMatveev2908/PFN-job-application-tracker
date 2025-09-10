import { useCallback, useReducer, useRef } from "react";
import { searchBarInitState } from "../etc/initState";
import { searchbarReducer } from "../etc/reducer";
import {
  PayloadPaginationT,
  PayloadPendingT,
  PayloadSetBarT,
} from "../etc/actions";
import { genURLSearchQuery } from "@/core/lib/forms";
import { useWrapAPI } from "@/core/hooks/api/useWrapAPI";
import { TriggerApiT } from "@/common/types/api";

export const useSearchCtxProvider = <T>() => {
  const [state, dispatchRct] = useReducer(searchbarReducer, searchBarInitState);
  const prevData = useRef<T | null>(null);

  const { wrapAPI } = useWrapAPI();

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

  const triggerSearch = useCallback(
    async (arg: {
      freshData: T;
      triggerRTK: TriggerApiT<T>;
      keyPending: "submit" | "reset";
    }) => {
      setPending({ key: arg.keyPending, val: true });

      prevData.current = arg.freshData;

      await wrapAPI({
        cbAPI: () => arg.triggerRTK(genURLSearchQuery(arg.freshData)),
      });
    },
    [wrapAPI, setPending]
  );

  return {
    ...state,
    setBar,
    setCurrFilter,
    setPagination,
    setPending,
    prevData,
    triggerSearch,
  };
};

export type SearchBarCtxT = ReturnType<typeof useSearchCtxProvider>;
