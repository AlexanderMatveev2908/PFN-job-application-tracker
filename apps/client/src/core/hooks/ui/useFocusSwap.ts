import { useEffect, useMemo } from "react";
import { SwapStateT } from "../etc/useSwap/etc/initState";
import { FieldValues, Path, UseFormSetFocus } from "react-hook-form";

type Params<T extends FieldValues> = {
  swapState: SwapStateT;
  kwargs: Path<T>[];
  setFocus: UseFormSetFocus<T>;
};

export const useFocusSwap = <T extends FieldValues>({
  swapState,
  kwargs,
  setFocus,
}: Params<T>) => {
  const saved = useMemo(() => kwargs, [kwargs]);

  useEffect(() => {
    if (swapState.swapMode === "swapped") setFocus(saved[swapState.currSwap]);
  }, [swapState, setFocus, saved]);
};
