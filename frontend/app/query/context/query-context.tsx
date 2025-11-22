"use client";

import { SourceNode } from "@llamaindex/chat-ui/widgets";
import React, { createContext, useContext, useState } from "react";

interface QueryContextType {
  agentic: boolean;
  setAgentic: React.Dispatch<React.SetStateAction<boolean>>;
  streaming: boolean;
  setStreaming: React.Dispatch<React.SetStateAction<boolean>>;
  events: string[];
  setEvents: React.Dispatch<React.SetStateAction<string[]>>;
  sources: SourceNode[];
  setSources: React.Dispatch<React.SetStateAction<SourceNode[]>>;
  answer: string;
  setAnswer: React.Dispatch<React.SetStateAction<string>>;
}

export const queryContext = createContext<QueryContextType>({
  agentic: true,
  setAgentic: () => { },
  streaming: true,
  setStreaming: () => { },
  events: [],
  setEvents: () => { },
  sources: [],
  setSources: () => { },
  answer: '',
  setAnswer: () => { },
});

export function QueryProvider({ children }: React.PropsWithChildren) {
  const [agentic, setAgentic] = useState<boolean>(true);
  const [streaming, setStreaming] = useState<boolean>(true);
  const [events, setEvents] = useState<string[]>([]);
  const [sources, setSources] = useState<SourceNode[]>([]);
  const [answer, setAnswer] = useState<string>('');

  return (
    <queryContext.Provider value={{ agentic, setAgentic, streaming, setStreaming, events, setEvents, sources, setSources, answer, setAnswer }}>
      {children}
    </queryContext.Provider>
  );
}

export function useQuery() {
  const context = useContext(queryContext);
  if (!context) {
    throw new Error("useQuery must be used within a QueryProvider");
  }
  return context
}
