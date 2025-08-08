/** @jsxImportSource @emotion/react */
"use client";

import { AppEventT } from "@/common/types/api";
import { css, SerializedStyles } from "@emotion/react";
import { CSSProperties, useMemo, type FC } from "react";
import { IconType } from "react-icons";
import { $argClr } from "@/core/uiFactory/style";
import Link from "next/link";
import WrapApiBtn from "./WrapApiBtn";

type PropsType = {
  wrapper: "next_link" | "html_button";
  handleClick?: () => void;
  href?: string;
  act?: AppEventT;
  $customLabelCSS?: SerializedStyles;
  label?: string;
  Svg?: IconType;
  isEnabled?: boolean;
  isLoading?: boolean;
};

const WrapShadow: FC<PropsType> = ({
  wrapper,
  $customLabelCSS,
  Svg,
  act = "NONE",
  handleClick,
  href,
  isEnabled = true,
  label,
  isLoading,
}) => {
  const $clr = $argClr[act];

  const twd = `${
    wrapper === "next_link" ? "el__app" : "btn__app"
  } w-full flex justify-center items-center gap-5 py-2 px-4 rounded-xl`;
  const inlineStyle = useMemo(
    () =>
      ({
        "--scale__up": 1.2,
      } as CSSProperties),
    []
  );
  const emotion = css`
    border: 2px solid ${$clr};
    color: ${$clr};
    background: transparent;

    &${wrapper === "html_button" ? ":enabled" : ""}:hover {
      box-shadow: 0 0 5px ${$clr}, 0 0 10px ${$clr}, 0 0 15px ${$clr},
        0 0 20px ${$clr}, 0 0 25px ${$clr}, 0 0 30px ${$clr};
    }
  `;

  const objProps = useMemo(
    () => ({
      className: twd,
      style: inlineStyle,
      css: emotion,
    }),
    [emotion, inlineStyle, twd]
  );

  const content = (
    <>
      {Svg && <Svg className="svg__md" />}

      {label && (
        <span
          css={css`
            ${$customLabelCSS}
          `}
          className="txt__md"
        >
          {label}
        </span>
      )}
    </>
  );

  return wrapper === "next_link" ? (
    <Link href={href!} {...objProps}>
      {content}
    </Link>
  ) : (
    <WrapApiBtn {...{ isLoading, act }}>
      <button onClick={handleClick} disabled={!isEnabled} {...objProps}>
        {content}
      </button>
    </WrapApiBtn>
  );
};

export default WrapShadow;
