#%%
import json
from azure_search import AzureSearch, AzureSearchConfig

def file_reader(filename) -> dict:
    with open(filename, 'r') as file:
        return json.load(file)

config = file_reader('caselaw/search_config.json')
files = file_reader('caselaw/files.json')
search_client = AzureSearch(AzureSearchConfig(**config))

#%%
datasource = file_reader(files['datasource_file'])
search_client.create_datasource(datasource)
#%%
index = file_reader(files['index_file'])
search_client.create_index(index)
#%%
skillset = file_reader(files['skillset_file'])
search_client.create_skillset(skillset)
#%%
indexer = file_reader(files['indexer_file'])
search_client.create_indexer(indexer)
#%%
search_client.reset_run(reset=True, run=True, wait=True)
#%%
search_client.query("murder")

#%%
search_client.query("entity: CF & I Fabricators of Utah, Inc")
