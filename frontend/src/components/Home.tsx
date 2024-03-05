import React, { Component, ChangeEvent, MouseEvent } from 'react';
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

  async fetchData() {
    return fetch('http://localhost:5000/data').then(response => response.json());
  }

  async query(data: string, text: string) {
    return fetch(`http://localhost:5000/query?data=${data}&text=${text}`).then(response => response.text());
  }

  initData() {
    this.fetchData().then(dataList => {
      const keys = Object.keys(dataList).map((data) => {
        return data;
      });
      this.setState({ dataList: keys })
    });
  }

  handleSubmitRequest = async (e: MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    const { data, request } = this.state;

    this.query(data, request).then(response => {
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
              <input type="text"
                value={request}
                onChange={(e: ChangeEvent<HTMLInputElement>) => {
                  this.setState({ request: e.target.value });
                }}
                style={{ width: '70%' }}
              />
              <button onClick={this.handleSubmitRequest}>Submit</button>
            </div>
          </div>
        </div>
      </div >
    );
  }
}

export default Home;
