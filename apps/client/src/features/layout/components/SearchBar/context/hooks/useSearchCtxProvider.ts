import { useCallback, useReducer, useRef } from "react";
import { searchBarInitState } from "../etc/initState";
import { searchbarReducer } from "../etc/reducer";
import {
  PayloadPaginationT,
  PayloadPendingT,
  PayloadSearchAPIT,
  PayloadSetBarT,
} from "../etc/actions";
import { genURLSearchQuery } from "@/core/lib/forms";
import { useWrapAPI } from "@/core/hooks/api/useWrapAPI";
import { TriggerApiT } from "@/common/types/api";
import { cpyObj } from "@/core/lib/dataStructure/ect";

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

  const setSearchApi = useCallback(
    (payload: PayloadSearchAPIT) => dispatchRct({ type: "SET_API", payload }),
    []
  );

  const triggerSearch = useCallback(
    async (arg: {
      freshData: T;
      triggerRTK: TriggerApiT<T>;
      keyPending: "submit" | "reset";
      skipCall?: boolean;
    }) => {
      setPending({ key: arg.keyPending, val: true });

      setSearchApi({ key: "skipCall", val: !!arg.skipCall });

      prevData.current = cpyObj(arg.freshData);

      await wrapAPI({
        cbAPI: () => arg.triggerRTK(genURLSearchQuery(arg.freshData)),
      });
    },
    [wrapAPI, setPending, setSearchApi]
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
