/** @jsxImportSource @emotion/react */
"use client";

import BtnSvg from "@/common/components/buttons/BtnSvg";
import FormFieldTxt from "@/common/components/forms/inputs/FormFieldTxt";
import {
  Control,
  FieldValues,
  Path,
  UseFieldArrayRemove,
} from "react-hook-form";
import { MdDelete } from "react-icons/md";
import { FormFieldTxtSearchBarT } from "@/common/types/ui";

type PropsType<T extends FieldValues> = {
  control: Control<T>;
  remove: UseFieldArrayRemove;
  existingFields: FormFieldTxtSearchBarT<T>[];
};

const PrimaryRow = <T extends FieldValues>({
  remove,
  control,
  existingFields,
}: PropsType<T>) => {
  return existingFields.map((el, i, arg) => (
    <div key={el.id} className="w-full relative">
      <FormFieldTxt
        {...{
          control,
          el: {
            ...el,
            name: `txtFields.${i}.val` as Path<T>,
          },
          showLabel: false,
        }}
      />

      <div className="w-[50px] h-[50px] absolute -top-[20px] -right-[10px]">
        <BtnSvg
          {...{
            Svg: MdDelete,
            act: "ERR",
            handleClick: () => remove(i),
            confPortal: {
              showPortal: true,
              txt: `Remove`,
              optDep: [arg.length],
            },
          }}
        />
      </div>
    </div>
  ));
};

export default PrimaryRow;
