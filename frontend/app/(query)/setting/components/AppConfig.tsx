"use client";

import { useSetting } from '@/(query)/context/setting-context';
import {
  fetchDataConfig,
  fetchMcpServers,
  fetchModelProviders,
  fetchToolSets,
  indexData,
  updateConfig
} from '@/lib/backend';
import { AppConfig } from '@/types/config';
import { ChangeEvent, MouseEvent, useEffect, useState } from 'react';
import '../../common.css';
import '../Setting.css';

export default function AppConfigSetting() {
  const settingContext = useSetting();

  const [modelProviders, setModelProviders] = useState<string[]>([]);
  const [toolSets, setToolSets] = useState<string[]>([]);
  const [dataDirs, setDataDirs] = useState<string[]>([]);
  const [mcpServers, setMcpServers] = useState<string[]>([]);

  const [appConfig, setAppConfig] = useState<AppConfig>(settingContext.appConfig);

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

  const handleIndexData = async (e: MouseEvent) => {
    indexData(appConfig.dataDir).then(() => {
      alert('Data Indexed!')
    });
  }

  const handleSaveConfig = async (e: MouseEvent) => {
    const config = {
      'model_provider': appConfig.modelProvider,
      'tool_set': appConfig.toolSet,
      'data_dir': appConfig.dataDir,
      'mcp_server': appConfig.mcpServer,
    };
    updateConfig(JSON.stringify(config)).then(() => {
      alert('Setting Saved!');
    })
    settingContext.setAppConfig(appConfig);
  };

  useEffect(() => {
    initModelProviders();
    initToolSets();
    initDataDirs();
    initMcpServers();
    setAppConfig(settingContext.appConfig);
  }, [settingContext.appConfig]);

  return (
    <div>
      <label className='title'>App Config</label>
      <div className='setting-container'>
        <div className='setting'>
          <label>Model Provider:</label>
          <select value={appConfig.modelProvider} onChange={(e: ChangeEvent<HTMLSelectElement>) => {
            setAppConfig(prev => ({ ...prev, modelProvider: e.target.value }));
          }}>{modelProviders.map(modelProvider => (
            <option key={modelProvider} value={modelProvider}>{modelProvider}</option>
          ))}
          </select>
        </div>
        <div className='setting'>
          <label>Tool Set:</label>
          <select value={appConfig.toolSet} onChange={(e: ChangeEvent<HTMLSelectElement>) => {
            setAppConfig(prev => ({ ...prev, toolSet: e.target.value }));
          }}>{toolSets.map(toolSet => (
            <option key={toolSet} value={toolSet}>{toolSet}</option>
          ))}
          </select>
        </div>
        <div className='setting'>
          <label>Data Dir:</label>
          <select value={appConfig.dataDir} onChange={(e: ChangeEvent<HTMLSelectElement>) => {
            setAppConfig(prev => ({ ...prev, dataDir: e.target.value }));
          }}>{dataDirs.map(dataDir => (
            <option key={dataDir} value={dataDir}>{dataDir}</option>
          ))}
          </select>
          <button onClick={handleIndexData}>Index</button>
        </div>
        <div className='setting'>
          <label>MCP server:</label>
          <select value={appConfig.mcpServer} onChange={(e: ChangeEvent<HTMLSelectElement>) => {
            setAppConfig(prev => ({ ...prev, mcpServer: e.target.value }));
          }}>{mcpServers.map(mcpServer => (
            <option key={mcpServer} value={mcpServer}>{mcpServer}</option>
          ))}
          </select>
        </div>
        <div className='setting'>
          <button onClick={handleSaveConfig}>Save</button>
        </div>
      </div>
    </div>
  );
}
