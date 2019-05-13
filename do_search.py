#%%
import json
from azure_search import AzureSearch  

def file_reader(filename) -> dict:
    with open(filename, 'r') as file:
        return json.load(file)


#%%
config = file_reader('caselaw/config.json')
search_client = AzureSearch(config, debug = True)
api_version = "2019-05-06-Preview"

#%%
datasource = file_reader(config['datasource_file'])
search_client.create_datasource(datasource, api_version)
#%%
index = file_reader(config['index_file'])
search_client.create_index(index, api_version)
#%%
skillset = file_reader(config['skillset_file'])
search_client.create_skillset(skillset, api_version)
#%%
indexer = file_reader(config['indexer_file'])
search_client.create_indexer(indexer, api_version)
#%%
search_client.reset_run(api_version, reset=True, run=True, wait=False)
#%%
search_client.query("entity: mother", api_version)
