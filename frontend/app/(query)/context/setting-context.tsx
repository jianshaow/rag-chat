"use client";

import { fetchChatConfig, fetchConfig, fetchModelConfig, getBeBaseUrl, } from '@/lib/backend';
import { AppConfig, ChatConfig, ModelConfig } from '@/types/config';
import React, { createContext, useContext, useEffect, useState } from "react";

interface SettingContextType {
  beBaseUrl: string;
  setBeBaseUrl: React.Dispatch<React.SetStateAction<string>>;
  appConfig: AppConfig;
  setAppConfig: React.Dispatch<React.SetStateAction<AppConfig>>;
  modelConfig: ModelConfig;
  setModelConfig: React.Dispatch<React.SetStateAction<ModelConfig>>;
  chatConfig: ChatConfig;
  setChatConfig: React.Dispatch<React.SetStateAction<ChatConfig>>;
  loading: boolean;
  reloadModelConfig: (modelProvider: string) => Promise<void>;
  reload: () => Promise<void>;
}

export const settingContext = createContext<SettingContextType | null>(null);

export function SettingProvider({ children }: React.PropsWithChildren) {
  const [beBaseUrl, setBeBaseUrl] = useState<string>('');
  const [appConfig, setAppConfig] = useState<AppConfig>({
    modelProvider: '',
    dataDir: '',
    toolSet: '',
    mcpServer: '',
  });
  const [modelConfig, setModelConfig] = useState<ModelConfig>({
    embedModel: '',
    chatModel: '',
  });
  const [chatConfig, setChatConfig] = useState<ChatConfig>({
    starterQuestions: [],
  });
  const [loading, setLoading] = useState(true);

  async function loadModelConfig(modelProvider: string) {
    const modelConfig = await fetchModelConfig(modelProvider);
    setModelConfig({
      embedModel: modelConfig.embed_model,
      chatModel: modelConfig.chat_model,
    });
  }

  async function loadChatConfig() {
    const chatConfig = await fetchChatConfig();
    setChatConfig({
      starterQuestions: chatConfig.starterQuestions,
    });
  }

  async function loadConfig() {
    try {
      setLoading(true);
      const appConfig = await fetchConfig();
      setAppConfig({
        modelProvider: appConfig.model_provider,
        dataDir: appConfig.data_dir,
        toolSet: appConfig.tool_set,
        mcpServer: appConfig.mcp_server,
      });
      await loadModelConfig(appConfig.model_provider);
      await loadChatConfig()
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    setBeBaseUrl(getBeBaseUrl());
  }, []);

  useEffect(() => {
    loadConfig();
  }, [beBaseUrl]);

  useEffect(() => {
    if (appConfig.modelProvider) {
      loadModelConfig(appConfig.modelProvider);
    }
    loadChatConfig();
  }, [appConfig]);

  return (
    <settingContext.Provider
      value={{
        beBaseUrl, setBeBaseUrl,
        appConfig, setAppConfig,
        modelConfig, setModelConfig,
        chatConfig, setChatConfig,
        loading, reload: loadConfig,
        reloadModelConfig: loadModelConfig,
      }}
    >
      {children}
    </settingContext.Provider>
  );
}

export function useSetting() {
  const context = useContext(settingContext);
  if (!context) {
    throw new Error("useSetting must be used within a SettingProvider");
  }
  return context
}
