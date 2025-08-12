import { FieldErrors, FieldValues, Path } from "react-hook-form";

export const swapOnErr = <T extends FieldValues>({
  errs,
  kwargs,
}: {
  kwargs: Path<T>[][];
  errs: FieldErrors<T>;
}): { i: number; field: Path<T> } | undefined => {
  let i = 0;

  while (i < kwargs.length) {
    const curr = kwargs[i];

    for (const field of curr) {
      if (errs?.[field]?.message) {
        return { i, field };
      }
    }

    i++;
  }
};
