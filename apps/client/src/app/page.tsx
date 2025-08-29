/** @jsxImportSource @emotion/react */
"use client";

import BtnShadow from "@/common/components/buttons/BtnShadow";
import WrapCSR from "@/common/components/HOC/pageWrappers/WrapCSR";
import { useWrapMutation } from "@/core/hooks/api/useWrapMutation";
import { testSliceAPI } from "@/features/test/slices/api";
import { type FC } from "react";

const Home: FC = () => {
  const [mutate, { isLoading }] = testSliceAPI.usePosHelloMutation();
  const { wrapMutation } = useWrapMutation();

  const handleClick = async () => {
    await wrapMutation({
      cbAPI: () => mutate({ msg: "Client message" }),
    });
  };

  return (
    <WrapCSR>
      <div className="w-full h-full min-h-screen flex flex-col justify-center items-center gap-20">
        <span className="text-3xl font-bold">Script worked ✌🏽</span>

        <div className="w-[250px]">
          <BtnShadow
            {...{
              act: "OK",
              handleClick,
              el: {
                label: "Click me",
              },
              isLoading,
            }}
          />
        </div>
      </div>
    </WrapCSR>
  );
};

export default Home;
