"use client";

import { useSetting } from '@/(query)/context/setting-context';
import { indexData, updateAppConfig } from '@/lib/backend';
import { AppConfig } from '@/types/config';
import { ChangeEvent, useEffect, useState } from 'react';
import '../../common.css';
import '../setting.css';

export default function AppConfigSetting() {
  const settingContext = useSetting();
  const [appConfig, setAppConfig] = useState<AppConfig>(settingContext.appConfig);

  const handleIndexData = async () => {
    indexData(appConfig.dataDir).then(() => {
      alert('Data Indexed!')
    });
  }

  const handleSaveConfig = async () => {
    const config = {
      'model_provider': appConfig.modelProvider,
      'tool_set': appConfig.toolSet,
      'data_dir': appConfig.dataDir,
      'mcp_server': appConfig.mcpServer,
    };
    updateAppConfig(JSON.stringify(config)).then(() => {
      alert('Setting Saved!');
    })
    settingContext.setAppConfig(appConfig);
  };

  useEffect(() => {
    async function reload() {
      setAppConfig(settingContext.appConfig);
    }
    reload();
  }, [settingContext.appConfig]);

  return (
    <div>
      <label className='title'>App Config</label>
      <div className='setting-container'>
        <div className='setting'>
          <label>Model Provider:</label>
          <select value={appConfig.modelProvider} onChange={(e: ChangeEvent<HTMLSelectElement>) => {
            setAppConfig(prev => ({ ...prev, modelProvider: e.target.value }));
          }}>{settingContext.modelProviders.map(modelProvider => (
            <option key={modelProvider} value={modelProvider}>{modelProvider}</option>
          ))}
          </select>
        </div>
        <div className='setting'>
          <label>Tool Set:</label>
          <select value={appConfig.toolSet} onChange={(e: ChangeEvent<HTMLSelectElement>) => {
            setAppConfig(prev => ({ ...prev, toolSet: e.target.value }));
          }}>{settingContext.toolSets.map(toolSet => (
            <option key={toolSet} value={toolSet}>{toolSet}</option>
          ))}
          </select>
        </div>
        <div className='setting'>
          <label>Data Dir:</label>
          <select value={appConfig.dataDir} onChange={(e: ChangeEvent<HTMLSelectElement>) => {
            setAppConfig(prev => ({ ...prev, dataDir: e.target.value }));
          }}>{settingContext.dataDirs.map(dataDir => (
            <option key={dataDir} value={dataDir}>{dataDir}</option>
          ))}
          </select>
          <button onClick={handleIndexData}>Index</button>
        </div>
        <div className='setting'>
          <label>MCP server:</label>
          <select value={appConfig.mcpServer} onChange={(e: ChangeEvent<HTMLSelectElement>) => {
            setAppConfig(prev => ({ ...prev, mcpServer: e.target.value }));
          }}>{settingContext.mcpServers.map(mcpServer => (
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
