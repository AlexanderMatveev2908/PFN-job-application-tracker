import { envApp } from "@/core/constants/env";

export const resetValsRegister = {
  first_name: "",
  last_name: "",
  email: "",
  password: "",
  confirm_password: "",
};

export const getDefValsRegister = () =>
  !envApp.isDev
    ? resetValsRegister
    : {
        first_name: "Alex",
        last_name: "Matveev",
        email: "matveevalexander470@gmail.com",
        password: "0$EM09btNPiC}!3d+t2{",
        confirm_password: "0$EM09btNPiC}!3d+t2{",
        terms: true,
      };
