import { useEffect } from "react";
import { FieldValues, Path, UseFormSetFocus } from "react-hook-form";
import { useWrapClientListener } from "../etc/useWrapClientListener";

type Params<T extends FieldValues> = {
  setFocus: UseFormSetFocus<T>;
};

export const useFocus = <T extends FieldValues, K extends Path<T>>(
  path: K,
  { setFocus }: Params<T>
) => {
  const { wrapClientListener } = useWrapClientListener();

  useEffect(() => {
    const cb = () =>
      setTimeout(() => {
        setFocus(path);
      }, 250);

    wrapClientListener(cb);
  }, [wrapClientListener, setFocus, path]);
};
