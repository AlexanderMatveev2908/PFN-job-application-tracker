import { useDispatch } from "react-redux";
import { useWrapAPI } from "../api/useWrapAPI";
import { useRouter } from "next/navigation";
import { useNotice } from "@/features/notice/hooks/useNotice";
import { useUser } from "@/features/user/hooks/useUser";

export const useKitApp = () => {
  const dispatch = useDispatch();

  const nav = useRouter();

  const { wrapAPI } = useWrapAPI();
  const { setNotice } = useNotice();
  const userHook = useUser();

  return {
    dispatch,
    nav,
    wrapAPI,
    setNotice,
    userHook,
  };
};
