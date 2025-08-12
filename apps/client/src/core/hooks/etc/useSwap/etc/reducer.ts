import { __cg } from "@/core/lib/log";
import { SwapActionsT, SwapStateT } from "./initState";

export const reducer = (
  state: SwapStateT,
  action: SwapActionsT
): SwapStateT => {
  switch (action.type) {
    case "START_SWAP": {
      const { swap, manualFocus } = action.payload;

      return {
        currSwap: swap,
        swapMode: "swapping",
        manualFocus: !!manualFocus,
      };
    }

    case "END_SWAP":
      return {
        ...state,
        swapMode: action?.payload ?? "swapped",
      };

    case "RESET_FOCUS":
      return {
        ...state,
        manualFocus: false,
      };

    default:
      __cg("Invalid action", action);
      throw new Error("Invalid action 😡");
  }
};
