/** @jsxImportSource @emotion/react */
"use client";

import { AppEventT } from "@/common/types/api";
import { css, SerializedStyles } from "@emotion/react";
import { CSSProperties, useMemo, type FC } from "react";
import { $argClr } from "@/core/uiFactory/style";
import Link from "next/link";
import WrapBtnAPI from "../buttonWrappers/WrapBtnAPI";
import { FieldTxtSvgT, TestIdT } from "@/common/types/ui";

type PropsType = {
  wrapper: "next_link" | "html_button";
  handleClick?: () => void;
  href?: string;
  $customLabelCSS?: SerializedStyles;
  isEnabled?: boolean;
  isLoading?: boolean;
  el: FieldTxtSvgT;
  act: AppEventT;
} & TestIdT;

const WrapElWithShadow: FC<PropsType> = ({
  wrapper,
  $customLabelCSS,
  act = "NONE",
  handleClick,
  href,
  isEnabled = true,
  isLoading,
  el,
  t_id,
}) => {
  const $clr = $argClr[act];

  const objProps = useMemo(
    () => ({
      "data-testid": t_id,
      className: `${
        wrapper === "next_link" ? "el__app" : "btn__app"
      } w-full flex justify-center items-center gap-6 py-2 px-4 rounded-xl`,

      style: {
        "--scale__up": 1.15,
      } as CSSProperties,

      css: css`
        border: 2px solid ${$clr};
        color: ${$clr};
        background: transparent;

        &${wrapper === "html_button" ? ":enabled" : ""}:hover {
          box-shadow: 0 0 5px ${$clr}, 0 0 10px ${$clr}, 0 0 15px ${$clr},
            0 0 20px ${$clr}, 0 0 25px ${$clr}, 0 0 30px ${$clr};
        }
      `,
    }),
    [$clr, wrapper, t_id]
  );

  const content = (
    <>
      {el.Svg && <el.Svg className="svg__md" />}

      {el.label && (
        <span
          css={css`
            ${$customLabelCSS}
          `}
          className="txt__lg"
        >
          {el.label}
        </span>
      )}
    </>
  );

  return wrapper === "next_link" ? (
    <Link
      href={href!}
      {...objProps}
      {...(href?.startsWith("https://")
        ? { rel: "noopener noreferrer", target: "_blank" }
        : {})}
    >
      {content}
    </Link>
  ) : (
    <WrapBtnAPI {...{ isLoading, act }}>
      <button onClick={handleClick} disabled={!isEnabled} {...objProps}>
        {content}
      </button>
    </WrapBtnAPI>
  );
};

export default WrapElWithShadow;
