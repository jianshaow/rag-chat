function setBeBaseUrl(beBaseUrl: string) {
    localStorage.setItem('beBaseUrl', beBaseUrl);
}

function getBeBaseUrl() {
    var beBaseUrl = localStorage.getItem('beBaseUrl');
    if (beBaseUrl === null) {
        beBaseUrl = "http://localhost:8000";
        setBeBaseUrl(beBaseUrl);
    }
    return beBaseUrl;
}

async function fetchConfig() {
    const url = `${getBeBaseUrl()}/api/setting`;
    return fetch(url).then(response => response.json());
}

async function updateConfig(config: string) {
    const url = `${getBeBaseUrl()}/api/setting`;
    fetch(url, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: config,
    })
}

async function fetchData() {
    const url = `${getBeBaseUrl()}/api/data`;
    return fetch(url).then(response => response.json());
}

async function fetchDataConfig() {
    const url = `${getBeBaseUrl()}/api/data/config`;
    return fetch(url).then(response => response.json());
}

async function updateDataConfig(data_config: string) {
    const url = `${getBeBaseUrl()}/api/data/config`;
    fetch(url, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: data_config,
    })
}

async function fetchModelProviders() {
    const url = `${getBeBaseUrl()}/api/model/provider`
    return fetch(url).then(response => response.json());
}


async function fetchModelConfig(model_provider: string) {
    const url = `${getBeBaseUrl()}/api/model/provider/${model_provider}`;
    return fetch(url).then(response => response.json());
}

async function updateModelConfig(model_provider: string, config: string) {
    const url = `${getBeBaseUrl()}/api/model/provider/${model_provider}`;
    fetch(url, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: config,
    })
}

async function fetchEmbedModels(reload: boolean) {
    const url = `${getBeBaseUrl()}/api/model/embed?reload=${reload}`
    return fetch(url).then(response => response.json());
}

async function fetchChatModels(reload: boolean) {
    const url = `${getBeBaseUrl()}/api/model/chat?reload=${reload}`
    return fetch(url).then(response => response.json());
}

async function query(query: string) {
    const url = `${getBeBaseUrl()}/api/query`;
    return fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'plain/text' },
        body: query,
    }).then(response => response.json());
}

async function fetchChrunk(data: string, id: string) {
    const url = `${getBeBaseUrl()}/api/data/${data}/node/${id}`;
    return fetch(url).then(response => response.json());
}

export {
    fetchChatModels, fetchChrunk, fetchConfig, fetchData, fetchDataConfig, fetchEmbedModels, fetchModelConfig, fetchModelProviders, getBeBaseUrl, query, setBeBaseUrl, updateConfig, updateDataConfig, updateModelConfig
};
