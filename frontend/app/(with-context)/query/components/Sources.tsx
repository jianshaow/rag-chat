"use client";

import { useSetting } from '@/context/setting-context';
import { getBeBaseUrl } from '@/lib/backend';
import { MouseEvent } from 'react';
import { useQuery } from "../context/query-context";
import './Question.css';

export default function Sources() {
  const { sources } = useQuery();
  const { appConfig: settingInfo } = useSetting();

  const viewFull = (e: MouseEvent<HTMLButtonElement>) => {
    const file_name = (e.target as HTMLButtonElement).id
    const url = `${getBeBaseUrl()}/api/files/${settingInfo?.dataDir}/${file_name}`;
    window.open(url)
  }

  return (
    <div className='reference-block'>
      <label>Reference</label>
      <div>
        {sources.map(source => (
          <li key={source.id}>
            <label style={{ marginRight: '10px' }}>{source.metadata["file_name"] as string}</label>
            <button id={source.id} onClick={(e: MouseEvent<HTMLButtonElement>) => {
              alert(source.text);
            }}>chunk</button>
            <button id={source.metadata["file_name"] as string} onClick={viewFull}>full</button>
          </li>
        ))}
      </div>
    </div>
  );
}
