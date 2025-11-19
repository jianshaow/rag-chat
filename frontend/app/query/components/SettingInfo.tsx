import {
  fetchConfig,
  fetchModelConfig
} from '@/lib/backend';
import React, { useEffect, useState } from "react";

import '../Home.css';
import './SettingInfo.css';

interface SettingInfo {
  modelProvider: string;
  toolSet: string;
  dataDir: string;
  mcpServer: string;
}

interface ModelConfig {
  embedModel: string;
  chatModel: string;
}

const SettingInfo: React.FC = () => {

  const [settingInfo, setSettingInfo] = useState<SettingInfo>();
  const [modelConfig, setModelConfig] = useState<ModelConfig>();

  useEffect(() => {
    fetchConfig().then(config => {
      setSettingInfo({
        modelProvider: config.model_provider,
        dataDir: config.data_dir,
        toolSet: config.tool_set,
        mcpServer: config.mcp_server,
      });
      fetchModelConfig(config.model_provider).then(config => {
        setModelConfig({
          embedModel: config.embed_model,
          chatModel: config.chat_model,
        });
      });
    });
  }, []);

  return (
    <div className='container-column'>
      <label>Current Setting</label>
      <div className='info-block'>
        <div>
          <label>Model Provider</label>
          <div className="info-value">{settingInfo?.modelProvider}</div>
        </div>
        <div>
          <label>Embed Model</label>
          <div className="info-value">{modelConfig?.embedModel}</div>
        </div>
        <div>
          <label>Chat Model</label>
          <div className="info-value">{modelConfig?.chatModel}</div>
        </div>
        <div>
          <label>Tool Set</label>
          <div className="info-value">{settingInfo?.toolSet}</div>
        </div>
        <div>
          <label>Data Dir</label>
          <div className="info-value">{settingInfo?.dataDir}</div>
        </div>
        <div>
          <label>MCP Server</label>
          <div className="info-value">{settingInfo?.mcpServer}</div>
        </div>
      </div>
    </div>
  );
}

export default SettingInfo
