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
      textareaRef.current?.form?.dispatchEvent(
        new Event("submit", { cancelable: true, bubbles: true })
      );
    }
  };

  useEffect(() => {
    if (chatConfig?.starterQuestions?.length) {
      setInput(chatConfig.starterQuestions[0]);
    }
  }, [chatConfig.starterQuestions]);

  useEffect(() => {
    autoResize();
  }, []);

  return (
    <form onSubmit={handleSubmit}>
      <div className="question-bar">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          placeholder="Type your question..."
        />
        <button type="submit">
          <Send size={16} color="#ffffff" />
        </button>
      </div>
    </form>
  );
}
