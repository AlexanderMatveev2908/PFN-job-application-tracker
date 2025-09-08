/** @jsxImportSource @emotion/react */
"use client";

import BtnSvg from "@/common/components/buttons/BtnSvg";
import { FormFieldTxtSearchBarT } from "@/common/types/ui";
import { FieldValues } from "react-hook-form";
import { FaPlus } from "react-icons/fa6";

type PropsType<T extends FieldValues> = {
  fields: FormFieldTxtSearchBarT<T>[];
};

const SecondaryRow = <T extends FieldValues>({ fields }: PropsType<T>) => {
  return (
    <div className="w-full grid grid-cols-2">
      <div className="w-[75px]">
        <BtnSvg
          {...{
            act: "INFO",
            Svg: FaPlus,
            confPortal: {
              txt: "Add Input",
              showPortal: true,
              optDep: [fields.length],
            },
          }}
        />
      </div>
    </div>
  );
};

export default SecondaryRow;
