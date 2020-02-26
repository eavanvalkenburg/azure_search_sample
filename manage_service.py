
#%%
import json
import requests
from pprint import pprint
from azure_search import AzureSearchConfig, AzureSearchQuery, AzureSearchClient


def file_reader(filename) -> dict:
    with open(filename, "r") as file:
        return json.load(file)


files = file_reader("<case>/files.json")
search_client = AzureSearchClient(
    AzureSearchConfig(**file_reader("<case>/search_config.json")), debug=False
)

#%%
datasource = file_reader(files["datasource_file"])
search_client.create_datasource(datasource)

#%%
synmap = file_reader(files["synonym_file"])
search_client.create_synonyms(synmap)

#%%
index = file_reader(files["index_file"])
search_client.create_index(index)

#%%
skillset = file_reader(files["skillset_file"])
search_client.create_skillset(skillset)#, debug=True)

#%%
indexer = file_reader(files["indexer_file"])
search_client.create_indexer(indexer)

#%%
search_client.reset_run(reset=True, run=True, wait=True)



# %%
