import { RefObject, useEffect, useMemo } from "react";
import { SwapStateT } from "../etc/useSwap/etc/initState";
import { FieldValues, Path, UseFormSetFocus } from "react-hook-form";

type Params<T extends FieldValues> = {
  swapState: SwapStateT;
  kwargs: Path<T>[];
  setFocus: UseFormSetFocus<T>;
  lockFocusRef?: RefObject<boolean>;
};

export const useFocusSwap = <T extends FieldValues>({
  swapState,
  kwargs,
  setFocus,
  lockFocusRef,
}: Params<T>) => {
  // ! do not pass dynamic variables
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const saved = useMemo(() => kwargs, []);

  useEffect(() => {
    if (swapState.swapMode === "swapped" && !lockFocusRef?.current)
      setFocus(saved[swapState.currSwap]);
  }, [swapState.currSwap, swapState.swapMode, setFocus, saved, lockFocusRef]);
};
