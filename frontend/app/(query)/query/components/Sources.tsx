"use client";

import { SourceNode } from "@llamaindex/chat-ui/widgets";
import * as Popover from "@radix-ui/react-popover";
import { ExternalLink, Eye } from "lucide-react";
import { useQuery } from "../context/query-context";
import "../query.css";

export default function Sources() {
  const { sources } = useQuery();

  const truncateText = (text: string, maxLength: number) =>
    text.length > maxLength ? text.slice(0, maxLength) + "..." : text;

  const viewFull = async (source: SourceNode) => {
    const metadata = source.metadata;
    const sourceType = metadata["source_type"] as string;
    // const fileName = metadata["file_name"] as string;
    const url = source.url || "";
    if ("mcp" === sourceType) {
      const args = metadata["tool_kwargs"];
      const newWindow = window.open("", "_blank");
      if (!newWindow) {
        alert("Popup blocked! Please allow popups for this site.");
        return;
      }
      newWindow.document.body.innerText = "Loading...";
      const res = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(args),
      });
      const text = await res.text();
      const blob = new Blob([text], { type: "text/plain" });
      const blobUrl = URL.createObjectURL(blob);
      newWindow.location.href = blobUrl;
      return
    }
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
                id={source.id}
                onClick={() => viewFull(source)}
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
