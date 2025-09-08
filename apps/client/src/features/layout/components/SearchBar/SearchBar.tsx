/** @jsxImportSource @emotion/react */
"use client";

import BtnShadow from "@/common/components/buttons/BtnShadow";
import Shim from "@/common/components/elements/Shim";
import FormFieldTxt from "@/common/components/forms/inputs/FormFieldTxt";
import { FormFieldTxtSearchBarT } from "@/common/types/ui";
import { useHydration } from "@/core/hooks/etc/hydration/useHydration";
import { logFormData, logFormErrs } from "@/core/lib/forms";
import { __cg } from "@/core/lib/log";
import { css } from "@emotion/react";
import { useEffect, type FC } from "react";
import { FieldValues, Path, useFormContext } from "react-hook-form";

type PropsType<T extends FieldValues> = {};

const SearchBar = <T extends FieldValues>({}: PropsType<T>) => {
  const { isHydrated } = useHydration();
  const {
    watch,
    control,
    formState: { errors },
    handleSubmit,
  } = useFormContext<T>();
  const fields: FormFieldTxtSearchBarT<T>[] = watch("txtFields" as Path<T>);

  const handleSave = handleSubmit(async (data) => {
    __cg(data);
  }, logFormErrs);

  const data = watch();

  useEffect(() => {
    console.log(data);
    console.log(errors);
  }, [data, errors]);

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
        <FormFieldTxt
          key={el.id}
          {...{
            control,
            el: {
              ...el,
              name: `txtFields.${i}.val` as Path<T>,
            },
          }}
        />
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
