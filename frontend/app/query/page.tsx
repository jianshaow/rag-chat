"use client";

import Link from 'next/link';
import { ConfigProvider } from "../context/config-context";
import '../styles/common.css';
import Answer from "./components/Answer";
import EventViewer from "./components/Events";
import MarkdownViewer from "./components/Markdown";
import QueryForm from "./components/QueryForm";
import QuerySection from "./components/QuerySection";
import Question from "./components/Question";
import SettingInfo from './components/SettingInfo';
import Sources from "./components/Sources";
import './Home.css';

export default function Page() {
  return (
    <ConfigProvider>
      <div className='main-frame'>
        <div className='header'>
          <Link href='/setting'>Setting</Link>
        </div>
        <h1 className='title'>RAG Q&A Demo</h1>
        <SettingInfo />
        <QuerySection>
          <Question>
            <QueryForm />
          </Question>
          <EventViewer height={'4em'} />
          <Answer>
            <MarkdownViewer height={300} />
          </Answer>
          <Sources />
        </QuerySection>
      </div>
    </ConfigProvider>
  );
}