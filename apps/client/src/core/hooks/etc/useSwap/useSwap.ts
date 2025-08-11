import { clearTmr } from "@/core/lib/etc";
import { useCallback, useEffect, useReducer, useRef } from "react";
import { reducer } from "./etc/reducer";
import { initState } from "./etc/initState";

export const useSwap = () => {
  const [state, dispatchRCT] = useReducer(reducer, initState);
  const timerID = useRef<NodeJS.Timeout | null>(null);

  const startSwap = useCallback((val: number) => {
    dispatchRCT({ type: "START_SWAP", payload: val });
  }, []);

  const endSwap = useCallback(() => {
    dispatchRCT({ type: "END_SWAP" });
  }, []);

  useEffect(() => {
    timerID.current = setTimeout(() => {
      endSwap();
      clearTmr(timerID);
    }, 100);

    return () => {
      clearTmr(timerID);
    };
  }, [state.currSwap, endSwap]);

  return {
    swapState: state,
    startSwap,
    endSwap,
  };
};
