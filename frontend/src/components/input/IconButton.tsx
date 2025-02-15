import {
  IconButton as IconButtonInternal,
  Tooltip
} from "@mui/material";
import React from "react";

export const IconButton = ({label, icon, ...rest}: {
  label?: string,
  icon: React.ReactNode,
} & React.PropsWithoutRef<any>) => (
  <Tooltip title={label}>
    <IconButtonInternal {...rest}>
      {icon}
    </IconButtonInternal>
  </Tooltip>
)
