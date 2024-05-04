import { Component, ChangeEvent, FormEvent } from 'react';
import { Link } from 'react-router-dom';
import { fetchConfig, fetchData, query } from '../services/backend'
import './Common.css';
import './Home.css';

interface HomeState {
  modelSpec: string;
  dataList: string[];
  data: string;
  request: string;
  response: string;
}

class Home extends Component<{}, HomeState> {
  constructor(props: {}) {
    super(props);
    this.state = { modelSpec: "", dataList: [], data: '', request: '', response: '' };
    this.initConfig()
    this.initData();
  }

  initConfig() {
    fetchConfig().then(config => {
      this.setState({
        modelSpec: config.model_spec,
      });
    });
  }

  initData() {
    fetchData().then(dataList => {
      this.setState({ dataList: dataList, data: dataList[0] });
    });
  }

  handleQuestion = async (e: FormEvent) => {
    e.preventDefault();
    const { data, request } = this.state;

    query(data, request).then(response => {
      this.setState({ response: response });
    });
  }

  render() {
    const { modelSpec, dataList, data, request, response } = this.state;
    return (
      <div className='container-column'>
        <div className='header'>
          <Link to='/setting'>Setting</Link>
        </div>
        <h1 className='title'>RAG Chat</h1>
        <div className='container'>
          <label className='config-lable'>Model Spec: </label>
          <input value={modelSpec} readOnly style={{ marginRight: '5px' }} />
          <label className='config-lable'>Data: </label>
          <select value={data} onChange={(e: ChangeEvent<HTMLSelectElement>) => {
            this.setState({ data: e.target.value });
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
              <textarea value={response} readOnly rows={20} style={{ width: '100%' }} />
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Home;
