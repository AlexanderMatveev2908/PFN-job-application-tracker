import { easeInOut } from "framer-motion";

export const varToast = {
  hidden: {
    opacity: 0,
    x: "100%",
  },
  open: {
    transition: {
      duration: 0.6,
      ease: easeInOut,
    },
    opacity: [0, ...Array.from({ length: 6 }, () => 1)],
    x: ["100%", "-60%", "40%", "-30%", "20%", "-10%", "0%"],
  },
  close: {
    transition: {
      duration: 0.3,
      ease: easeInOut,
    },
    opacity: [1, 1, 0.5],
    x: ["0%", "-60%", "100%"],
  },
};
