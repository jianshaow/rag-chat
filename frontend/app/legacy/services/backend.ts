function setBeBaseUrl(beBaseUrl: string) {
    localStorage.setItem('beBaseUrl', beBaseUrl);
}

function getBeBaseUrl() {
    var beBaseUrl = localStorage.getItem('beBaseUrl');
    if (beBaseUrl === null) {
        beBaseUrl = "http://localhost:5000/legacy";
        setBeBaseUrl(beBaseUrl);
    }
    return beBaseUrl;
}

async function fetchConfig() {
    const url = `${getBeBaseUrl()}/config`;
    return fetch(url).then(response => response.json());
}

async function updateConfig(config: string) {
    const url = `${getBeBaseUrl()}/config`;
    fetch(url, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: config,
    })
}

async function fetchData() {
    const url = `${getBeBaseUrl()}/data`;
    return fetch(url).then(response => response.json());
}

async function fetchDataConfig() {
    const url = `${getBeBaseUrl()}/data_config`;
    return fetch(url).then(response => response.json());
}

async function updateDataConfig(data_config: string) {
    const url = `${getBeBaseUrl()}/config`;
    fetch(url, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: data_config,
    })
}

async function fetchModelProviders() {
    const url = `${getBeBaseUrl()}/model_provider`
    return fetch(url).then(response => response.json());
}


async function fetchModelConfig(model_provider: string) {
    const url = `${getBeBaseUrl()}/model_provider/${model_provider}`;
    return fetch(url).then(response => response.json());
}

async function updateModelConfig(model_provider: string, config: string) {
    const url = `${getBeBaseUrl()}/model_provider/${model_provider}`;
    fetch(url, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: config,
    })
}

async function fetchEmbedModels(reload: boolean) {
    const url = `${getBeBaseUrl()}/embed_models?reload=${reload}`
    return fetch(url).then(response => response.json());
}

async function fetchChatModels(reload: boolean) {
    const url = `${getBeBaseUrl()}/chat_models?reload=${reload}`
    return fetch(url).then(response => response.json());
}

async function query(data: string, query: string) {
    const url = `${getBeBaseUrl()}/${data}/query`;
    return fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'plain/text' },
        body: query,
    }).then(response => response.json());
}

async function fetchChrunk(data: string, id: string) {
    const url = `${getBeBaseUrl()}/${data}/get/${id}`;
    return fetch(url).then(response => response.json());
}

export {
    getBeBaseUrl,
    setBeBaseUrl,
    fetchData,
    fetchConfig,
    updateConfig,
    fetchDataConfig,
    updateDataConfig,
    fetchModelProviders,
    fetchModelConfig,
    updateModelConfig,
    fetchEmbedModels,
    fetchChatModels,
    query,
    fetchChrunk,
}