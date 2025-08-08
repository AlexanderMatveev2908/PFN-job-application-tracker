import { useEffect } from "react";
import { FieldValues, Path, UseFormSetFocus } from "react-hook-form";
import { useWrapListener } from "./useWrapListener";

type Params<T extends FieldValues> = {
  setFocus: UseFormSetFocus<T>;
};

export const useFocus = <T extends FieldValues, K extends Path<T>>(
  path: K,
  { setFocus }: Params<T>
) => {
  const { wrapListener } = useWrapListener();

  useEffect(() => {
    const cb = () => setFocus(path);

    wrapListener(cb);
  }, [wrapListener, setFocus, path]);
};
