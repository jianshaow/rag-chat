"use client";

import { MessageAnnotation, MessageAnnotationType } from "@llamaindex/chat-ui";
import { SourceData, SourceNode } from "@llamaindex/chat-ui/widgets";

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

async function fetchMcpServers() {
    const url = `${getBeBaseUrl()}/api/tools/mcp_servers`;
    return fetch(url).then(response => response.json());
}

async function fetchChatConfig() {
    const url = `${getBeBaseUrl()}/api/chat/config`;
    return fetch(url).then(response => response.json());
}

async function indexData(data: string) {
    const url = `${getBeBaseUrl()}/api/data/${data}`;
    return fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'plain/text' },
        body: data,
    }).then(response => { return });
}

async function fetchModelProviders() {
    const url = `${getBeBaseUrl()}/api/model/provider`
    return fetch(url).then(response => response.json());
}

async function fetchToolSets() {
    const url = `${getBeBaseUrl()}/api/tools`
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

async function streamQuery(query: string, agentic: boolean, onTextProcess: (answer: string) => void, onSoucesProcess: (sources: SourceNode[]) => void,) {
    var path = '/api/query/stream';
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

export { fetchChatConfig, fetchChatModels, fetchChrunk, fetchConfig, fetchData, fetchDataConfig, fetchEmbedModels, fetchMcpServers, fetchModelConfig, fetchModelProviders, fetchToolSets, getBeBaseUrl, indexData, query, setBeBaseUrl, streamQuery, updateConfig, updateModelConfig };

