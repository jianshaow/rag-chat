import Link from 'next/link';
import { SettingProvider } from "../../context/setting-context";
import '../styles/common.css';
import Answer from "./components/Answer";
import Events from "./components/Events";
import Markdown from "./components/Markdown";
import QueryForm from "./components/QueryForm";
import QuerySection from "./components/QuerySection";
import Question from "./components/Question";
import SettingInfo from './components/SettingInfo';
import Sources from "./components/Sources";
import './Home.css';

export default function Page() {
  return (
    <SettingProvider>
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
          <Events height={'4em'} />
          <Answer>
            <Markdown height={300} />
          </Answer>
          <Sources />
        </QuerySection>
      </div>
    </SettingProvider>
  );
}