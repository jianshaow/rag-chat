import { MessageAnnotation, MessageAnnotationType, SourceData, SourceNode } from "@llamaindex/chat-ui";

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

async function streamQuery(query: string, onTextProcess: (answer: string) => void, onSoucesProcess: (sources: SourceNode[]) => void,) {
    const url = `${getBeBaseUrl()}/api/query/stream`;
    const resp = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'plain/text' },
        body: query,
    });

    const reader = resp.body?.getReader();
    if (!reader) {
        return;
    }

    const decoder = new TextDecoder();
    let accumulatedText = "";

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');
        lines.forEach(line => {
            if (line.length === 0) return;
            const index = line.indexOf(':');
            if (index !== -1) {
                const streamTypePart = line.substring(0, index);
                const streamContextPart = line.substring(index + 1);
                const streamContext = JSON.parse(streamContextPart);
                if (streamTypePart === '0') {
                    accumulatedText += streamContext;
                    onTextProcess(accumulatedText)
                } else if (streamTypePart === '8') {
                    const annotations: MessageAnnotation[] = streamContext as MessageAnnotation[]
                    annotations.forEach(annotation => {
                        if (annotation.type === MessageAnnotationType.SOURCES) {
                            const sourceData = annotation.data as SourceData;
                            onSoucesProcess(sourceData.nodes)
                        }
                    });
                }
            }
        });
    }

}

async function fetchChrunk(data: string, id: string) {
    const url = `${getBeBaseUrl()}/api/data/${data}/node/${id}`;
    return fetch(url).then(response => response.json());
}

export {
    fetchChatModels, fetchChrunk, fetchConfig, fetchData, fetchDataConfig, fetchEmbedModels, fetchModelConfig, fetchModelProviders, getBeBaseUrl, query, setBeBaseUrl, streamQuery, updateConfig, updateDataConfig, updateModelConfig
};

