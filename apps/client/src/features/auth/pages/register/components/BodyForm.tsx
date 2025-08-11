/** @jsxImportSource @emotion/react */
"use client";

import { css } from "@emotion/react";
import { type FC } from "react";
import WrapSwap from "./subComponents/WrapSwap";
import { registerSwap_0, termsField } from "../uiFactory/register";
import { useFormContext } from "react-hook-form";
import { useGenIDs } from "@/core/hooks/etc/useGenIDs";
import FormFieldTxt from "@/common/components/forms/inputs/FormFieldTxt";
import { RegisterFormT } from "../schemas/register";
import { useListenHeight } from "@/core/hooks/ui/useListenHeight";
import FormFieldCheck from "@/common/components/forms/inputs/FormFieldCheck/FormFieldCheck";
import PairPwd from "@/features/auth/components/PairPwd/PairPwd";

type PropsType = {
  currSwap: number;
};

const BodyForm: FC<PropsType> = ({ currSwap }) => {
  const { contentRef, contentH } = useListenHeight({ opdDep: [currSwap] });

  const {
    control,
    formState: { errors },
    watch,
    setValue,
  } = useFormContext<RegisterFormT>();

  const { ids } = useGenIDs({
    lengths: [registerSwap_0.length, registerSwap_0.length],
  });

  return (
    <div
      className="transition-all duration-[0.4s] p-5"
      css={css`
        max-height: ${contentH ? `${contentH}px` : "fit-content"};
        height: ${contentH ? `${contentH}px` : "fit-content"};
        overflow: hidden;
      `}
    >
      <div
        className="w-full h-full flex"
        css={css`
          min-width: 200%;
          transition: 0.4s;
          transform: translateX(-${(100 / 2) * currSwap}%);
        `}
      >
        <WrapSwap
          {...{
            isCurr: currSwap === 0,
            contentRef,
          }}
        >
          {registerSwap_0.map((el, i) => (
            <FormFieldTxt
              key={ids[0][i]}
              {...{
                el,
                control,
              }}
            />
          ))}
        </WrapSwap>

        <WrapSwap
          {...{
            isCurr: currSwap === 1,
            contentRef,
          }}
        >
          <PairPwd
            {...{
              isCurrSwap: currSwap === 1,
            }}
          />

          <FormFieldCheck
            {...{
              el: termsField,
              errors,
              isChecked: watch("terms"),
              setValue,
              showLabel: false,
              optTxt: "I accept terms & conditions",
            }}
          />
        </WrapSwap>
      </div>
    </div>
  );
};

export default BodyForm;
