import { __cg } from "@/core/lib/log";
import { SwapActionsT, SwapStateT } from "./initState";

export const reducer = (
  state: SwapStateT,
  action: SwapActionsT
): SwapStateT => {
  switch (action.type) {
    case "START_SWAP":
      return {
        currSwap: action.payload,
        swapMode: "swapping",
      };

    case "END_SWAP":
      return {
        ...state,
        swapMode: "swapped",
      };

    default:
      __cg("Invalid action", action);
      throw new Error("Invalid action 😡");
  }
};
