import { Component, ChangeEvent, FormEvent, MouseEvent } from 'react';
import { Link } from 'react-router-dom';
import { getBeBaseUrl, fetchConfig, fetchModelConfig, fetchDataConfig, query, fetchChrunk } from '../services/backend'
import './Common.css';
import './Home.css';

interface Node {
  id: string;
  file_name: string;
}

interface Response {
  text: string;
  sources: Node[];
}

interface HomeState {
  modelProvider: string;
  embedModel: string;
  chatModel: string;
  dataDirs: string[];
  dataDir: string;
  dataConfig: any;
  request: string;
  response: Response;
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
      response: { text: '', sources: [] },
    };
  }

  componentDidMount() {
    this.initConfig()
    // this.initData();
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
      console.log(dataDir);
      console.log(dataConfig);
      const defaultQuestion = dataConfig[dataDir].default_question;
      this.setState({ request: defaultQuestion });
    });
  }

  handleQuestion = async (e: FormEvent) => {
    e.preventDefault();
    const { dataDir, request } = this.state;

    query(dataDir, request).then(response => {
      this.setState({ response: response });
    });
  }

  viewChrunk = (e: MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    const { dataDir } = this.state;
    const id = (e.target as HTMLButtonElement).id
    fetchChrunk(dataDir, id).then(source => {
      alert(source['text']);
    });
  }

  viewFull = (e: MouseEvent<HTMLButtonElement>) => {
    const { dataDir } = this.state;
    const file_name = (e.target as HTMLButtonElement).id
    const url = `${getBeBaseUrl()}/${dataDir}/files/${file_name}`;
    window.open(url)
  }

  render() {
    const { modelProvider, embedModel, chatModel, dataDir, request, response } = this.state;
    return (
      <div className='container-column'>
        <div className='header'>
          <Link to='/legacy/setting'>Setting</Link>
        </div>
        <h1 className='title'>RAG Q&A</h1>
        <div className='container'>
          <label className='config-lable'>Model Provider:</label>
          <input value={modelProvider} readOnly style={{ maxWidth: '60px' }} />
          <label className='config-lable'>Embed Model: </label>
          <input value={embedModel} readOnly />
          <label className='config-lable'>Chat Model: </label>
          <input value={chatModel} readOnly />
          <label className='config-lable'>Data Dir:</label>
          <input value={dataDir} readOnly />
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
            <label>Answer</label>
            <div>
              <textarea value={response.text} readOnly rows={10} style={{ width: '100%' }} />
            </div>
          </div>
          <div className='reference-block'>
            <label>Reference</label>
            <div>
              {response.sources.map(source => (
                <li key={source.id}>
                  <label style={{ marginRight: '10px' }}>{source.file_name}</label>
                  <button id={source.id} onClick={this.viewChrunk}>chunk</button>
                  <button id={source.file_name} onClick={this.viewFull}>full</button>
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
