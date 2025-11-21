"use client";

import { useConfig } from "@/context/config-context";
import { query, streamQuery } from "@/lib/backend";
import { SourceNode } from "@llamaindex/chat-ui/widgets";
import { ChangeEvent, FormEvent, useEffect, useState } from "react";
import { useQuery } from "../context/query-context";
import './Question.css';

export default function QueryForm() {
  const { chatConfig } = useConfig();
  const { agentic, streaming, setEvents, setSources, setAnswer } = useQuery();
  const [input, setInput] = useState('');

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    if (agentic || streaming) {
      streamQuery(input, agentic, (answer: string) => {
        setAnswer(answer);
      }, (title: string) => {
        setEvents((prevEvents) => [...prevEvents, title]);
      }, (newSources: SourceNode[]) => {
        setSources((prevSources) => [...prevSources, ...newSources]);
      });
    } else {
      query(input).then(response => {
        setAnswer(response.answer);
        setSources(response.sources);
      });
    }
  }

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
  }

  useEffect(() => {
    if (chatConfig && chatConfig.starterQuestions && chatConfig.starterQuestions.length > 0) {
      setInput(chatConfig.starterQuestions[0]);
    }
  }, []);

  return (
    <form onSubmit={handleSubmit}>
      <div className='question-bar'>
        <input type='text' value={input}
          onChange={handleInputChange}
          style={{ width: '100%' }} />
        <button type='submit'>Submit</button>
      </div>
    </form>
  );
}
