/** @jsxImportSource @emotion/react */
"use client";

import { useMouseOut } from "@/core/hooks/etc/useMouseOut";
import { useRef, type FC } from "react";
import BlackBg from "../../elements/BlackBg";
import { motion } from "framer-motion";
import { varPop } from "./uiFactory";
import BtnSvg from "../../buttons/BtnSvg";
import { X } from "lucide-react";

type PropsType = {
  isPop: boolean | null;
  setIsPop:
    | ((val: boolean | null) => void)
    | React.Dispatch<React.SetStateAction<boolean | null>>;

  children: React.ReactNode | (() => React.ReactNode);
  allowClose?: boolean;
};

const WrapPop: FC<PropsType> = ({
  isPop,
  setIsPop,
  children,
  allowClose = true,
}) => {
  const popRef = useRef<HTMLDivElement | null>(null);

  useMouseOut({
    ref: popRef,
    cb: () => (allowClose ? setIsPop(false) : null),
  });

  return (
    <>
      <BlackBg {...{ isDark: isPop, classIndexCSS: "z__black_bg__popup" }} />

      <motion.div
        ref={popRef}
        className="z__popup fixed inset-0 m-auto w-[80%] max-w-[600px] h-full max-h-[600px] bg-neutral-950 p-5 rounded-2xl border-neutral-600 border-[3px]"
        initial={{
          scaleX: 0,
          scaleY: 0,
        }}
        variants={varPop}
        animate={
          typeof isPop === "boolean" ? (isPop ? "open" : "close") : undefined
        }
      >
        <div className="flex w-full max-h-full justify-end -mt-2">
          <BtnSvg
            {...{
              handleClick: () => setIsPop(false),
              isEnabled: allowClose,
              Svg: X,
              act: "ERR",
            }}
          />
        </div>

        <div className="h-full w-full pt-6">
          {typeof children === "function" ? children() : children}
        </div>
      </motion.div>
    </>
  );
};

export default WrapPop;
