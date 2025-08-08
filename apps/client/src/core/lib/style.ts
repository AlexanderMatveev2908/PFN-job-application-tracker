import { uiBreaks } from "../constants/uiBreaks";

export const resp = (str: keyof typeof uiBreaks | number | undefined) =>
  !str
    ? ""
    : str in uiBreaks
    ? `@media screen and (min-width: ${
        uiBreaks[str as keyof typeof uiBreaks]
      }px)`
    : `@media screen and (min-width: ${str}px)`;
