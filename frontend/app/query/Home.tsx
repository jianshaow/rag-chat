"use client";

import { SourceNode } from "@llamaindex/chat-ui/widgets";
import Link from 'next/link';
import { ChangeEvent, Component, FormEvent, MouseEvent } from 'react';
import {
  fetchChatConfig,
  fetchConfig,
  getBeBaseUrl,
  query,
  streamQuery
} from '../lib/backend';
import '../styles/common.css';
import EventViewer from "./components/Events";
import MarkdownViewer from './components/Markdown';
import SettingInfo from './components/SettingInfo';
import './Home.css';

interface HomeState {
  dataDir: string;
  agentic: boolean;
  streaming: boolean;
  request: string;
  text: string;
  events: string[];
  sources: SourceNode[];
}

class Home extends Component<{}, HomeState> {
  constructor(props: {}) {
    super(props);
    this.state = {
      dataDir: '',
      agentic: true,
      streaming: true,
      request: '',
      text: '',
      events: [],
      sources: [],
    };
  }

  componentDidMount() {
    this.initConfig();
    this.initChatConfig();
  }

  initConfig() {
    fetchConfig().then(config => {
      this.setState({
        dataDir: config.data_dir,
      })
    });
  }

  initChatConfig() {
    fetchChatConfig().then(chatConfig => {
      console.log(chatConfig);
      const starterQuestion = chatConfig.starterQuestions[0];
      this.setState({ request: starterQuestion });
    });
  }

  handleQuestion = async (e: FormEvent) => {
    e.preventDefault();
    this.setState({ text: '', sources: [] })

    const { request, agentic, streaming } = this.state;

    if (agentic || streaming) {
      streamQuery(request, agentic, (answer: string) => {
        this.setState({ text: answer });
      }, (title: string) => {
        const { events } = this.state;
        this.setState({ events: [...events, title] });
      }, (sources: SourceNode[]) => {
        this.setState({ sources: sources });
      });
    } else {
      query(request).then(response => {
        console.log(response);
        this.setState({ text: response.answer, sources: response.sources });
      });
    }
  }

  viewFull = (e: MouseEvent<HTMLButtonElement>) => {
    const { dataDir } = this.state;
    const file_name = (e.target as HTMLButtonElement).id
    const url = `${getBeBaseUrl()}/api/files/${dataDir}/${file_name}`;
    window.open(url)
  }

  render() {
    const { agentic, streaming, request, text, events, sources } = this.state;
    return (
      <div className='main-frame'>
        <div className='header'>
          <Link href='/setting'>Setting</Link>
        </div>
        <h1 className='title'>RAG Q&A Demo</h1>
        <SettingInfo />
        <div className='container-column'>
          <div className='question-block'>
            <label>Question</label>
            <form onSubmit={this.handleQuestion}>
              <div className='question-bar'>
                <input type='text' value={request}
                  onChange={(e: ChangeEvent<HTMLInputElement>) => {
                    this.setState({ request: e.target.value });
                  }}
                  style={{ width: '100%' }} />
                <button type='submit'>Submit</button>
              </div>
            </form>
          </div>
          <EventViewer events={events} height={'50px'} />
          <div className='answer-block'>
            <div className='between-container'>
              <label>Answer</label>
              <div className='right-group'>
                <label>Agentic: </label>
                <input type='checkbox' onChange={(e: ChangeEvent<HTMLInputElement>) => {
                  this.setState({ agentic: e.target.checked });
                }} checked={agentic} />
                <label>Streaming: </label>
                <input type='checkbox' onChange={(e: ChangeEvent<HTMLInputElement>) => {
                  this.setState({ streaming: e.target.checked });
                }} checked={streaming} disabled={agentic} />
              </div>
            </div>
            <MarkdownViewer content={text} height={300} />
          </div>
          <div className='reference-block'>
            <label>Reference</label>
            <div>
              {sources.map(source => (
                <li key={source.id}>
                  <label style={{ marginRight: '10px' }}>{source.metadata["file_name"] as string}</label>
                  <button id={source.id} onClick={(e: MouseEvent<HTMLButtonElement>) => {
                    alert(source.text);
                  }}>chunk</button>
                  <button id={source.metadata["file_name"] as string} onClick={this.viewFull}>full</button>
                </li>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Home;
