/** @jsxImportSource @emotion/react */
"use client";

import { css } from "@emotion/react";
import { useEffect, type FC } from "react";
import WrapSwap from "./subComponents/WrapSwap";
import { registerSwap_0, registerSwap_1 } from "../uiFactory/register";
import { useFormContext } from "react-hook-form";
import { useGenIDs } from "@/core/hooks/etc/useGenIDs";
import FormFieldTxt from "@/common/components/forms/inputs/FormFieldTxt";
import { RegisterFormT } from "../schemas/register";
import { useListenHeight } from "@/core/hooks/ui/useListenHeight";

type PropsType = {
  currSwap: number;
};

const BodyForm: FC<PropsType> = ({ currSwap }) => {
  const { contentRef, contentH } = useListenHeight({ opdDep: [currSwap] });

  const {
    control,
    trigger,
    formState: { errors },
    setError,
    clearErrors,
    watch,
  } = useFormContext<RegisterFormT>();

  const pwd = watch("password");
  const confPwd = watch("confirm_password");

  const { ids } = useGenIDs({
    lengths: [registerSwap_0.length, registerSwap_0.length],
  });

  useEffect(() => {
    if (pwd !== confPwd)
      setError("confirm_password", {
        message: "Passwords do not match",
      });
    else if (
      errors?.confirm_password?.message === "Passwords do not match" &&
      pwd === confPwd
    )
      clearErrors("confirm_password");
  }, [pwd, confPwd, watch, setError, errors, clearErrors]);

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
                errors,
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
          {registerSwap_1.map((el, i) => (
            <FormFieldTxt
              key={ids[1][i]}
              {...{
                el,
                control,
                errors,
                cb: () =>
                  trigger(
                    el.name === "password" ? "confirm_password" : "password"
                  ),
              }}
            />
          ))}
        </WrapSwap>
      </div>
    </div>
  );
};

export default BodyForm;
