"use client";

import { useSetting } from "@/(query)/context/setting-context";
import * as Collapsible from "@radix-ui/react-collapsible";
import { ChevronDown } from "lucide-react";
import { useState } from "react";
import "../query.css";

export default function SettingInfo() {
  const { appConfig: settingInfo, modelConfig } = useSetting();
  const [open, setOpen] = useState(false);

  return (
    <Collapsible.Root open={open} onOpenChange={setOpen}>
      <Collapsible.Trigger asChild>
        <div className="flex items-center gap-1.5 cursor-pointer text-base font-normal">
          <span>{open ? "Hide Setting" : "Show Setting"}</span>
          <ChevronDown
            size={18}
            className={`transition-transform duration-200 ${open ? "rotate-180" : "rotate-0"}`}
          />
        </div>
      </Collapsible.Trigger>

      <Collapsible.Content>
        <div className="info-block mt-2">
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
      </Collapsible.Content>

      {!open && <div className="mb-2" />}
    </Collapsible.Root>
  );
}
