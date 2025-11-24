"use client";

import { useSetting } from '@/(query)/context/setting-context';
import {
  fetchChatModels,
  fetchEmbedModels,
  updateModelConfig
} from '@/lib/backend';
import { ModelConfig } from '@/types/config';
import { ChangeEvent, MouseEvent, useEffect, useState } from 'react';
import '../../cquery.module.css';
import '../page.module.css';

export default function ModelConfigSetting() {
  const settingContext = useSetting();

  const [embedModels, setEmbedModels] = useState<string[]>([]);
  const [chatModels, setChatModels] = useState<string[]>([]);
  const [modelConfig, setModelConfig] = useState<ModelConfig>(settingContext.modelConfig);

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

  const handleReloadModels = async (e: MouseEvent) => {
    fetchEmbedModels(true).then((models) => {
      if (!models.includes(modelConfig.embedModel)) {
        models.push(modelConfig.embedModel);
      }
      setEmbedModels(models);
    });
    fetchChatModels(true).then((models) => {
      if (!models.includes(modelConfig.chatModel)) {
        models.push(modelConfig.chatModel);
      }
      setChatModels(models);
    });
  };

  const handleSaveModelConfig = async (e: MouseEvent) => {
    const config = {
      'embed_model': modelConfig.embedModel,
      'chat_model': modelConfig.chatModel,
    };
    updateModelConfig(settingContext.appConfig.modelProvider, JSON.stringify(config)).then(() => {
      alert('Model Config Saved!')
    })
  };

  useEffect(() => {
    initEmbedModels();
    initChatModels();
    setModelConfig(settingContext.modelConfig);
  }, [settingContext.modelConfig]);

  return (
    <div>
      <label className='title'>Model Config</label>
      <div className='setting-container'>
        <div className='setting'>
          <label>Embed Model: </label>
          <select value={modelConfig.embedModel} onChange={(e: ChangeEvent<HTMLSelectElement>) => {
            setModelConfig(prev => ({ ...prev, embedModel: e.target.value }));
          }}>{embedModels.map(model => (
            <option key={model} value={model}>{model}</option>
          ))}
          </select>
        </div>
        <div className='setting'>
          <label>Chat Model: </label>
          <select value={modelConfig.chatModel} onChange={(e: ChangeEvent<HTMLSelectElement>) => {
            setModelConfig(prev => ({ ...prev, chatModel: e.target.value }));
          }}>{chatModels.map(model => (
            <option key={model} value={model}>{model}</option>
          ))}
          </select>
        </div>
        <div className='setting'>
          <button onClick={handleSaveModelConfig}>Save</button>
          <button onClick={handleReloadModels}>Reload Models</button>
        </div>
      </div>
    </div>
  );
}
