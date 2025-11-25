"use client";

import { useSetting } from '@/(query)/context/setting-context';
import { getBeBaseUrl } from '@/lib/backend';
import { MouseEvent } from 'react';
import { useQuery } from "../context/query-context";
import '../query.css';

export default function Sources() {
  const { sources } = useQuery();
  const { appConfig: settingInfo } = useSetting();

  const viewFull = (e: MouseEvent<HTMLButtonElement>) => {
    const file_name = (e.target as HTMLButtonElement).id
    const url = `${getBeBaseUrl()}/api/files/${settingInfo?.dataDir}/${file_name}`;
    window.open(url)
  }

  return (
    <div className='sources-block'>
      <label>Sources</label>
      <ul>
        {sources.map(source => (
          <li key={source.id} className='gap-2'>
            <div className='source-item'>
              <label>{source.metadata["file_name"] as string}</label>
              <button id={source.id} onClick={(e: MouseEvent<HTMLButtonElement>) => {
                alert(source.text);
              }}>chunk</button>
              <button id={source.metadata["file_name"] as string} onClick={viewFull}>full</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
