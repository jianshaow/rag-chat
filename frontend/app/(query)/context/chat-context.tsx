"use client";

import { UseChatHelpers } from "@ai-sdk/react";
import { Message } from "@llamaindex/chat-ui";
import { createContext, useContext } from "react";

const ChatContext = createContext<UseChatHelpers<Message> | null>(null);

interface ChatProviderProps {
  chat: UseChatHelpers<Message>;
}

export function ChatProvider({ chat, children }: React.PropsWithChildren<ChatProviderProps>) {
  return (
    <ChatContext.Provider value={chat}>
      {children}
    </ChatContext.Provider>
  );
}

export function useChatContext() {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error("useChatContext must be used within ChatProvider");
  }
  return context;
}
