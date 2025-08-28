/** @jsxImportSource @emotion/react */
"use client";

import { css } from "@emotion/react";
import { type FC } from "react";
import WrapSwap from "./subComponents/WrapSwap";
import { registerSwap_0, termsField } from "../uiFactory/register";
import { useFormContext, useWatch } from "react-hook-form";
import { useGenIDs } from "@/core/hooks/etc/useGenIDs";
import FormFieldTxt from "@/common/components/forms/inputs/FormFieldTxt";
import { RegisterFormT } from "../schemas/register";
import { useListenHeight } from "@/core/hooks/ui/useListenHeight";
import FormFieldCheck from "@/common/components/forms/inputs/FormFieldCheck/FormFieldCheck";
import PairPwd from "@/features/auth/components/PairPwd/PairPwd";
import { SwapStateT } from "@/core/hooks/etc/useSwap/etc/initState";

type PropsType = {
  swapState: SwapStateT;
};

const BodyForm: FC<PropsType> = ({ swapState }) => {
  const { currSwap, swapMode } = swapState;
  const { contentRef, contentH } = useListenHeight({
    opdDep: [currSwap],
  });

  const {
    control,
    formState: { errors },
    setValue,
  } = useFormContext<RegisterFormT>();
  const isChecked = useWatch<RegisterFormT>({
    control,
    name: "terms",
  });

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
                portalConf: {
                  showPortal: !currSwap && swapMode !== "swapping",
                  optDep: [currSwap, swapMode],
                },
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
              swapMode,
            }}
          />

          <FormFieldCheck
            {...{
              t_id: "body__form_terms",
              el: termsField,
              errors,
              isChecked: isChecked as boolean,
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
