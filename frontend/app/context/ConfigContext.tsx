"use client";

import {
  fetchConfig,
  fetchModelConfig
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

interface ConfigContextType {
  settingInfo?: SettingInfo;
  modelConfig?: ModelConfig;
  loading: boolean;
  error?: string;
  refresh: () => Promise<void>;
}

export const configContext = createContext<ConfigContextType>({
  loading: true,
  refresh: async () => { },
});

export function ConfigProvider({ children }: { children: React.ReactNode }) {
  const [settingInfo, setSettingInfo] = useState<SettingInfo>();
  const [modelConfig, setModelConfig] = useState<ModelConfig>();
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

  return (
    <configContext.Provider
      value={{ settingInfo, modelConfig, loading, error, refresh: loadConfig }}
    >
      {children}
    </configContext.Provider>
  );
}

export function useConfig() {
  return useContext(configContext);
}
