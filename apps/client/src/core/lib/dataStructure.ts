export const isStr = (str: unknown): boolean =>
  typeof str === "string" && !!str.trim().length;
