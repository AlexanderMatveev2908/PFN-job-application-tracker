/** @jsxImportSource @emotion/react */
"use client";

import { FieldValues } from "react-hook-form";
import AddFieldTxtDrop, {
  AddFieldTxtPropsType,
} from "./components/AddFieldTxtDrop";

type PropsType<T extends FieldValues> = {} & AddFieldTxtPropsType<T>;

const SecondaryRow = <T extends FieldValues>({
  existingFields,
  allowedTxtFields,
  append,
}: PropsType<T>) => {
  return (
    <div className="w-full grid grid-cols-2">
      <AddFieldTxtDrop
        {...{
          allowedTxtFields,
          append,
          existingFields,
        }}
      />
    </div>
  );
};

export default SecondaryRow;
