import { SourceNode } from "@llamaindex/chat-ui/widgets";
import React, { ChangeEvent, Component, FormEvent, MouseEvent } from 'react';
import { Link } from 'react-router-dom';
import { fetchChatConfig, fetchConfig, fetchModelConfig, getBeBaseUrl, query, streamQuery } from '../services/backend';
import './Common.css';
import './Home.css';

interface HomeState {
  modelProvider: string;
  embedModel: string;
  chatModel: string;
  toolSet: string;
  dataDirs: string[];
  dataDir: string;
  dataConfig: any;
  mcpUrl: string;
  agentic: boolean;
  streaming: boolean;
  request: string;
  text: string;
  sources: SourceNode[];
}

class Home extends Component<{}, HomeState> {
  constructor(props: {}) {
    super(props);
    this.state = {
      modelProvider: '',
      embedModel: '',
      chatModel: '',
      toolSet: '',
      dataConfig: {},
      dataDirs: [],
      dataDir: '',
      mcpUrl: '',
      agentic: true,
      streaming: true,
      request: '',
      text: '',
      sources: [],
    };
  }

  textRef = React.createRef<HTMLTextAreaElement>();

  componentDidMount() {
    this.initConfig();
  }

  initConfig() {
    fetchConfig().then(config => {
      this.setState({
        modelProvider: config.model_provider,
        dataDir: config.data_dir,
        toolSet: config.tool_set,
        mcpUrl: config.mcp_url,
      });
      fetchModelConfig(config.model_provider).then(config => {
        this.setState({
          embedModel: config.embed_model,
          chatModel: config.chat_model,
        });
      });
      this.initChatConfig();
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
        if (this.textRef.current) {
          this.textRef.current.scrollTop = this.textRef.current.scrollHeight;
        }
      }, (sources: SourceNode[]) => {
        this.setState({ sources: sources });
      });
    } else {
      query(request).then(response => {
        console.log(response);
        this.setState({ text: response.answer, sources: response.sources });
        if (this.textRef.current) {
          this.textRef.current.scrollTop = this.textRef.current.scrollHeight;
        }
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
    const { modelProvider, embedModel, chatModel, toolSet, dataDir, mcpUrl, agentic, streaming, request, text, sources } = this.state;
    return (
      <div className='main-frame'>
        <div className='header'>
          <Link to='/setting'>Setting</Link>
        </div>
        <h1 className='title'>RAG Q&A</h1>
        <div className='container-column'>
          <label>Model Info</label>
          <div className='info-block'>
            <label>Model Provider:</label>
            <input value={modelProvider} readOnly style={{ maxWidth: '60px' }} />
            <label>Embed Model:</label>
            <input value={embedModel} readOnly />
            <label>Chat Model:</label>
            <input value={chatModel} readOnly />
          </div>
          <label>Tools Info</label>
          <div className='info-block'>
            <label>Tool Set:</label>
            <input value={toolSet} readOnly style={{ maxWidth: '100px' }} />
            <label>Data Dir:</label>
            <input value={dataDir} readOnly style={{ maxWidth: '100px' }} />
            <label className='config-lable'>MCP URL:</label>
            <input value={mcpUrl} readOnly />
          </div>
        </div>
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
          <div className='answer-block'>
            <div className='between-container'>
              <label>Answer</label>
              <div className='right-group'>
                <label className='config-lable'>Agentic: </label>
                <input type='checkbox' onChange={(e: ChangeEvent<HTMLInputElement>) => {
                  this.setState({ agentic: e.target.checked });
                }} checked={agentic} />
                <label className='config-lable'>Streaming: </label>
                <input type='checkbox' onChange={(e: ChangeEvent<HTMLInputElement>) => {
                  this.setState({ streaming: e.target.checked });
                }} checked={streaming} disabled={agentic} />
              </div>
            </div>
            <div>
              <textarea ref={this.textRef} value={text} readOnly rows={10} style={{ width: '100%' }} />
            </div>
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
