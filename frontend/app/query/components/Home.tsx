import { SourceNode } from '@llamaindex/chat-ui';
import { ChangeEvent, Component, FormEvent, MouseEvent } from 'react';
import { Link } from 'react-router-dom';
import { fetchConfig, fetchDataConfig, fetchModelConfig, getBeBaseUrl, streamQuery } from '../services/backend';
import './Common.css';
import './Home.css';

interface HomeState {
  modelProvider: string;
  embedModel: string;
  chatModel: string;
  dataDirs: string[];
  dataDir: string;
  dataConfig: any;
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
      dataConfig: {},
      dataDirs: [],
      dataDir: '',
      request: '',
      text: "",
      sources: [],
    };
  }

  componentDidMount() {
    this.initConfig()
  }

  initConfig() {
    fetchConfig().then(config => {
      this.setState({
        modelProvider: config.model_provider,
        dataDir: config.data_dir,
      });
      fetchModelConfig(config.model_provider).then(config => {
        this.setState({
          embedModel: config.embed_model,
          chatModel: config.chat_model,
        });
      });
      this.updateData(config.data_dir);
    });
  }

  updateData(dataDir: string) {
    fetchDataConfig().then(dataConfig => {
      const defaultQuestion = dataConfig[dataDir].default_question;
      this.setState({ request: defaultQuestion });
    });
  }

  handleStreamQuestion = async (e: FormEvent) => {
    e.preventDefault();
    const { request } = this.state;
    streamQuery(request, (answer: string) => {
      this.setState({ text: answer })
    }, (sources: SourceNode[]) => {
      this.setState({ sources: sources })
    })
  };

  viewFull = (e: MouseEvent<HTMLButtonElement>) => {
    const { dataDir } = this.state;
    const file_name = (e.target as HTMLButtonElement).id
    const url = `${getBeBaseUrl()}/api/files/${dataDir}/${file_name}`;
    window.open(url)
  }

  render() {
    const { modelProvider, embedModel, chatModel, dataDir, request, text, sources } = this.state;
    return (
      <div className='container-column' style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <div className='header'>
          <Link to='/setting'>Setting</Link>
        </div>
        <h1 className='title'>RAG Q&A</h1>
        <div className='container'>
          <label className='config-lable'>Model Provider:</label>
          <input value={modelProvider} readOnly style={{ maxWidth: '80px' }} />
          <label className='config-lable'>Data Dir:</label>
          <input value={dataDir} readOnly style={{ maxWidth: '100px' }} />
          <label className='config-lable'>Embed Model: </label>
          <input value={embedModel} readOnly />
          <label className='config-lable'>Chat Model: </label>
          <input value={chatModel} readOnly />
        </div>
        <div className='container-column'>
          <div className='question-block'>
            <label>Question</label>
            <form onSubmit={this.handleStreamQuestion}>
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
            <label>Answer</label>
            <div>
              <textarea value={text} readOnly rows={10} style={{ width: '100%' }} />
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
