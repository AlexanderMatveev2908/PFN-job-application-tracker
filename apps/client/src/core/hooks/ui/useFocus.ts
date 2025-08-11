import { useEffect } from "react";
import { FieldValues, Path, UseFormSetFocus } from "react-hook-form";
import { useWrapListener } from "../etc/useWrapListener";

type Params<T extends FieldValues> = {
  setFocus: UseFormSetFocus<T>;
};

export const useFocus = <T extends FieldValues, K extends Path<T>>(
  path: K,
  { setFocus }: Params<T>
) => {
  const { wrapListener } = useWrapListener();

  useEffect(() => {
    const cb = () =>
      setTimeout(() => {
        setFocus(path);
      }, 250);

    wrapListener(cb);
  }, [wrapListener, setFocus, path]);
};
