export const initState = {
  isCopied: false,
  id: "",
};

export type CpyPasteStateT = typeof initState;

export type CpyPasteActionsT =
  | {
      type: "OPEN";
    }
  | {
      type: "CLOSE";
    }
  | {
      type: "FORCE";
    };
