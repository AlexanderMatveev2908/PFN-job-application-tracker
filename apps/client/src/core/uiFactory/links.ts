import SvgConfirmEmail from "@/common/components/SVGs/ConfirmEmail";
import { GoHomeFill } from "react-icons/go";
import SvgRegister from "@/common/components/SVGs/Register";
import { LinkAppSvgT } from "@/common/types/ui";
import { FaKey } from "react-icons/fa6";
import { FiLogIn } from "react-icons/fi";
import { HiOutlineLogout } from "react-icons/hi";

export const linksAll: LinkAppSvgT[] = [
  {
    label: "Home",
    href: "/",
    Svg: GoHomeFill,
  },
];

const linkConfirmEmail: LinkAppSvgT = {
  label: "Confirm Email",
  href: "/auth/confirm-email",
  Svg: SvgConfirmEmail,
};

export const linksNonLogged: LinkAppSvgT[] = [
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
    label: "Recover Password",
    href: "/auth/recover-pwd",
    Svg: FaKey,
    fill: "var(--white__0)",
  },
  linkConfirmEmail,
];

export const linkLogout: LinkAppSvgT = {
  label: "Logout",
  href: "#",
  Svg: HiOutlineLogout,
};
