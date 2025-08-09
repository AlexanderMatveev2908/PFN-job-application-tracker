import SvgAccount from "@/common/components/SVGs/Account";
import SvgConfirmEmail from "@/common/components/SVGs/ConfirmEmail";
import SvgHome from "@/common/components/SVGs/Home";
import SvgLogin from "@/common/components/SVGs/Login";
import SvgRecoverPwd from "@/common/components/SVGs/RecoverPwd";
import SvgRegister from "@/common/components/SVGs/Register";
import SvgSearch from "@/common/components/SVGs/Search";
import SvgWrite from "@/common/components/SVGs/Write";
import { DropMenuT, LinkAppSvgT } from "@/common/types/ui";

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

export const sideLinksNonLogged: DropMenuT = {
  label: "Account",
  Svg: SvgAccount,

  links: [
    {
      label: "Register",
      href: "/auth/register",
      Svg: SvgRegister,
    },
    {
      label: "Login",
      href: "/auth/login",
      Svg: SvgLogin,
    },
    {
      label: "Recover Email",
      href: "/auth/recover-pwd",
      Svg: SvgRecoverPwd,
    },
    ...sideSharedLinks,
  ],
};
