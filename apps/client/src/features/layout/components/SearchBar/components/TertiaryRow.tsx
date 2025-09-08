/** @jsxImportSource @emotion/react */
"use client";

import BtnShadow from "@/common/components/buttons/BtnShadow";
import { useGenIDs } from "@/core/hooks/etc/useGenIDs";
import { resp } from "@/core/lib/style";
import { css } from "@emotion/react";
import type { FC } from "react";
import { mainBtnsSearchBar } from "../uiFactory";

type PropsType = {
  handleReset: () => void;
};

const TertiaryRow: FC<PropsType> = ({ handleReset }) => {
  const {
    ids: [ids],
  } = useGenIDs({ lengths: [2] });

  return (
    <div className="w-full grid grid-cols-2 gap-10 justify-items-center">
      {mainBtnsSearchBar.map((btn, i) => (
        <div key={ids[i]} className="w-[80px] md:w-[250px]">
          <BtnShadow
            {...{
              act: btn.act,
              el: {
                label: btn.label,
                Svg: btn.Svg,
              },
              handleClick: btn.act === "OK" ? () => null : handleReset,
              type: btn.act === "OK" ? "submit" : "button",
              $customLabelCSS: css`
                display: none;

                ${resp("md")} {
                  display: block;
                }
              `,
            }}
          />
        </div>
      ))}
    </div>
  );
};

export default TertiaryRow;
