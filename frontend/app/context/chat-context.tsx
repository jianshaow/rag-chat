"use client";

import { UseChatHelpers } from "@ai-sdk/react";
import { createContext, useContext } from "react";

const chatContext = createContext<UseChatHelpers | null>(null);

interface ChatProviderProps extends React.PropsWithChildren {
  chat: UseChatHelpers;
}

export function ChatProvider({ chat, children }: ChatProviderProps) {
  return (
    <chatContext.Provider value={chat}>
      {children}
    </chatContext.Provider>
  );
}

export function useChatContext() {
  const context = useContext(chatContext);
  if (!context) {
    throw new Error("useChatContext must be used within ChatProvider");
  }
  return context;
}
