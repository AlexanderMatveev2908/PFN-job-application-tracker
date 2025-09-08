/** @jsxImportSource @emotion/react */
"use client";

import BtnShadow from "@/common/components/buttons/BtnShadow";
import BtnSvg from "@/common/components/buttons/BtnSvg";
import Shim from "@/common/components/elements/Shim";
import FormFieldTxt from "@/common/components/forms/inputs/FormFieldTxt";
import { FormFieldTxtSearchBarT } from "@/common/types/ui";
import { useHydration } from "@/core/hooks/etc/hydration/useHydration";
import { logFormErrs } from "@/core/lib/forms";
import { __cg } from "@/core/lib/log";
import { css } from "@emotion/react";
import {
  ArrayPath,
  FieldValues,
  Path,
  useFieldArray,
  useFormContext,
} from "react-hook-form";
import { MdDelete } from "react-icons/md";

type PropsType<T extends FieldValues> = {};

const SearchBar = <T extends FieldValues>({}: PropsType<T>) => {
  const { isHydrated } = useHydration();
  const { watch, control, handleSubmit } = useFormContext<T>();
  const fields: FormFieldTxtSearchBarT<T>[] =
    watch("txtFields" as Path<T>) ?? [];

  const { append, remove } = useFieldArray({
    control,
    name: "txtFields" as ArrayPath<T>,
  });
  const handleSave = handleSubmit(async (data) => {
    __cg(data);
  }, logFormErrs);

  return !isHydrated ? (
    <Shim
      {...{
        $CSS: css`
          width: 95%;
          max-width: 1200px;
          height: 200px;
        `,
      }}
    />
  ) : (
    <form
      onSubmit={handleSave}
      className="w-full max-w-[1200px] h-fit min-h-[200px] border-3 border-w__0 rounded-xl p-5 grid grid-cols-1 gap-10"
    >
      {fields.map((el, i) => (
        <div key={el.id} className="w-full relative">
          <FormFieldTxt
            {...{
              control,
              el: {
                ...el,
                name: `txtFields.${i}.val` as Path<T>,
              },
            }}
          />

          <div className="w-[50px] h-[50px] absolute top-[20px] -right-[10px]">
            <BtnSvg
              {...{
                Svg: MdDelete,
                act: "ERR",
                handleClick: () => remove(i),
                confPortal: {
                  showPortal: true,
                  txt: `Remove`,
                  optDep: [fields.length],
                },
              }}
            />
          </div>
        </div>
      ))}

      <div className="w-[250px]">
        <BtnShadow
          {...{
            act: "OK",
            el: {
              label: "Search",
            },
            type: "submit",
          }}
        />
      </div>
    </form>
  );
};

export default SearchBar;
