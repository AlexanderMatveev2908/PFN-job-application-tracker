/** @jsxImportSource @emotion/react */
"use client";

import { FormFieldCheckT } from "@/common/types/ui";
import {
  FieldErrors,
  FieldValues,
  Path,
  UseFormSetValue,
} from "react-hook-form";
import MiniCheckBox from "./components/MiniCheckBox";
import ErrField from "../../etc/ErrField";

type PropsType<T extends FieldValues> = {
  el: FormFieldCheckT<T>;
  showLabel?: boolean;
  isChecked: boolean;
  errors: FieldErrors<T>;
  setValue: UseFormSetValue<T>;
  manualErr?: string;
  optTxt?: string;
};

const FormFieldCheck = <T extends FieldValues>({
  el,
  showLabel = true,
  isChecked,
  setValue,
  optTxt,
  errors,
  manualErr,
}: PropsType<T>) => {
  const handleChange = () => {
    setValue(el.name, !isChecked as T[Path<T>], {
      shouldValidate: true,
    });
  };

  const msg = manualErr ?? (errors?.[el.name]?.message as string);

  return (
    <div className="w-full grid grid-cols-1 gap-4">
      {showLabel && <span className="txt__lg">{el.label}</span>}

      <div className="w-fit flex items-center gap-6 relative">
        <label
          className="w-[40px] h-[40px] relative cursor-pointer"
          onClick={handleChange}
        >
          <MiniCheckBox
            {...{
              isChecked,
            }}
          />
        </label>

        <ErrField
          {...{
            msg,
          }}
        />

        <span className="txt__md">{optTxt}</span>
      </div>
    </div>
  );
};

export default FormFieldCheck;
