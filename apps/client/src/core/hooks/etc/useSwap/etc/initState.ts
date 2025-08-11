export type SwapModeT = "swapped" | "swapping" | "none";

export interface SwapStateT {
  currSwap: number;
  swapMode: SwapModeT;
}

export const initState: SwapStateT = {
  currSwap: 0,
  swapMode: "none",
};

export type SwapActionsT =
  | {
      type: "START_SWAP";
      payload: number;
    }
  | {
      type: "END_SWAP";
    };
