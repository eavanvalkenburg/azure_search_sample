import requests
import time
# import msrest

class AzureSearch:
    def __init__(self, config, debug=False):
        self.config = config
        self.debug = debug
        self.base_url = f"https://{self.config['search_service_name']}.search.windows.net/"
        self.api_key = self.config["search_api_key"]
        self.cogn_svc_key = self.config["cogn_svc_key"]
        self.storage_conn_string = self.config["storage_conn_string"]

    #create datasource
    def create_datasource(self, body, api_version):
        body['credentials']['connectionString'] = self.storage_conn_string
        body['name'] = self.config['datasource_name']

        if self.debug:
            print(body)

        payload = {"api-version": api_version}
        headers = {"api-key": self.api_key, "Content-Type": "application/json"}
        url = self.base_url + f"datasources/{self.config['datasource_name']}"
        req = requests.put(url, headers=headers, json=body, params=payload)
        if self.debug:
            print(req.text)
        req.raise_for_status()

    #create index
    def create_index(self, body, api_version):
        body['name'] = self.config['index_name']

        payload = {"api-version": api_version}
        headers = {"api-key": self.api_key, "Content-Type": "application/json"}

        # try delete
        url = self.base_url + f"indexes/{self.config['index_name']}"
        delete = requests.delete(url, headers=headers, params=payload)

        req = requests.put(url, headers=headers, json=body, params=payload)
        req.raise_for_status()
        if self.debug:
            print(req.text)

    #create skillset
    def create_skillset(self, body, api_version):
        body['name'] = self.config['skillset_name']
        if 'cognitiveServices' in body:
            body['cognitiveServices']['key'] = self.cogn_svc_key        
        if 'knowledgeStore' in body: 
            body['knowledgeStore']['storageConnectionString'] = self.storage_conn_string

        if self.debug:
            print(body)
        payload = {"api-version": api_version}
        headers = {"api-key": self.api_key, "Content-Type": "application/json"}
        url = self.base_url + f"skillsets/{self.config['skillset_name']}"
        req = requests.put(url, headers=headers, json=body, params=payload)
        if self.debug:
            print(req.text)
        req.raise_for_status()

    #create indexer
    def create_indexer(self, 
        body,
        api_version,
        timeout=60):

        body['name'] = self.config['indexer_name']
        body['dataSourceName'] = self.config['datasource_name']
        body['skillsetName'] = self.config['skillset_name']
        body['targetIndexName'] = self.config['index_name']

        payload = {"api-version": api_version}
        headers = {"api-key": self.api_key, "Content-Type": "application/json"}
        url = self.base_url + f"indexers/{self.config['indexer_name']}"
        req = requests.put(url, headers=headers, json=body, params=payload, timeout=timeout)
        if self.debug:
            print(req.text)
        req.raise_for_status()

    #reset and run indexer
    def reset_run(self, api_version, reset=True, run=True, wait=False):
        payload = {"api-version": api_version}
        headers = {"api-key": self.api_key}
        if reset:
            reset_url = self.base_url + f"indexers/{self.config['indexer_name']}/reset"
            reset = requests.post(reset_url, headers=headers, params=payload)
            reset.raise_for_status()
        if run:
            run_url = self.base_url + f"indexers/{self.config['indexer_name']}/run"
            run = requests.post(run_url, headers=headers, params=payload)
            run.raise_for_status()
        status_url = self.base_url + f"indexers/{self.config['indexer_name']}/status"
        status = requests.get(status_url, headers=headers, params=payload)
        status.raise_for_status()
        out = status.json()
        state = out.get('lastResult').get('status')
        print(state)
        if self.debug:
            print(out)
        if wait:
            while state == 'inProgress' or state == "reset":
                time.sleep(5)
                status = requests.get(status_url, headers=headers, params=payload)
                status.raise_for_status()
                out = status.json()
                state = out.get('lastResult').get('status')
                print(state)

    #query
    def query(self, query, api_version):
        payload = {"api-version": api_version, "search": query}
        headers = {"api-key": self.api_key}
        query_url = self.base_url + f"indexes/{self.config['index_name']}/docs"
        query = requests.get(query_url, headers=headers, params=payload)
        query.raise_for_status()
        return query.json()

