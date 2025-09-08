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
import PrimaryRow from "./components/PrimaryRow";
import SecondaryRow from "./components/SecondaryRow";
import { FaSearch } from "react-icons/fa";
import { resp } from "@/core/lib/style";
import TertiaryRow from "./components/TertiaryRow";

type PropsType<T extends FieldValues> = {};

const SearchBar = <T extends FieldValues>({}: PropsType<T>) => {
  const { isHydrated } = useHydration();
  const { watch, control, handleSubmit } = useFormContext<T>();
  const fields: FormFieldTxtSearchBarT<T>[] =
    watch("txtFields" as Path<T>) ?? [];

  const { remove } = useFieldArray({
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
      className="w-full max-w-[1200px] mx-auto h-fit min-h-[200px] border-3 border-w__0 rounded-xl p-5 grid grid-cols-1 gap-8"
    >
      <PrimaryRow {...{ fields, remove, control }} />

      <SecondaryRow
        {...{
          fields,
        }}
      />

      <TertiaryRow />
    </form>
  );
};

export default SearchBar;
