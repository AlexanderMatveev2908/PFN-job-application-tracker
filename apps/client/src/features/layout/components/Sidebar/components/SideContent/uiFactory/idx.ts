import SvgAccount from "@/common/components/SVGs/Account";
import SvgConfirmEmail from "@/common/components/SVGs/ConfirmEmail";
import SvgHome from "@/common/components/SVGs/Home";
import SvgRecoverPwd from "@/common/components/SVGs/RecoverPwd";
import SvgRegister from "@/common/components/SVGs/Register";
import SvgSearch from "@/common/components/SVGs/Search";
import SvgWrite from "@/common/components/SVGs/Write";
import { DropElT, LinkAppSvgT } from "@/common/types/ui";
import { FiLogIn } from "react-icons/fi";
import { HiOutlineLogout } from "react-icons/hi";

export const sideLinksAll: LinkAppSvgT[] = [
  {
    label: "Home",
    href: "/",
    Svg: SvgHome,
  },
];

const sideSharedLinks: LinkAppSvgT[] = [
  {
    label: "Confirm Email",
    href: "/auth/confirm-email",
    Svg: SvgConfirmEmail,
  },
];

export const sideLinksLogged: LinkAppSvgT[] = [
  {
    label: "Applications",
    href: "/applications/list",
    Svg: SvgSearch,
  },
  {
    label: "Add application",
    href: "/applications/post",
    Svg: SvgWrite,
  },
];

export const sideDropAccount: DropElT = {
  label: "Account",
  Svg: SvgAccount,
};

export const sideLinksNonLogged: LinkAppSvgT[] = [
  {
    label: "Register",
    href: "/auth/register",
    Svg: SvgRegister,
  },
  {
    label: "Login",
    href: "/auth/login",
    Svg: FiLogIn,
  },
  {
    label: "Recover Email",
    href: "/auth/recover-pwd",
    Svg: SvgRecoverPwd,
    fill: "var(--white__0)",
  },
  ...sideSharedLinks,
];

export const sideLinkLogout: LinkAppSvgT = {
  label: "Logout",
  href: "#",
  Svg: HiOutlineLogout,
};
