import { Component, ChangeEvent, MouseEvent } from 'react';
import { Link } from 'react-router-dom';
import {
  getBeBaseUrl,
  setBeBaseUrl,
  fetchConfig,
  updateConfig,
} from '../services/backend'
import './Common.css';
import './Setting.css';

interface SettingState {
  beBaseUrl: string;
  dataBaseDir: string;
  chromaBaseDir: string;
  modelSpec: string;
}

class Setting extends Component<{}, SettingState> {
  constructor(props: {}) {
    super(props);
    this.state = {
      beBaseUrl: getBeBaseUrl(),
      modelSpec: '',
      dataBaseDir: '',
      chromaBaseDir: '',
    };
    this.initSetting();
  }

  initSetting() {
    this.initConfig();
  }

  handleSaveBeBaseUrl = async (e: MouseEvent) => {
    const { beBaseUrl } = this.state;
    setBeBaseUrl(beBaseUrl);
    this.initSetting();
  };

  handleDetectBeBaseUrl = async (e: MouseEvent) => {
    const protocol = window.location.protocol;
    const host = window.location.host;
    const url = `${protocol}//${host}`;
    this.setState({ beBaseUrl: url })
  };

  initConfig() {
    fetchConfig().then(config => {
      this.setState({
        modelSpec: config.model_spec,
        dataBaseDir: config.data_base_dir,
        chromaBaseDir: config.chroma_base_dir,
      });
    });
  }

  handleSaveConfig = async (e: MouseEvent) => {
    const { modelSpec, dataBaseDir, chromaBaseDir } = this.state
    const config = {
      'model_spec': modelSpec,
      'data_base_dir': dataBaseDir,
      'chroma_base_dir': chromaBaseDir,
    };
    updateConfig(JSON.stringify(config)).then(() => {
      alert('Setting Saved!')
    })
  };

  render() {
    const { beBaseUrl, dataBaseDir, chromaBaseDir, modelSpec } = this.state;

    return (
      <div className='container-column'>
        <div className='header'>
          <Link to='/'>Return Home</Link>
        </div>
        <h1 className='title'>Settings</h1>
        <div className='setting'>
          <div>
            <label className='config-lable'>Backend Base URL: </label>
            <input
              type='text'
              value={beBaseUrl}
              onChange={(e: ChangeEvent<HTMLInputElement>) => {
                this.setState({ beBaseUrl: e.target.value });
              }}
            />
            <button onClick={this.handleSaveBeBaseUrl}>Save</button>
            <button onClick={this.handleDetectBeBaseUrl}>Detect</button>
          </div>
        </div>
        <label className='title'>Backend</label>
        <div className='setting-container'>
          <div className='setting'>
            <div>
              <label className='config-lable'>Data Base Dir: </label>
              <input
                type='text'
                value={dataBaseDir}
                onChange={(e: ChangeEvent<HTMLInputElement>) => {
                  this.setState({ dataBaseDir: e.target.value });
                }}
              />
            </div>
          </div>
          <div className='setting'>
            <div>
              <label className='config-lable'>Chroma Base Dir: </label>
              <input
                type='text'
                value={chromaBaseDir}
                onChange={(e: ChangeEvent<HTMLInputElement>) => {
                  this.setState({ chromaBaseDir: e.target.value });
                }}
              />
            </div>
          </div>
          <div className='setting'>
            <div>
              <label className='config-lable'>Model Spec: </label>
              <select value={modelSpec} onChange={(e: ChangeEvent<HTMLSelectElement>) => {
                this.setState({ modelSpec: e.target.value })
              }}>
                {modelSpec === '' ? <option>Select a spec</option> : ''}
                <option key='openai' value='openai'>openai</option>
                <option key='gemini' value='gemini'>gemini</option>
              </select>
            </div>
          </div>
          <div className='setting'>
            <div>
              <button onClick={this.handleSaveConfig}>Save Setting</button>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Setting;