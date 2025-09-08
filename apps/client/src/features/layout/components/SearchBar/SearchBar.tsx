/** @jsxImportSource @emotion/react */
"use client";

import Shim from "@/common/components/elements/Shim";
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
import TertiaryRow from "./components/TertiaryRow";

type PropsType<T extends FieldValues> = {
  allowedTxtFields: FormFieldTxtSearchBarT<T>[];
};

const SearchBar = <T extends FieldValues>({
  allowedTxtFields,
}: PropsType<T>) => {
  const { isHydrated } = useHydration();
  const { watch, control, handleSubmit } = useFormContext<T>();
  const existingFields: FormFieldTxtSearchBarT<T>[] =
    watch("txtFields" as Path<T>) ?? [];

  const { remove, append } = useFieldArray({
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
      <PrimaryRow {...{ fields: existingFields, remove, control }} />

      <SecondaryRow
        {...{
          existingFields,
          allowedTxtFields,
          append,
        }}
      />

      <TertiaryRow />
    </form>
  );
};

export default SearchBar;
