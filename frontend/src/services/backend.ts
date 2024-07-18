function setBeBaseUrl(beBaseUrl: string) {
    localStorage.setItem('beBaseUrl', beBaseUrl);
}

function getBeBaseUrl() {
    var beBaseUrl = localStorage.getItem('beBaseUrl');
    if (beBaseUrl === null) {
        beBaseUrl = "http://localhost:5000";
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

async function fetchApiSpecs() {
    const url = `${getBeBaseUrl()}/api_spec`
    return fetch(url).then(response => response.json());
}


async function fetchApiConfig(api_spec: string) {
    const url = `${getBeBaseUrl()}/api_spec/${api_spec}`;
    return fetch(url).then(response => response.json());
}

async function updateApiConfig(api_spec: string, config: string) {
    const url = `${getBeBaseUrl()}/api_spec/${api_spec}`;
    fetch(url, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: config,
    })
}

async function fetchModels(reload: boolean) {
    const url = `${getBeBaseUrl()}/models?reload=${reload}`
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

export {
    getBeBaseUrl,
    setBeBaseUrl,
    fetchConfig,
    updateConfig,
    fetchDataConfig,
    updateDataConfig,
    fetchData,
    fetchApiSpecs,
    fetchApiConfig,
    updateApiConfig,
    fetchModels,
    query,
}