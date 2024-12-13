import { Component, ChangeEvent, MouseEvent } from 'react';
import { Link } from 'react-router-dom';
import {
  getBeBaseUrl,
  setBeBaseUrl,
  fetchConfig,
  updateConfig,
  fetchApiSpecs,
  updateApiConfig,
  fetchApiConfig,
  fetchModels,
} from '../services/backend'
import './Common.css';
import './Setting.css';

interface SettingState {
  beBaseUrl: string;
  dataBaseDir: string;
  chromaBaseDir: string;
  apiSpecs: string[];
  apiSpec: string;
  models: string[];
  model: string;
}

class Setting extends Component<{}, SettingState> {
  constructor(props: {}) {
    super(props);
    this.state = {
      beBaseUrl: getBeBaseUrl(),
      dataBaseDir: '',
      chromaBaseDir: '',
      apiSpecs: [],
      apiSpec: '',
      model: '',
      models: [],
    };
  }

  componentDidMount() {
    this.initSetting();
  }

  initSetting() {
    this.initConfig();
    this.initApiSpecs();
    this.initModels();
  }

  initApiSpecs() {
    fetchApiSpecs().then((apiSpecs) => {
      this.setState({ apiSpecs: apiSpecs });
    });
  }

  initModels() {
    fetchModels(false).then((models) => {
      const { model } = this.state;
      if (!models.includes(model)) {
        models.push(model);
      }
      this.setState({ models: models });
    });
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
        apiSpec: config.api_spec,
        dataBaseDir: config.data_base_dir,
        chromaBaseDir: config.chroma_base_dir,
      });
      this.reloadApiConfig(config.api_spec);
    });
  }

  reloadApiConfig(apiSpec: string) {
    fetchApiConfig(apiSpec).then((config) => {
      console.log(config);
      this.setState({
        model: config.model,
      });
    })
  }

  handleReloadModels = async (e: MouseEvent) => {
    fetchModels(true).then((models) => {
      const { model } = this.state;
      if (!models.includes(model)) {
        models.push(model);
      }
      this.setState({ models: models });
    });
  };

  handleSaveConfig = async (e: MouseEvent) => {
    const { apiSpec, dataBaseDir, chromaBaseDir } = this.state
    const config = {
      'api_spec': apiSpec,
      'data_base_dir': dataBaseDir,
      'chroma_base_dir': chromaBaseDir,
    };
    updateConfig(JSON.stringify(config)).then(() => {
      alert('Setting Saved!');
      this.initModels();
      this.reloadApiConfig(apiSpec);
    })
  };

  handleSaveApiConfig = async (e: MouseEvent) => {
    const { apiSpec, model } = this.state
    const config = {
      'model': model,
    };
    updateApiConfig(apiSpec, JSON.stringify(config)).then(() => {
      alert('API Config Saved!')
    })
  };

  render() {
    const { beBaseUrl, dataBaseDir, chromaBaseDir, apiSpecs, apiSpec, models, model } = this.state;

    return (
      <div className='container-column'>
        <div className='header'>
          <Link to='/legacy'>Return Home</Link>
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
              <label className='config-lable'>API Spec: </label>
              <select value={apiSpec} onChange={(e: ChangeEvent<HTMLSelectElement>) => {
                this.setState({ apiSpec: e.target.value })
              }}>{apiSpecs.map(apiSpec => (
                <option key={apiSpec} value={apiSpec}>{apiSpec}</option>
              ))}
              </select>
            </div>
          </div>
          <div className='setting'>
            <div>
              <button onClick={this.handleSaveConfig}>Save</button>
            </div>
          </div>
        </div>
        <label className='title'>API Config</label>
        <div className='setting-container'>
          <div className='setting'>
            <div>
              <label className='config-lable'>Chat Model: </label>
              <select value={model} onChange={(e: ChangeEvent<HTMLSelectElement>) => {
                this.setState({ model: e.target.value })
              }}>{models.map(model => (
                <option key={model} value={model}>{model}</option>
              ))}
              </select>
              <button onClick={this.handleReloadModels}>Reload Models</button>
            </div>
          </div>
          <div className='setting'>
            <div>
              <button onClick={this.handleSaveApiConfig}>Save</button>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Setting;