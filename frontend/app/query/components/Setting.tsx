import { ChangeEvent, Component, MouseEvent } from 'react';
import { Link } from 'react-router-dom';
import {
  fetchChatModels,
  fetchConfig,
  fetchDataConfig,
  fetchEmbedModels,
  fetchMcpServers,
  fetchModelConfig,
  fetchModelProviders,
  fetchToolSets,
  getBeBaseUrl,
  indexData,
  setBeBaseUrl,
  updateConfig,
  updateModelConfig
} from '../services/backend';
import './Common.css';
import './Setting.css';

interface SettingState {
  beBaseUrl: string;
  dataDirs: string[];
  dataDir: string;
  modelProviders: string[];
  modelProvider: string;
  embedModels: string[];
  embedModel: string;
  chatModels: string[];
  chatModel: string;
  toolSets: string[];
  toolSet: string;
  mcpServers: string[];
  mcpServer: string;
}

class Setting extends Component<{}, SettingState> {
  constructor(props: {}) {
    super(props);
    this.state = {
      beBaseUrl: getBeBaseUrl(),
      dataDirs: [],
      dataDir: '',
      modelProviders: [],
      modelProvider: '',
      embedModels: [],
      embedModel: '',
      chatModels: [],
      chatModel: '',
      toolSets: [],
      toolSet: '',
      mcpServers: [],
      mcpServer: '',
    };
  }

  componentDidMount() {
    this.initSetting();
  }

  initSetting() {
    this.initModelProviders();
    this.initEmbedModels()
    this.initChatModels();
    this.initToolSets();
    this.initDataDirs();
    this.initMcpServers();
    this.initConfig();
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

  initToolSets() {
    fetchToolSets().then(toolSets => {
      this.setState({ toolSets: toolSets });
    });
  }

  initDataDirs() {
    fetchDataConfig().then(dataConfig => {
      const dataDirs = Object.keys(dataConfig).map((data) => {
        return data;
      });
      this.setState({ dataDirs: dataDirs });
    });
  }

  initMcpServers() {
    fetchMcpServers().then(mcpServers => {
      this.setState({ mcpServers: mcpServers });
    });
  }

  initConfig() {
    fetchConfig().then(config => {
      this.setState({
        modelProvider: config.model_provider,
        dataDir: config.data_dir,
        toolSet: config.tool_set,
        mcpServer: config.mcp_server,
      });
      this.reloadApiConfig(config.model_provider);
    });
  }

  reloadApiConfig(modelProvider: string) {
    fetchModelConfig(modelProvider).then((config) => {
      this.setState({
        embedModel: config.embed_model,
        chatModel: config.chat_model,
      });
    })
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
    const { modelProvider, dataDir, toolSet, mcpServer } = this.state;
    const config = {
      'model_provider': modelProvider,
      'tool_set': toolSet,
      'data_dir': dataDir,
      'mcp_server': mcpServer,
    };
    updateConfig(JSON.stringify(config)).then(() => {
      alert('Setting Saved!');
      this.reloadApiConfig(modelProvider);
      this.initEmbedModels();
      this.initChatModels();
    })
  };

  handleIndexData = async (e: MouseEvent) => {
    const { dataDir } = this.state;
    indexData(dataDir).then(() => {
      alert('Data Indexed!')
    });
  }

  handleSaveModelConfig = async (e: MouseEvent) => {
    const { modelProvider, embedModel, chatModel } = this.state;
    const config = {
      'embed_model': embedModel,
      'chat_model': chatModel,
    };
    updateModelConfig(modelProvider, JSON.stringify(config)).then(() => {
      alert('Model Config Saved!')
    })
  };

  render() {
    const { beBaseUrl, dataDirs, dataDir, mcpServers, mcpServer, modelProviders, modelProvider, embedModel, chatModel, embedModels, chatModels, toolSets, toolSet } = this.state;

    return (
      <div className='main-frame'>
        <div className='header'>
          <Link to='/query'>Return Home</Link>
        </div>
        <h1 className='title'>Settings</h1>
        <label className='title'>General</label>
        <div className='setting-container'>
          <div className='setting'>
            <label>Backend Base URL:</label>
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
            <label>Tool Set:</label>
            <select value={toolSet} onChange={(e: ChangeEvent<HTMLSelectElement>) => {
              this.setState({ toolSet: e.target.value })
            }}>{toolSets.map(toolSet => (
              <option key={toolSet} value={toolSet}>{toolSet}</option>
            ))}
            </select>
          </div>
          <div className='setting'>
            <label>Data Dir:</label>
            <select value={dataDir} onChange={(e: ChangeEvent<HTMLSelectElement>) => {
              this.setState({ dataDir: e.target.value })
            }}>{dataDirs.map(dataDir => (
              <option key={dataDir} value={dataDir}>{dataDir}</option>
            ))}
            </select>
            <button onClick={this.handleIndexData}>Index</button>
          </div>
          <div className='setting'>
            <label>MCP server:</label>
            <select value={mcpServer} onChange={(e: ChangeEvent<HTMLSelectElement>) => {
              this.setState({ mcpServer: e.target.value })
            }}>{mcpServers.map(mcpServer => (
              <option key={mcpServer} value={mcpServer}>{mcpServer}</option>
            ))}
            </select>
          </div>
          <div className='setting'>
            <label>Model Provider:</label>
            <select value={modelProvider} onChange={(e: ChangeEvent<HTMLSelectElement>) => {
              this.setState({ modelProvider: e.target.value })
            }}>{modelProviders.map(modelProvider => (
              <option key={modelProvider} value={modelProvider}>{modelProvider}</option>
            ))}
            </select>
          </div>
          <div className='setting'>
            <button onClick={this.handleSaveConfig}>Save</button>
          </div>
        </div>
        <label className='title'>Model Config</label>
        <div className='setting-container'>
          <div className='setting'>
            <label>Embed Model: </label>
            <select value={embedModel} onChange={(e: ChangeEvent<HTMLSelectElement>) => {
              this.setState({ embedModel: e.target.value })
            }}>{embedModels.map(model => (
              <option key={model} value={model}>{model}</option>
            ))}
            </select>
          </div>
          <div className='setting'>
            <label>Chat Model: </label>
            <select value={chatModel} onChange={(e: ChangeEvent<HTMLSelectElement>) => {
              this.setState({ chatModel: e.target.value })
            }}>{chatModels.map(model => (
              <option key={model} value={model}>{model}</option>
            ))}
            </select>
          </div>
          <div className='setting'>
            <button onClick={this.handleSaveModelConfig}>Save</button>
            <button onClick={this.handleReloadModels}>Reload Models</button>
          </div>
        </div>
      </div>
    );
  }
}

export default Setting;