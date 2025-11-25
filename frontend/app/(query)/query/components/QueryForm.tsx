"use client";

import { useSetting } from "@/(query)/context/setting-context";
import { query, streamQuery } from "@/lib/backend";
import { SourceNode } from "@llamaindex/chat-ui/widgets";
import { Send } from "lucide-react";
import { ChangeEvent, FormEvent, useEffect, useRef, useState } from "react";
import { useQuery } from "../context/query-context";
import "../query.css";

export default function QueryForm() {
  const { chatConfig } = useSetting();
  const { agentic, streaming, setEvents, setSources, setAnswer } = useQuery();
  const [input, setInput] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const autoResize = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = textareaRef.current.scrollHeight + "px";
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    // setInput("");
    autoResize();

    if (agentic || streaming) {
      streamQuery(
        input,
        agentic,
        (answer: string) => setAnswer(answer),
        (title: string) => setEvents((prev) => [...prev, title]),
        (newSources: SourceNode[]) => setSources((prev) => [...prev, ...newSources])
      );
    } else {
      query(input).then((response) => {
        setAnswer(response.answer);
        setSources(response.sources);
      });
    }
  };

  const handleInputChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
    autoResize();
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      textareaRef.current?.form?.dispatchEvent(new Event("submit", { cancelable: true, bubbles: true }));
    }
  };

  useEffect(() => {
    if (chatConfig?.starterQuestions?.length) {
      setInput(chatConfig.starterQuestions[0]);
    }
  }, [chatConfig]);

  useEffect(() => {
    autoResize();
  }, []);

  return (
    <form onSubmit={handleSubmit}>
      <div
        className="question-bar"
        style={{
          position: "relative",
          display: "flex",
          alignItems: "flex-end",
        }}
      >
        <textarea
          ref={textareaRef}
          value={input}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          placeholder="Type your question..."
          style={{
            width: "100%",
            resize: "none",
            overflow: "hidden",
            minHeight: "40px",
            lineHeight: "1.5em",
            padding: "6px 48px 6px 10px",
            borderRadius: "8px",
            border: "1px solid #ccc",
            fontSize: "14px",
          }}
        />

        <button
          type="submit"
          style={{
            position: "absolute",
            right: "8px",
            bottom: "8px",
            width: "32px",
            height: "32px",
            borderRadius: "50%",
            backgroundColor: "#888888",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            border: "none",
            cursor: "pointer",
            transition: "all 0.2s ease",
          }}
        >
          <Send
            size={16}
            color="#ffffff"
            style={{
              pointerEvents: "none",
              transition: "transform 0.1s ease",
            }}
          />
        </button>
      </div>
    </form>
  );
}
