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
    <Collapsible.Root
      open={open}
      onOpenChange={setOpen}
      className="setting-info"
    >
      <Collapsible.Trigger asChild>
        <div
          style={{
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            gap: "6px",
            fontSize: "16px",
            fontWeight: "normal",
          }}
        >
          <span>{open ? "Hide Setting" : "Show Setting"}</span>

          <ChevronDown
            size={18}
            style={{
              transition: "transform 0.2s ease",
              transform: open ? "rotate(180deg)" : "rotate(0deg)",
            }}
          />
        </div>
      </Collapsible.Trigger>

      <Collapsible.Content>
        <div className="info-block" style={{ marginTop: "12px" }}>
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

      {!open && <div style={{ marginBottom: "12px" }} />}
    </Collapsible.Root>
  );
}
