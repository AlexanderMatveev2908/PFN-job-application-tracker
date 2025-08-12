export type SwapModeT = "swapped" | "swapping" | "none";

export interface SwapStateT {
  currSwap: number;
  swapMode: SwapModeT;
  manualFocus: boolean;
}

export const initState: SwapStateT = {
  currSwap: 0,
  swapMode: "none",
  manualFocus: false,
};

export type PayloadStartSwapT = { swap: number; manualFocus?: boolean };

export type SwapActionsT =
  | {
      type: "START_SWAP";
      payload: PayloadStartSwapT;
    }
  | {
      type: "END_SWAP";
      payload?: SwapModeT;
    };
