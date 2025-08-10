/** @jsxImportSource @emotion/react */
"use client";

import { css } from "@emotion/react";
import { useEffect, useRef, useState, type FC } from "react";
import WrapSwap from "./subComponents/WrapSwap";
import { registerSwap_0, registerSwap_1 } from "../uiFactory/register";
import { useFormContext } from "react-hook-form";
import { useGenIDs } from "@/core/hooks/etc/useGenIDs";
import FormFieldTxt from "@/common/components/forms/inputs/FormFieldTxt";
import { RegisterFormT } from "../schemas/register";

type PropsType = {
  currSwap: number;
};

const BodyForm: FC<PropsType> = ({ currSwap }) => {
  const contentRef = useRef<HTMLDivElement>(null);
  const [contentH, setContentH] = useState(0);

  useEffect(() => {
    const el = contentRef.current;
    if (!el) return;

    const cb = () => setContentH(el.scrollHeight + 50);
    cb();

    const ro = new ResizeObserver(cb);
    ro.observe(el);

    return () => {
      ro.disconnect();
    };
  }, [currSwap]);

  const {
    control,
    trigger,
    formState: { errors },
  } = useFormContext<RegisterFormT>();

  const { ids } = useGenIDs({
    lengths: [registerSwap_0.length, registerSwap_0.length],
  });
  return (
    <div
      className="transition-all duration-[0.4s] p-5"
      css={css`
        max-height: ${contentH}px;
        height: ${contentH}px;
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
