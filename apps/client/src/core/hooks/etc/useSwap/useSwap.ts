import { clearTmr } from "@/core/lib/etc";
import { useCallback, useEffect, useReducer, useRef } from "react";
import { reducer } from "./etc/reducer";
import { initState, PayloadStartSwapT } from "./etc/initState";

export const useSwap = () => {
  const [state, dispatchRCT] = useReducer(reducer, initState);
  const timerID = useRef<NodeJS.Timeout | null>(null);

  const startSwap = useCallback(({ swap }: PayloadStartSwapT) => {
    dispatchRCT({ type: "START_SWAP", payload: { swap } });
  }, []);

  const endSwap = useCallback(() => {
    dispatchRCT({ type: "END_SWAP" });
  }, []);

  useEffect(() => {
    timerID.current = setTimeout(() => {
      endSwap();
      clearTmr(timerID);
    }, 400);

    return () => {
      clearTmr(timerID);
    };
  }, [state, endSwap]);

  return {
    swapState: state,
    startSwap,
    endSwap,
  };
};
