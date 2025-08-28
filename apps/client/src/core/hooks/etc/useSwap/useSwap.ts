import { clearTmr } from "@/core/lib/etc";
import { useCallback, useEffect, useReducer, useRef } from "react";
import { reducer } from "./etc/reducer";
import { initState, PayloadStartSwapT } from "./etc/initState";
import { lockFocusCb } from "@/core/lib/style";
import { useFocusSwap } from "./subHooks/useFocusSwap";
import { FieldValues, Path, UseFormSetFocus } from "react-hook-form";

type Params<T extends FieldValues> = {
  kwargs: Path<T>[];
  setFocus: UseFormSetFocus<T>;
};

export const useSwap = <T extends FieldValues>(params: Params<T>) => {
  const [state, dispatchRCT] = useReducer(reducer, initState);
  const timerSwapMode = useRef<NodeJS.Timeout | null>(null);
  const lockFocusRef = useRef<boolean>(false);

  useFocusSwap({
    kwargs: params.kwargs,
    setFocus: params.setFocus,
    swapState: state,
    lockFocusRef,
  });

  const startSwap = useCallback(
    ({ swap, lockFocus }: PayloadStartSwapT & { lockFocus?: boolean }) => {
      dispatchRCT({ type: "START_SWAP", payload: { swap } });

      if (lockFocus) lockFocusCb(lockFocusRef);
    },
    []
  );

  const endSwap = useCallback(() => {
    dispatchRCT({ type: "END_SWAP" });
  }, []);

  useEffect(() => {
    if (state.swapMode !== "swapping") return;

    clearTmr(timerSwapMode);

    timerSwapMode.current = setTimeout(() => {
      endSwap();
      clearTmr(timerSwapMode);
    }, 400);

    return () => {
      clearTmr(timerSwapMode);
    };
  }, [state, endSwap]);

  return {
    swapState: state,
    startSwap,
    endSwap,
    lockFocusRef,
  };
};
