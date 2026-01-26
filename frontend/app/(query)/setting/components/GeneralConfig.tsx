"use client";

import { useSetting } from '@/(query)/context/setting-context';
import { storeBeBaseUrl } from '@/lib/backend';
import { ChangeEvent, useEffect, useState } from 'react';
import '../../common.css';
import '../setting.css';

export default function GeneralConfigSetting() {
  const settingContext = useSetting();
  const [beBaseUrl, setBeBaseUrl] = useState<string>(settingContext.beBaseUrl);

  const handleSaveBeBaseUrl = async () => {
    storeBeBaseUrl(beBaseUrl);
    alert('Backend Base URL Saved!');
    settingContext.setBeBaseUrl(beBaseUrl);
  };

  const handleDetectBeBaseUrl = async () => {
    const protocol = window.location.protocol;
    const host = window.location.host;
    const url = `${protocol}//${host}`;
    setBeBaseUrl(url);
  };

  useEffect(() => {
    async function reload() {
      setBeBaseUrl(settingContext.beBaseUrl);
    }
    reload();
  }, [settingContext.beBaseUrl]);

  return (
    <div>
      <label className='title'>General</label>
      <div className='setting-container'>
        <div className='setting'>
          <label>Backend Base URL:</label>
          <input
            type='text'
            value={beBaseUrl}
            onChange={(e: ChangeEvent<HTMLInputElement>) => {
              setBeBaseUrl(e.target.value);
            }}
          />
          <button onClick={handleSaveBeBaseUrl}>Save</button>
          <button onClick={handleDetectBeBaseUrl}>Detect</button>
        </div>
      </div>
    </div>
  );
}
