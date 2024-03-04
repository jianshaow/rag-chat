import React, { Component, ChangeEvent, MouseEvent } from 'react';
import './Common.css';
import './Home.css';

interface HomeState {
  data: string;
  request: string;
  response: string;
}

class Home extends Component<{}, HomeState> {
  constructor(props: {}) {
    super(props);
    this.state = { data: "__root", request: "", response: "" }
  }

  getData() {
    const data_path = {
      __root: "data",
      en_novel1: "data/en_novel1",
      en_novel2: "data/en_novel2",
      zh_novel1: "data/zh_novel1",
      zh_novel2: "data/zh_novel2"
    };

    const keys = Object.keys(data_path).map((data) => {
      if (data === "__root") {
        return "ROOT";
      }
      return data;
    });

    return keys;
  }

  handleSubmitRequest = async (e: MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    const { request } = this.state;

    this.setState({ response: request });
  }

  render() {
    const { data, request, response } = this.state;
    return (
      <div className="container">
        <div className="center">
          <div>
            <h1>RAG Chat</h1>
            <div>
              <label>Docs: </label>
              <select value={data} onChange={(e: ChangeEvent<HTMLSelectElement>) => {
                this.setState({ data: e.target.value })
              }}>{this.getData().map(data => (
                <option key={data} value={data}>{data}</option>
              ))}
              </select>
            </div>
            <div style={{ width: '80%' }}>
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
            <label>Answer</label>
            <div>
              <textarea value={response} readOnly rows={10} />
            </div>
          </div>
        </div>
      </div >
    );
  }
}

export default Home;
