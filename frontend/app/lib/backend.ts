import { DataPart, EventPartType, SourcesPartType } from "@llamaindex/chat-ui";
import { ChatEvent, SourceData, SourceNode } from "@llamaindex/chat-ui/widgets";

export function storeBeBaseUrl(beBaseUrl: string) {
    localStorage.setItem('beBaseUrl', beBaseUrl);
}

export function getBeBaseUrl() {
    let beBaseUrl = localStorage.getItem('beBaseUrl');
    if (beBaseUrl === null) {
        beBaseUrl = "http://localhost:8000";
        storeBeBaseUrl(beBaseUrl);
    }
    return beBaseUrl;
}

export async function fetchAppConfig() {
    const url = `${getBeBaseUrl()}/api/setting`;
    return fetch(url).then(response => response.json());
}

export async function updateAppConfig(config: string) {
    const url = `${getBeBaseUrl()}/api/setting`;
    fetch(url, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: config,
    })
}

export async function fetchData() {
    const url = `${getBeBaseUrl()}/api/data`;
    return fetch(url).then(response => response.json());
}

export async function fetchDataConfig() {
    const url = `${getBeBaseUrl()}/api/data/config`;
    return fetch(url).then(response => response.json());
}

export async function fetchMcpServers() {
    const url = `${getBeBaseUrl()}/api/tools/mcp_servers`;
    return fetch(url).then(response => response.json());
}

export async function fetchChatConfig() {
    const url = `${getBeBaseUrl()}/api/chat/config`;
    return fetch(url).then(response => response.json());
}

export async function indexData(data: string) {
    const url = `${getBeBaseUrl()}/api/data/${data}`;
    return fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'plain/text' },
        body: data,
    });
}

export async function fetchModelProviders() {
    const url = `${getBeBaseUrl()}/api/model/provider`
    return fetch(url).then(response => response.json());
}

export async function fetchToolSets() {
    const url = `${getBeBaseUrl()}/api/tools`
    return fetch(url).then(response => response.json());
}

export async function fetchModelConfig(model_provider: string) {
    const url = `${getBeBaseUrl()}/api/model/provider/${model_provider}`;
    return fetch(url).then(response => response.json());
}

export async function updateModelConfig(model_provider: string, config: string) {
    const url = `${getBeBaseUrl()}/api/model/provider/${model_provider}`;
    fetch(url, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: config,
    })
}

export async function fetchEmbedModels(reload: boolean) {
    const url = `${getBeBaseUrl()}/api/model/embed?reload=${reload}`
    return fetch(url).then(response => response.json());
}

export async function fetchChatModels(reload: boolean) {
    const url = `${getBeBaseUrl()}/api/model/chat?reload=${reload}`
    return fetch(url).then(response => response.json());
}

export async function query(query: string) {
    const url = `${getBeBaseUrl()}/api/query`;
    return fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'plain/text' },
        body: query,
    }).then(response => response.json());
}

export async function streamQuery(query: string, agentic: boolean, onTextProcess: (answer: string) => void, onEventsProcess: (title: string) => void, onSoucesProcess: (sources: SourceNode[]) => void,) {
    let path = '/api/query/stream';
    if (agentic) {
        path = '/api/query/agent_stream';
    }
    const url = `${getBeBaseUrl()}${path}`;
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
                    const dataParts: DataPart[] = streamContext as DataPart[]
                    dataParts.forEach(dataPart => {
                        if (dataPart.type === EventPartType) {
                            const eventData = dataPart.data as ChatEvent;
                            onEventsProcess(eventData.title)
                        }
                        if (dataPart.type === SourcesPartType) {
                            const sourceData = dataPart.data as SourceData;
                            onSoucesProcess(sourceData.nodes)
                        }
                    });
                }
            }
        });
    }
}

export async function fetchChrunk(data: string, id: string) {
    const url = `${getBeBaseUrl()}/api/data/${data}/node/${id}`;
    return fetch(url).then(response => response.json());
}
