"use client";

import { fetchAppConfig, fetchChatConfig, fetchChatModels, fetchDataConfig, fetchEmbedModels, fetchMcpServers, fetchModelConfig, fetchModelProviders, fetchToolSets, getBeBaseUrl, } from '@/lib/backend';
import { AppConfig, ChatConfig, ModelConfig } from '@/types/config';
import React, { createContext, useContext, useEffect, useState } from "react";

interface SettingContextType {
  beBaseUrl: string;
  setBeBaseUrl: React.Dispatch<React.SetStateAction<string>>;
  modelProviders: string[];
  setModelProviders: React.Dispatch<React.SetStateAction<string[]>>;
  toolSets: string[];
  setToolSets: React.Dispatch<React.SetStateAction<string[]>>;
  dataDirs: string[];
  setDataDirs: React.Dispatch<React.SetStateAction<string[]>>;
  mcpServers: string[];
  setMcpServers: React.Dispatch<React.SetStateAction<string[]>>;
  embedModels: string[];
  setEmbedModels: React.Dispatch<React.SetStateAction<string[]>>;
  chatModels: string[];
  setChatModels: React.Dispatch<React.SetStateAction<string[]>>;
  appConfig: AppConfig;
  setAppConfig: React.Dispatch<React.SetStateAction<AppConfig>>;
  modelConfig: ModelConfig;
  setModelConfig: React.Dispatch<React.SetStateAction<ModelConfig>>;
  chatConfig: ChatConfig;
  setChatConfig: React.Dispatch<React.SetStateAction<ChatConfig>>;
}

export const SettingContext = createContext<SettingContextType | null>(null);

export function SettingProvider({ children }: React.PropsWithChildren) {
  const [beBaseUrl, setBeBaseUrl] = useState<string>('');
  const [modelProviders, setModelProviders] = useState<string[]>([]);
  const [toolSets, setToolSets] = useState<string[]>([]);
  const [dataDirs, setDataDirs] = useState<string[]>([]);
  const [mcpServers, setMcpServers] = useState<string[]>([]);
  const [embedModels, setEmbedModels] = useState<string[]>([]);
  const [chatModels, setChatModels] = useState<string[]>([]);
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

  function initModelProviders() {
    fetchModelProviders().then((modelProviders) => {
      setModelProviders(modelProviders);
    });
  }

  function initToolSets() {
    fetchToolSets().then(toolSets => {
      setToolSets(toolSets);
    });
  }

  function initDataDirs() {
    fetchDataConfig().then(dataConfig => {
      const dataDirs = Object.keys(dataConfig).map((data) => {
        return data;
      });
      setDataDirs(dataDirs);
    });
  }

  function initMcpServers() {
    fetchMcpServers().then(mcpServers => {
      setMcpServers(mcpServers);
    });
  }

  function initEmbedModels() {
    fetchEmbedModels(false).then((models) => {
      if (!models.includes(modelConfig.embedModel)) {
        models.push(modelConfig.embedModel);
      }
      setEmbedModels(models);
    });
  }

  function initChatModels() {
    fetchChatModels(false).then((models) => {
      if (!models.includes(modelConfig.chatModel)) {
        models.push(modelConfig.chatModel);
      }
      setChatModels(models);
    });
  }

  async function loadAppConfig() {
    const appConfig = await fetchAppConfig();
    setAppConfig({
      modelProvider: appConfig.model_provider,
      dataDir: appConfig.data_dir,
      toolSet: appConfig.tool_set,
      mcpServer: appConfig.mcp_server,
    });
    return appConfig;
  }

  async function loadModelConfig(modelProvider: string) {
    const modelConfig = await fetchModelConfig(modelProvider);
    setModelConfig({
      embedModel: modelConfig.embed_model,
      chatModel: modelConfig.chat_model,
    });
    return modelConfig;
  }

  async function loadChatConfig() {
    const chatConfig = await fetchChatConfig();
    setChatConfig({
      starterQuestions: chatConfig.starterQuestions,
    });
    return chatConfig;
  }

  useEffect(() => {
    const baseUrl = getBeBaseUrl();
    setBeBaseUrl(baseUrl);
  }, []);

  useEffect(() => {
    if (beBaseUrl != '') {
      initModelProviders();
      initToolSets();
      initDataDirs();
      initMcpServers();
      loadAppConfig();
    }
  }, [beBaseUrl]);

  useEffect(() => {
    if (appConfig.modelProvider) {
      initEmbedModels();
      initChatModels();
      loadModelConfig(appConfig.modelProvider);
    }
  }, [appConfig.modelProvider]);

  useEffect(() => {
    loadChatConfig();
  }, [appConfig.dataDir, appConfig.toolSet, appConfig.mcpServer]);

  return (
    <SettingContext.Provider
      value={{
        beBaseUrl, setBeBaseUrl,
        modelProviders, setModelProviders,
        toolSets, setToolSets,
        dataDirs, setDataDirs,
        mcpServers, setMcpServers,
        embedModels, setEmbedModels,
        chatModels, setChatModels,
        appConfig, setAppConfig,
        modelConfig, setModelConfig,
        chatConfig, setChatConfig,
      }}
    >
      {children}
    </SettingContext.Provider>
  );
}

export function useSetting() {
  const context = useContext(SettingContext);
  if (!context) {
    throw new Error("useSetting must be used within a SettingProvider");
  }
  return context
}
