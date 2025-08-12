import { __cg } from "@/core/lib/log";
import { CpyPasteActionsT, CpyPasteStateT, initState } from "./initState";
import { v4 } from "uuid";

export const reducer = (
  _: CpyPasteStateT,
  action: CpyPasteActionsT
): CpyPasteStateT => {
  switch (action.type) {
    case "OPEN":
      return {
        id: v4(),
        isCopied: true,
      };

    case "CLOSE":
      return initState;

    case "FORCE":
      return {
        id: v4(),
        isCopied: true,
      };

    default:
      __cg("invalid action", action);

      throw new Error("Invalid action 😡");
  }
};
