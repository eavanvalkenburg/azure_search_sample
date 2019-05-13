import requests
import time
# import msrest

class AzureSearchConfig:
    def __init__(self,
            search_service_name,
            search_api_key,
            search_api_version,
            cognitive_services_key,
            storage_connection_string,
            datasource,
            index,
            skillset,
            indexer):
        self.search_service_name = search_service_name
        self.search_api_key = search_api_key
        self.search_api_version = search_api_version
        self.cognitive_services_key = cognitive_services_key
        self.storage_connection_string = storage_connection_string
        self.datasource = datasource
        self.index = index
        self.skillset = skillset
        self.indexer = indexer

    def get_base_url(self, domain='search.windows.net/'):
        return f"https://{self.search_service_name}.{domain}"

class AzureSearch:
    def __init__(self, config: AzureSearchConfig, debug=False):
        self.config = config
        self.debug = debug
        self.base_url = self.config.get_base_url()
        self.base_payload = {"api-version": self.config.search_api_version}
        self.base_headers = {"api-key": self.config.search_api_key, "Content-Type": "application/json"}

    #create datasource
    def create_datasource(self, body, **kwargs):
        body['credentials']['connectionString'] = self.config.storage_connection_string
        body['name'] = self.config.datasource

        if self.debug:
            print(body)
        url = self.base_url + f"datasources/{self.config.datasource}"
        req = requests.put(url, headers=self.base_headers, json=body, params=self.base_payload, **kwargs)
        if self.debug:
            print(req.text)
        req.raise_for_status()

    #create index
    def create_index(self, body, **kwargs):
        body['name'] = self.config.index

        # try delete
        url = self.base_url + f"indexes/{self.config.index}"
        delete = requests.delete(url, headers=self.base_headers, params=self.base_payload, **kwargs)

        req = requests.put(url, headers=self.base_headers, json=body, params=self.base_payload, **kwargs)
        req.raise_for_status()
        if self.debug:
            print(req.text)

    #create skillset
    def create_skillset(self, body, **kwargs):
        body['name'] = self.config.skillset
        if 'cognitiveServices' in body:
            body['cognitiveServices']['key'] = self.config.cognitive_services_key        
        if 'knowledgeStore' in body: 
            body['knowledgeStore']['storageConnectionString'] = self.config.storage_connection_string

        if self.debug:
            print(body)
        url = self.base_url + f"skillsets/{self.config.skillset}"
        req = requests.put(url, headers=self.base_headers, json=body, params=self.base_payload,  **kwargs)
        if self.debug:
            print(req.text)
        req.raise_for_status()

    #create indexer
    def create_indexer(self, body, **kwargs):
        body['name'] = self.config.indexer
        body['dataSourceName'] = self.config.datasource
        body['skillsetName'] = self.config.skillset
        body['targetIndexName'] = self.config.index

        url = self.base_url + f"indexers/{self.config.indexer}"
        req = requests.put(url, headers=self.base_headers, json=body, params=self.base_payload, **kwargs)
        if self.debug:
            print(req.text)
        req.raise_for_status()

    #reset and run indexer
    def reset_run(self, reset=True, run=True, wait=False, **kwargs):
        if reset:
            reset_url = self.base_url + f"indexers/{self.config.indexer}/reset"
            reset = requests.post(reset_url, headers=self.base_headers, params=self.base_payload, **kwargs)
            reset.raise_for_status()
        if run:
            run_url = self.base_url + f"indexers/{self.config.indexer}/run"
            run = requests.post(run_url, headers=self.base_headers, params=self.base_payload, **kwargs)
            run.raise_for_status()
        status_url = self.base_url + f"indexers/{self.config.indexer}/status"
        status = requests.get(status_url, headers=self.base_headers, params=self.base_payload, **kwargs)
        status.raise_for_status()
        out = status.json()
        state = out.get('lastResult').get('status')
        print(state)
        if self.debug:
            print(out)
        if wait:
            while state == 'inProgress' or state == "reset":
                time.sleep(10)
                status = requests.get(status_url, headers=self.base_headers, params=self.base_payload, **kwargs)
                status.raise_for_status()
                out = status.json()
                state = out.get('lastResult').get('status')
                print(state)

    #query
    def query(self, query, **kwargs):
        payload = self.base_payload.copy()
        payload["search"] = query
        query_url = self.base_url + f"indexes/{self.config.index}/docs"
        query = requests.get(query_url, headers=self.base_headers, params=payload, **kwargs)
        query.raise_for_status()
        return query.json()

