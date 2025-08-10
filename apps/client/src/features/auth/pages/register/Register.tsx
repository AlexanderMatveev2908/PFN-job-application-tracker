/** @jsxImportSource @emotion/react */
"use client";

import FormFieldTxt from "@/common/components/forms/inputs/FormFieldTxt";
import { useEffect, useRef, useState, type FC } from "react";
import { registerSwap_0, registerSwap_1 } from "./uiFactory/register";
import { useFocus } from "@/core/hooks/etc/useFocus";
import { __cg } from "@/core/lib/log";
import { useGenIDs } from "@/core/hooks/etc/useGenIDs";
import { useForm } from "react-hook-form";
import { RegisterFormT, registerSchema } from "./schemas/register";
import { zodResolver } from "@hookform/resolvers/zod";
import { css } from "@emotion/react";
import BtnsSwapper from "@/common/components/HOC/BtnsSwapper";
import WrapSwap from "./components/WrapSwap";
import BtnShim from "@/common/components/buttons/BtnShim/BtnShim";

const Register: FC = ({}) => {
  const [currSwap, setCurrSwap] = useState(0);

  const [contentH, setContentH] = useState(0);
  const contentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = contentRef.current;
    if (!el) return;

    const cb = () => setContentH(el.scrollHeight);
    cb();

    const ro = new ResizeObserver(cb);
    ro.observe(el);

    return () => {
      ro.disconnect();
    };
  }, [currSwap]);

  const formCtx = useForm<RegisterFormT>({
    mode: "onChange",
    resolver: zodResolver(registerSchema),
  });

  const {
    control,
    setFocus,
    trigger,
    formState: { errors },
    handleSubmit,
  } = formCtx;

  const handleSave = handleSubmit(
    (data) => {
      __cg(data);
    },
    (errs) => {
      __cg("errors", errs);

      return errs;
    }
  );

  useFocus("first_name", { setFocus });

  const { ids } = useGenIDs({
    lengths: [registerSwap_0.length],
  });

  return (
    <form className="w-full grid grid-cols-1 gap-10" onSubmit={handleSave}>
      <div
        className="w-full flex"
        css={css`
          min-width: 200%;
          max-height: ${contentH}px;
          overflow: hidden;
          transition: transform 0.4s, max-height 0.4s, opacity 0.3s;
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
              key={ids[0][i]}
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

      <BtnsSwapper
        {...{
          currSwap,
          setCurrSwap,
          totSwaps: 2,
        }}
      />

      <div className="w-[250px] justify-self-center mt-4">
        <BtnShim
          {...{
            type: "submit",
            label: "Save",
          }}
        />
      </div>
    </form>
  );
};

export default Register;
