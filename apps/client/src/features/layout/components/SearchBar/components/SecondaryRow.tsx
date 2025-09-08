/** @jsxImportSource @emotion/react */
"use client";

import BtnSvg from "@/common/components/buttons/BtnSvg";
import { FormFieldTxtSearchBarT } from "@/common/types/ui";
import { useMouseOut } from "@/core/hooks/etc/useMouseOut";
import { css } from "@emotion/react";
import { useMemo, useRef, useState } from "react";
import { FieldValues, Path, UseFieldArrayAppend } from "react-hook-form";
import { FaPlus } from "react-icons/fa6";
import { v4 } from "uuid";

type PropsType<T extends FieldValues> = {
  allowedTxtFields: FormFieldTxtSearchBarT<T>[];
  existingFields: FormFieldTxtSearchBarT<T>[];
  append: UseFieldArrayAppend<T>;
};

const SecondaryRow = <T extends FieldValues>({
  existingFields,
  allowedTxtFields,
  append,
}: PropsType<T>) => {
  const [isShw, setIsShw] = useState(false);
  const contRef = useRef<HTMLDivElement | null>(null);

  const filtered: FormFieldTxtSearchBarT<T>[] = useMemo(
    () =>
      allowedTxtFields
        .filter(
          (el) => !new Set(existingFields.map((ex) => ex.name)).has(el.name)
        )
        .map((el) => ({
          ...el,
          id: v4(),
        })),
    [existingFields, allowedTxtFields]
  );

  useMouseOut({
    cb: () => setIsShw(false),
    ref: contRef,
  });

  return (
    <div className="w-full grid grid-cols-2">
      {!!filtered.length && (
        <div ref={contRef} className="w-[75px] relative">
          <BtnSvg
            {...{
              act: "INFO",
              Svg: FaPlus,
              confPortal: {
                txt: "Add Input",
                showPortal: true,
                optDep: [existingFields.length],
              },
              handleClick: () => setIsShw(!isShw),
            }}
          />

          <div
            className="absolute w-[250px] border-2 border-w__0 rounded-xl left-0 z-10 bg-neutral-950 overflow-hidden max-h-[250px] scroll__app overflow-y-auto"
            css={css`
              top: calc(100% + 10px);
              transition: 0.4s;
              transform: translateY(${isShw ? "0%" : "120%"});
              opacity: ${isShw ? "1" : "0"};
            `}
          >
            {filtered.map((el) => (
              <div
                key={el.id}
                onClick={() => {
                  append({
                    ...el,
                    val: "",
                  } as T[Path<T>]);
                  setIsShw(false);
                }}
                className="w-full flex justify-center py-2 hover:text-neutral-950 hover:bg-neutral-300 transition-all duration-300 cursor-pointer"
              >
                <span className="txt__md">{el.label}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default SecondaryRow;
