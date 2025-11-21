"use client";

import {
  fetchChatConfig,
  fetchConfig,
  fetchModelConfig,
} from '@/lib/backend';

import React, { createContext, useContext, useEffect, useState } from "react";

interface SettingInfo {
  modelProvider: string;
  dataDir: string;
  toolSet: string[];
  mcpServer: string;
}

interface ModelConfig {
  embedModel: string;
  chatModel: string;
}

interface ChatConfig {
  starterQuestions: string[];
}

interface ConfigContextType {
  settingInfo?: SettingInfo;
  modelConfig?: ModelConfig;
  chatConfig?: ChatConfig;
  loading: boolean;
  error?: string;
  refresh: () => Promise<void>;
}

export const configContext = createContext<ConfigContextType>({
  loading: true,
  refresh: async () => { },
});

export function ConfigProvider({ children }: React.PropsWithChildren) {
  const [settingInfo, setSettingInfo] = useState<SettingInfo>();
  const [modelConfig, setModelConfig] = useState<ModelConfig>();
  const [chatConfig, setChatConfig] = useState<ChatConfig>();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>();

  async function loadConfig() {
    try {
      const appConfig = await fetchConfig();
      setSettingInfo({
        modelProvider: appConfig.model_provider,
        dataDir: appConfig.data_dir,
        toolSet: appConfig.tool_set,
        mcpServer: appConfig.mcp_server,
      });
      const modelConfig = await fetchModelConfig(appConfig.model_provider);
      setModelConfig({
        embedModel: modelConfig.embed_model,
        chatModel: modelConfig.chat_model,
      });
      const chatConfig = await fetchChatConfig();
      setChatConfig({
        starterQuestions: chatConfig.starterQuestions,
      });
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError(String(err));
      }
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadConfig();
  }, []);

  if (!chatConfig) {
    return null;
  }

  return (
    <configContext.Provider
      value={{ settingInfo, modelConfig, chatConfig, loading, error, refresh: loadConfig }}
    >
      {children}
    </configContext.Provider>
  );
}

export function useConfig() {
  const context = useContext(configContext);
  if (!context) {
    throw new Error("useConfig must be used within a ConfigProvider");
  }
  return context
}
