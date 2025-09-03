/** @jsxImportSource @emotion/react */
"use client";

import { useMemo, useState, type FC } from "react";
import WrapSwapManageAcc from "./subComponents/WrapSwapManageAcc";
import { FormManageAccPropsType } from "../types";
import BtnShadow from "@/common/components/buttons/BtnShadow";
import { useKitHooks } from "@/core/hooks/etc/useKitHooks";
import { useGetUserState } from "@/features/user/hooks/useGetUserState";
import { Setup2FAReturnT, userSliceAPI } from "@/features/user/slices/api";
import ImgLoader from "@/common/components/HOC/assetsHandlers/ImgLoader";
import CpyPaste from "@/common/components/elements/tooltips/CpyPaste/CpyPaste";
import LinkShadow from "@/common/components/links/LinkShadow";

const SwapSetup2FA: FC<FormManageAccPropsType> = ({
  contentRef,
  isCurr,
  swapState,
}) => {
  const [res2FA, setRes2FA] = useState<Setup2FAReturnT | null>(null);

  const testID = "setup_2FA";

  const [mutate, { isLoading }] = userSliceAPI.useSetup2FAMutation();

  const { wrapAPI } = useKitHooks();
  const { cbc_hmac_token } = useGetUserState();

  const handleClick = async () => {
    const res = await wrapAPI<Setup2FAReturnT>({
      cbAPI: () => mutate({ cbc_hmac_token }),
      pushNotice: [401],
    });

    if (!res) return;

    setRes2FA({
      totp_secret_qrcode: res.totp_secret_qrcode,
      totp_secret: res.totp_secret,
      backup_codes: res.backup_codes,
      zip_file: res.zip_file,
    });
  };

  const portalConf = useMemo(
    () => ({
      showPortal: isCurr && swapState.swapMode !== "swapping",
      optDep: [isCurr, swapState.swapMode],
    }),
    [isCurr, swapState.swapMode]
  );

  return (
    <WrapSwapManageAcc
      {...{
        contentRef,
        isCurr,
        title: "Setup 2FA",
        testID,
      }}
    >
      {res2FA && (
        <div className="w-full grid grid-cols-1 md:grid-cols-2 justify-items-center items-center">
          <a
            download={"qrcode.png"}
            href={res2FA.totp_secret_qrcode}
            className="w-[250px] h-[250px] my-[30px]"
          >
            <ImgLoader {...{ src: res2FA.totp_secret_qrcode }} />
          </a>

          <div className="cont__grid__lg justify-items-center h-fit items-center">
            <div className="w-[250px]">
              <CpyPaste
                {...{
                  portalConf,
                  txt: res2FA.totp_secret,
                  label: "TOTP Secret",
                }}
              />
            </div>
            <div className="w-[250px]">
              <CpyPaste
                {...{
                  portalConf,
                  txt: (() => {
                    let txt = "";

                    for (let i = 0; i < 6; i += 2) {
                      txt +=
                        res2FA.backup_codes.slice(i, i + 2).join("  ") + "\n";
                    }

                    return txt;
                  })(),
                  label: "Backup Codes",
                }}
              />
            </div>
          </div>
        </div>
      )}

      <div className="mt-[50px] w-[250px] justify-self-center">
        {res2FA ? (
          <LinkShadow
            {...{
              el: {
                label: "Download Zip",
              },
              href: res2FA.zip_file,
              act: "INFO",
              download: "2FA.zip",
            }}
          />
        ) : (
          <BtnShadow
            {...{
              el: {
                label: "Submit",
              },
              testID: `${testID}__btn`,
              isLoading,
              act: "INFO",
              handleClick,
            }}
          />
        )}
      </div>
    </WrapSwapManageAcc>
  );
};

export default SwapSetup2FA;
