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
  dataList: string[];
  dataConfig: any;
  data: string;
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
      dataList: [],
      data: '',
      request: '',
      response: { text: '', sources: [] },
    };
  }

  componentDidMount() {
    this.initConfig()
    this.initData();
  }

  initConfig() {
    fetchConfig().then(config => {
      this.setState({
        modelProvider: config.model_provider,
      });
      fetchModelConfig(config.model_provider).then(config => {
        this.setState({
          embedModel: config.embed_model,
          chatModel: config.chat_model,
        });
      });
    });
  }

  initData() {
    fetchDataConfig().then(dataConfig => {
      const dataList = Object.keys(dataConfig).map((data) => {
        return data;
      });
      const defaultName = dataList[0];
      const defaultQuestion = dataConfig[defaultName].default_question;
      this.setState({ dataConfig: dataConfig, dataList: dataList, data: defaultName, request: defaultQuestion });
    });
  }

  handleQuestion = async (e: FormEvent) => {
    e.preventDefault();
    const { data, request } = this.state;

    query(data, request).then(response => {
      this.setState({ response: response });
    });
  }

  viewChrunk = (e: MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    const { data } = this.state;
    const id = (e.target as HTMLButtonElement).id
    fetchChrunk(data, id).then(source => {
      alert(source['text']);
    });
  }

  viewFull = (e: MouseEvent<HTMLButtonElement>) => {
    const { data } = this.state;
    const file_name = (e.target as HTMLButtonElement).id
    const url = `${getBeBaseUrl()}/${data}/files/${file_name}`;
    window.open(url)
  }

  render() {
    const { modelProvider, embedModel, chatModel, dataConfig, dataList, data, request, response } = this.state;
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
          <label className='config-lable'>Data:</label>
          <select value={data} onChange={(e: ChangeEvent<HTMLSelectElement>) => {
            this.setState({ data: e.target.value, request: dataConfig[e.target.value].default_question });
          }}>{dataList.map(data => (
            <option key={data} value={data}>{data}</option>
          ))}
          </select>
        </div>
        <div className='container-column'>
          <div className='question-block'>
            <label>Question</label>
            <form onSubmit={this.handleQuestion}>
              <input type='text' value={request}
                onChange={(e: ChangeEvent<HTMLInputElement>) => {
                  this.setState({ request: e.target.value });
                }}
                style={{ width: '100%' }} />
              <button type='submit'>Submit</button>
            </form>
          </div>
          <div className='answer-block'>
            <label>Answer</label>
            <div>
              <textarea value={response.text} readOnly rows={20} style={{ width: '100%' }} />
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
