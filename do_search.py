#%%
import json
from azure_search import AzureSearchClient, AzureSearchConfig

def file_reader(filename) -> dict:
    with open(filename, 'r') as file:
        return json.load(file)

files = file_reader('bootcamp/files.json')
search_client = AzureSearchClient(
        AzureSearchConfig(
                **file_reader('bootcamp/search_config.json')), debug=False)

#%%
datasource = file_reader(files['datasource_file'])
search_client.create_datasource(datasource)

#%%
index = file_reader(files['index_file'])
search_client.create_index(index)

#%%
skillset = file_reader(files['skillset_file'])
search_client.create_skillset(skillset, debug=True)

#%%
indexer = file_reader(files['indexer_file'])
search_client.create_indexer(indexer)

#%%
search_client.reset_run(reset=True, run=True, wait=True)

#%%
search_client.query("satya")

#%%
search_client.query("microsoft&&searchFields=organizations")

#%%
search_client.query("search=satya&$select=blob_uri,faces,categories")
