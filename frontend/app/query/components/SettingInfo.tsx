import { useSetting } from "@/context/setting-context";

import '../Home.css';
import './SettingInfo.css';

export default function SettingInfo() {
  const { appConfig: settingInfo, modelConfig } = useSetting();

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
