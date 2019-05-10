#%%
import requests
import json
import time
# import msrest

class search:
    def __init__(self, project_name, config_file_name='config', debug=False):
        self.project_name = project_name
        self.debug = debug
        config = self._file_reader(f'{self.project_name}/{config_file_name}.json')
        # self.client = msrest.ServiceClient(msrest.Configuration(base_url=f"https://{config['search_service_name']}.search.windows.net/"))
        # with open(f'{self.project_name}/{config_file_name}.json', 'r') as file:
        #     config = json.load(file)        
        self.base_url = f"https://{config['search_service_name']}.search.windows.net/"
        self.api_key = config["search_api_key"]
        # self.client.add_header('api-key', config["search_api_key"])
        self.cogn_svc_key = config["cogn_svc_key"]
        self.storage_conn_string = config["storage_conn_string"]

    #create datasource
    def create_datasource(self, api_version, name='datasource'):
        fullname = f'{self.project_name}-{name}'
        body = self._file_reader(f'{self.project_name}/{name}.json')
        # with open(f'{self.project_name}/{name}.json', 'r') as file:
        #     body = json.load(file)
        body['credentials']['connectionString'] = self.storage_conn_string
        body['name'] = fullname
        if self.debug:
            print(body)
        payload = {"api-version": api_version}
        headers = {"api-key": self.api_key, "Content-Type": "application/json"}
        url = self.base_url + f"datasources/{fullname}"
        # msrest.
        req = requests.put(url, headers=headers, json=body, params=payload)
        if self.debug:
            print(req.text)
        req.raise_for_status()

    #create index
    def create_index(self, api_version, name='index'):
        fullname = f'{self.project_name}-{name}'
        with open(f'{self.project_name}/{name}.json', 'r') as file:
            body = json.load(file)
        body['name'] = fullname
        payload = {"api-version": api_version}
        headers = {"api-key": self.api_key, "Content-Type": "application/json"}
        # try delete
        url = self.base_url + f"indexes/{fullname}"
        delete = requests.delete(url, headers=headers, params=payload)

        req = requests.put(url, headers=headers, json=body, params=payload)
        req.raise_for_status()
        if self.debug:
            print(req.text)

    #create skillset
    def create_skillset(self, api_version, name='skillset'):
        fullname = f'{self.project_name}-{name}'
        with open(f'{self.project_name}/{name}.json', 'r') as file:
            body = json.load(file)    
        body['name'] = fullname
        if 'cognitiveServices' in body:
            body['cognitiveServices']['key'] = self.cogn_svc_key        
        if 'knowledgeStore' in body: 
            body['knowledgeStore']['storageConnectionString'] = self.storage_conn_string
        if self.debug:
            print(body)
        payload = {"api-version": api_version}
        headers = {"api-key": self.api_key, "Content-Type": "application/json"}
        url = self.base_url + f"skillsets/{fullname}"
        req = requests.put(url, headers=headers, json=body, params=payload)
        if self.debug:
            print(req.text)
        req.raise_for_status()

    #create indexer
    def create_indexer(self, api_version, name='indexer', datasource_name='datasource', skillset_name='skillset', index_name='index'):
        fullname = f'{self.project_name}-{name}'
        with open(f'{self.project_name}/{name}.json', 'r') as file:
            body = json.load(file)
        body['name'] = fullname
        body['dataSourceName'] = f'{self.project_name}-{datasource_name}'
        body['skillsetName'] = f'{self.project_name}-{skillset_name}'
        body['targetIndexName'] = f'{self.project_name}-{index_name}'
        payload = {"api-version": api_version}
        headers = {"api-key": self.api_key, "Content-Type": "application/json"}
        url = self.base_url + f"indexers/{self.project_name}-{name}"
        req = requests.put(url, headers=headers, json=body, params=payload, timeout=600)
        if self.debug:
            print(req.text)
        req.raise_for_status()

    #reset and run indexer
    def reset_run(self, api_version, name='indexer', reset=True, run=True, wait=False):
        fullname = f'{self.project_name}-{name}'
        payload = {"api-version": api_version}
        headers = {"api-key": self.api_key}
        if reset:
            reset_url = self.base_url + f"indexers/{self.project_name}-{name}/reset"
            reset = requests.post(reset_url, headers=headers, params=payload)
            reset.raise_for_status()
        if run:
            run_url = self.base_url + f"indexers/{self.project_name}-{name}/run"
            run = requests.post(run_url, headers=headers, params=payload)
            run.raise_for_status()
        status_url = self.base_url + f"indexers/{self.project_name}-{name}/status"
        status = requests.get(status_url, headers=headers, params=payload)
        status.raise_for_status()
        out = status.json()
        state = out.get('lastResult').get('status')
        print(state)
        if self.debug:
            print(out)
        while state == 'inProgress' or state == "reset":
            time.sleep(5)
            status = requests.get(status_url, headers=headers, params=payload)
            status.raise_for_status()
            out = status.json()
            state = out.get('lastResult').get('status')
            print(state)

    #query
    def query(self, query, api_version, name='index'):
        fullname = f'{self.project_name}-{name}'
        payload = {"api-version": api_version, "search": query}
        headers = {"api-key": self.api_key}
        query_url = self.base_url + f"indexes/{self.project_name}-{name}/docs"
        query = requests.get(query_url, headers=headers, params=payload)
        query.raise_for_status()
        return query.json()

    def _file_reader(self, filename) -> dict:
        with open(filename, 'r') as file:
            return json.load(file)
        

#%%
project_folder = 'caselaw'
search_client = search(project_folder, debug = True)
api_version = "2019-05-06-Preview"
api_version_old = "2017-11-11-Preview"
api_version_not_preview = '2019-05-06'

#%%
search_client.create_datasource(api_version)
#%%
search_client.create_index(api_version)
#%%
search_client.create_skillset(api_version)
#%%
search_client.create_indexer(api_version)
#%%
search_client.reset_run(api_version, reset=True, run=True, wait=True)
#%%
search_client.query("murder", api_version)
