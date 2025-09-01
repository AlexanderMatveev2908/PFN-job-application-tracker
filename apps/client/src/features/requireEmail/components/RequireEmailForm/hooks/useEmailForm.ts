import { useForm } from "react-hook-form";
import { EmailFormT } from "../paperwork";
import { zodResolver } from "@hookform/resolvers/zod";
import { emailSchema } from "@/core/paperwork";
import { useFocus } from "@/core/hooks/ui/useFocus";

export const useEmailForm = () => {
  const formCtx = useForm<EmailFormT>({
    mode: "onChange",
    resolver: zodResolver(emailSchema),
    defaultValues: {
      email: "",
    },
  });

  const { setFocus } = formCtx;
  useFocus("email", { setFocus });

  return {
    formCtx,
  };
};
