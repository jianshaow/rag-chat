"use client";

import { useSetting } from "@/(query)/context/setting-context";
import { getBeBaseUrl } from "@/lib/backend";
import { useQuery } from "../context/query-context";
import { Eye, ExternalLink } from "lucide-react";
import * as Popover from "@radix-ui/react-popover";
import "../query.css";

export default function Sources() {
  const { sources } = useQuery();
  const { appConfig: settingInfo } = useSetting();

  const truncateText = (text: string, maxLength: number) =>
    text.length > maxLength ? text.slice(0, maxLength) + "..." : text;

  const viewFull = (fileName: string) => {
    const url = `${getBeBaseUrl()}/api/files/${settingInfo?.dataDir}/${fileName}`;
    window.open(url);
  };

  return (
    <div className="sources-block">
      <label>Sources</label>
      <ul>
        {sources.map((source) => (
          <li key={source.id} className="gap-2">
            <div className="source-item">
              <label>{source.metadata["file_name"] as string}</label>
              <Popover.Root>
                <Popover.Trigger asChild>
                  <button
                    style={{
                      background: "none",
                      border: "none",
                      cursor: "pointer",
                      padding: "4px",
                    }}
                    title="Show chunk"
                  >
                    <Eye size={16} color="#0070f3" />
                  </button>
                </Popover.Trigger>
                <Popover.Content
                  side="top"
                  align="start"
                  sideOffset={8}
                  className="source-popover"
                  style={{
                    maxWidth: "300px",
                    maxHeight: "200px",
                    overflowY: "auto",
                    padding: "8px",
                    backgroundColor: "#f9f9f9",
                    border: "1px solid #ccc",
                    borderRadius: "6px",
                    boxShadow: "0 2px 12px rgba(0,0,0,0.2)",
                    whiteSpace: "pre-wrap",
                  }}
                >
                  {truncateText(source.text, 200)}
                  <Popover.Arrow
                    style={{ fill: "#f9f9f9" }}
                  />
                </Popover.Content>
              </Popover.Root>

              <button
                id={source.metadata["file_name"] as string}
                onClick={() => viewFull(source.metadata["file_name"] as string)}
                style={{
                  background: "none",
                  border: "none",
                  cursor: "pointer",
                  padding: "4px",
                }}
                title="View full file"
              >
                <ExternalLink size={16} color="#0070f3" />
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
