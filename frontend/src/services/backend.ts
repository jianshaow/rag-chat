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

async function fetchData() {
    const url = `${getBeBaseUrl()}/data`;
    return fetch(url).then(response => response.json());
}

async function query(data: string, text: string) {
    const url = `${getBeBaseUrl()}/query?data=${data}&text=${text}`;
    return fetch(url).then(response => response.text());
}

export { getBeBaseUrl, setBeBaseUrl, fetchData, query }