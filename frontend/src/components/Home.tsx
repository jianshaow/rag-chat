import { Component, ChangeEvent, FormEvent } from 'react';
import { fetchData, query } from '../services/backend'
import './Common.css';
import './Home.css';

interface HomeState {
  dataList: string[];
  data: string;
  request: string;
  response: string;
}

class Home extends Component<{}, HomeState> {
  constructor(props: {}) {
    super(props);
    this.state = { dataList: [], data: "__root", request: "", response: "" }
    this.initData()
  }

  initData() {
    fetchData().then(dataList => {
      this.setState({ dataList: dataList })
    });
  }

  handleSubmitRequest = async (e: FormEvent) => {
    e.preventDefault();
    const { data, request } = this.state;

    query(data, request).then(response => {
      this.setState({ response: response });
    });
  }

  render() {
    const { dataList, data, request, response } = this.state;
    return (
      <div className="container">
        <div className="center">
          <div>
            <h1>RAG Chat</h1>
            <div>
              <label>Docs: </label>
              <select value={data} onChange={(e: ChangeEvent<HTMLSelectElement>) => {
                this.setState({ data: e.target.value })
              }}>{dataList.map(data => (
                <option key={data} value={data}>{data}</option>
              ))}
              </select>
            </div>
            <label>Answer</label>
            <div>
              <textarea value={response} readOnly rows={10} />
            </div>
            <div className="center">
              <label>Question: </label>
              <form onSubmit={this.handleSubmitRequest}>
                <input type="text"
                  value={request}
                  onChange={(e: ChangeEvent<HTMLInputElement>) => {
                    this.setState({ request: e.target.value });
                  }}
                  style={{ width: '70%' }}
                />
                <button type="submit">Submit</button>
              </form>
            </div>
          </div>
        </div>
      </div >
    );
  }
}

export default Home;
