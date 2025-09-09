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
import { useCallback, useEffect } from "react";
import AddFieldTxtDrop from "./components/AddFieldTxtDrop";
import FilterBar from "./components/FilterBar/FilterBar";
import { FilterSearchBarT } from "./types";
import { useSearchCtxConsumer } from "./context/hooks/useSearchCtxConsumer";
import SortBar from "./components/SortBar/SortBar";

type PropsType<T extends FieldValues> = {
  allowedTxtFields: FormFieldTxtSearchBarT<T>[];
  resetVals: T;
  filters: FilterSearchBarT[];
};

const SearchBar = <T extends FieldValues>({
  allowedTxtFields,
  resetVals,
  filters,
}: PropsType<T>) => {
  const { isHydrated } = useHydration();
  const { watch, control, handleSubmit, reset } = useFormContext<T>();
  const existingFields: FormFieldTxtSearchBarT<T>[] =
    watch("txtFields" as Path<T>) ?? [];

  const { remove, append } = useFieldArray({
    control,
    name: "txtFields" as ArrayPath<T>,
  });

  const handleSave = handleSubmit(async (data) => {
    __cg(data);
  }, logFormErrs);

  const handleReset = useCallback(() => reset(resetVals), [reset, resetVals]);

  const { setCurrFilter } = useSearchCtxConsumer();

  useEffect(() => {
    setCurrFilter({ val: filters[0].label });
  }, [filters, setCurrFilter]);

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
      className="w-full max-w-[1400px] mx-auto h-fit min-h-[200px] border-3 border-w__0 rounded-xl p-5 grid grid-cols-1 gap-8"
    >
      <div className="w-full grid grid-cols-1 gap-6 relative">
        <PrimaryRow
          {...{ existingFields, remove, control, append, allowedTxtFields }}
        />
        <AddFieldTxtDrop
          {...{
            allowedTxtFields,
            append,
            existingFields,
          }}
        />
      </div>

      <div className="w-full grid grid-cols-1 gap-8 xl:grid-cols-2">
        <SecondaryRow />

        <TertiaryRow
          {...{
            handleReset,
          }}
        />
      </div>

      <FilterBar
        {...{
          handleReset,
          filters,
        }}
      />

      <SortBar />
    </form>
  );
};

export default SearchBar;
