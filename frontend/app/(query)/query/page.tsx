import Link from 'next/link';
import '../common.css';
import Answer from "./components/Answer";
import Events from "./components/Events";
import Markdown from "./components/Markdown";
import QueryForm from "./components/QueryForm";
import QuerySection from "./components/QuerySection";
import Question from "./components/Question";
import SettingInfo from './components/SettingInfo';
import Sources from "./components/Sources";
import './query.css';

export default function Page() {
  return (
    <div className='main-frame'>
      <div className='text-right my-2'>
        <Link href='/setting'>Setting</Link>
      </div>
      <h1>RAG / Agent Q&A Demo</h1>
      <SettingInfo />
      <QuerySection>
        <Question>
          <QueryForm />
        </Question>
        <Events height={'4em'} />
        <Answer>
          <Markdown height={200} />
        </Answer>
        <Sources />
      </QuerySection>
    </div>
  );
}