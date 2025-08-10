/** @jsxImportSource @emotion/react */
"use client";

import { FormFieldTxtT } from "@/common/types/ui";
import { FieldValues } from "react-hook-form";

type PropsType<T extends FieldValues> = {
  el: FormFieldTxtT<T>;
};

const FormFieldTxt = <T extends FieldValues>({ el }: PropsType<T>) => {
  return (
    <label className="w-full grid grid-cols-1 gap-4">
      {el.label && <span className="txt__lg">{el.label}</span>}
    </label>
  );
};

export default FormFieldTxt;
