"use client";

import { useSetting } from "@/(query)/context/setting-context";
import { getBeBaseUrl } from "@/lib/backend";
import * as Popover from "@radix-ui/react-popover";
import { ExternalLink, Eye } from "lucide-react";
import { useQuery } from "../context/query-context";
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
                  <button title="Show chunk">
                    <Eye size={16} color="#0070f3" />
                  </button>
                </Popover.Trigger>

                <Popover.Content
                  side="top"
                  align="start"
                  sideOffset={8}
                  className="source-popover"
                >
                  {truncateText(source.text, 400)}
                  <Popover.Arrow className="source-popover-arrow" />
                </Popover.Content>
              </Popover.Root>

              <button
                id={source.metadata["file_name"] as string}
                onClick={() => viewFull(source.metadata["file_name"] as string)}
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
