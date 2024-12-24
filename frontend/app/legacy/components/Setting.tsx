import { Component, ChangeEvent, MouseEvent } from 'react';
import { Link } from 'react-router-dom';
import {
  getBeBaseUrl,
  setBeBaseUrl,
  fetchConfig,
  updateConfig,
  fetchModelProviders,
  updateModelConfig,
  fetchModelConfig,
  fetchEmbedModels,
  fetchChatModels,
} from '../services/backend'
import './Common.css';
import './Setting.css';

interface SettingState {
  beBaseUrl: string;
  dataBaseDir: string;
  chromaBaseDir: string;
  modelProviders: string[];
  modelProvider: string;
  embedModels: string[];
  embedModel: string;
  chatModels: string[];
  chatModel: string;
}

class Setting extends Component<{}, SettingState> {
  constructor(props: {}) {
    super(props);
    this.state = {
      beBaseUrl: getBeBaseUrl(),
      dataBaseDir: '',
      chromaBaseDir: '',
      modelProviders: [],
      modelProvider: '',
      embedModels: [],
      embedModel: '',
      chatModels: [],
      chatModel: '',
    };
  }

  componentDidMount() {
    this.initSetting();
  }

  initSetting() {
    this.initConfig();
    this.initModelProviders();
    this.initEmbedModels()
    this.initChatModels();
  }

  initModelProviders() {
    fetchModelProviders().then((modelProviders) => {
      this.setState({ modelProviders: modelProviders });
    });
  }

  initEmbedModels() {
    fetchEmbedModels(false).then((models) => {
      const { embedModel } = this.state;
      if (!models.includes(embedModel)) {
        models.push(embedModel);
      }
      this.setState({ embedModels: models });
    });
  }

  initChatModels() {
    fetchChatModels(false).then((models) => {
      const { chatModel } = this.state;
      if (!models.includes(chatModel)) {
        models.push(chatModel);
      }
      this.setState({ chatModels: models });
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
    const url = `${protocol}//${host}/legacy`;
    this.setState({ beBaseUrl: url })
  };

  initConfig() {
    fetchConfig().then(config => {
      this.setState({
        modelProvider: config.model_provider,
        dataBaseDir: config.data_base_dir,
        chromaBaseDir: config.chroma_base_dir,
      });
      this.reloadApiConfig(config.model_provider);
    });
  }

  reloadApiConfig(modelProvider: string) {
    fetchModelConfig(modelProvider).then((config) => {
      console.log(config);
      this.setState({
        embedModel: config.embed_model,
        chatModel: config.chat_model,
      });
    })
  }

  handleReloadModels = async (e: MouseEvent) => {
    fetchEmbedModels(true).then((models) => {
      const { embedModel } = this.state;
      if (!models.includes(embedModel)) {
        models.push(embedModel);
      }
      this.setState({ embedModels: models });
    });
    fetchChatModels(true).then((models) => {
      const { chatModel } = this.state;
      if (!models.includes(chatModel)) {
        models.push(chatModel);
      }
      this.setState({ chatModels: models });
    });
  };

  handleSaveConfig = async (e: MouseEvent) => {
    const { modelProvider, dataBaseDir, chromaBaseDir } = this.state
    const config = {
      'model_provider': modelProvider,
      'data_base_dir': dataBaseDir,
      'chroma_base_dir': chromaBaseDir,
    };
    updateConfig(JSON.stringify(config)).then(() => {
      alert('Setting Saved!');
      this.initEmbedModels();
      this.initChatModels();
      this.reloadApiConfig(modelProvider);
    })
  };

  handleSaveModelConfig = async (e: MouseEvent) => {
    const { modelProvider, embedModel, chatModel } = this.state
    const config = {
      'embed_model': embedModel,
      'chat_model': chatModel,
    };
    updateModelConfig(modelProvider, JSON.stringify(config)).then(() => {
      alert('Model Config Saved!')
    })
  };

  render() {
    const { beBaseUrl, dataBaseDir, chromaBaseDir, modelProviders, modelProvider, embedModel, chatModel, embedModels, chatModels } = this.state;

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
              <label className='config-lable'>Model Provider: </label>
              <select value={modelProvider} onChange={(e: ChangeEvent<HTMLSelectElement>) => {
                this.setState({ modelProvider: e.target.value })
              }}>{modelProviders.map(modelProvider => (
                <option key={modelProvider} value={modelProvider}>{modelProvider}</option>
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
              <label className='config-lable'>Embed Model: </label>
              <select value={embedModel} onChange={(e: ChangeEvent<HTMLSelectElement>) => {
                this.setState({ embedModel: e.target.value })
              }}>{embedModels.map(model => (
                <option key={model} value={model}>{model}</option>
              ))}
              </select>
            </div>
          </div>
          <div className='setting'>
            <div>
              <label className='config-lable'>Chat Model: </label>
              <select value={chatModel} onChange={(e: ChangeEvent<HTMLSelectElement>) => {
                this.setState({ chatModel: e.target.value })
              }}>{chatModels.map(model => (
                <option key={model} value={model}>{model}</option>
              ))}
              </select>
            </div>
          </div>
          <div className='setting'>
            <div>
              <button onClick={this.handleSaveModelConfig}>Save</button>
              <button onClick={this.handleReloadModels}>Reload Models</button>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Setting;