/** @jsxImportSource @emotion/react */
"use client";

import BtnShadow from "@/common/components/buttons/BtnShadow";
import WrapCSR from "@/common/components/HOC/pageWrappers/WrapCSR";
import { useWrapAPI } from "@/core/hooks/api/useWrapAPI";
import { testSliceAPI } from "@/features/test/slices/api";
import { useUs } from "@/features/user/hooks/useUs";
import { useEffect, type FC } from "react";

const Home: FC = () => {
  const [mutate, { isLoading }] = testSliceAPI.usePosHelloMutation();
  const { wrapAPI } = useWrapAPI();

  const handleClick = async () => {
    await wrapAPI({
      cbAPI: () => mutate({ msg: "Client message" }),
    });
  };

  const usState = useUs();

  useEffect(() => {
    if (usState.pendingAction) usState.endPendingAction();
  }, [usState]);

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
