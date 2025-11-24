"use client";

import React from "react";
import { SettingProvider } from "./context/setting-context";

export default function SharedLayout({ children }: React.PropsWithChildren) {
  return (
    <div className='background-gradient'>
      <SettingProvider>{children}</SettingProvider>
    </div>
  );
}
