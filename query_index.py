
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
# Details of documents that contain a search term. For example, the file name, URL, size, and last modified date of all documents that include "New York" (there should be 18).
pprint(search_client.query(AzureSearchQuery(search_client, 
        search="New York",
        searchMode= "all",
        queryType= "full",
        count= True,
        select= "id, file_name, url, size, last_modified",
        )))


#%%
# Document details based on multiple search terms - for example, details of all documents that include "London" and "Buckingham Palace" (there should be 2).
pprint(search_client.query(AzureSearchQuery(search_client, 
        search="london, buckingham palace",
        searchMode= "all",
        queryType= "simple",
        count= True,
        select= "id, file_name, url",
        )))

# %%
# Filtering based on specific fields - for example, all documents that contain the term "Las Vegas" that have "reviews" in their URL (there should be 13), and all documents containing the term "Las Vegas" that that do not have "reviews" in their URL (there should be 2).
pprint(search_client.query(AzureSearchQuery(search_client, 
        search="las vegas + url:reviews",
        searchMode= "all",
        queryType= "full",
        count= True,
        select= "id, file_name, url",
        )))

# %%
pprint(search_client.query(AzureSearchQuery(search_client, 
        search="las vegas + -url:reviews",
        searchMode= "all",
        queryType= "full",
        count= True,
        select= "id, file_name, url",
        )))

# %%
# Which hotels have positive (or negative) reviews?
pprint(search_client.query(AzureSearchQuery(search_client, 
        search="hotel + url:reviews",
        searchMode= "all",
        queryType= "full",
        count= True,
        select= "file_name, content, locations, persons, sentiment_score",
        orderby="sentiment_score desc"        
        )))


# %%
# What are the main talking points in the documents returned by a search?
pprint(search_client.query(AzureSearchQuery(search_client, 
        search="*",
        searchMode= "all",
        facets=["keyPhrases"],
        queryType= "full",
        count= True,
        select= "file_name",
        )))


# %%
# Which reviews were written by a specific reviewer?
pprint(search_client.query(AzureSearchQuery(search_client, 
        search="url:reviews",
        searchMode= "all",
        facets=["persons"],
        queryType= "full",
        count= True,
        select= "file_name, url, persons",
        )))

# %%
# Which documents mention a specific location?
pprint(search_client.query(AzureSearchQuery(search_client, 
        search="*",
        # searchFields="locations",
        facets=["locations"],
        searchMode= "all",
        queryType= "full",
        count= True,
        filter= "locations/any()",
        select= "locations",
        # orderby="score asc"
        )))

# %%
# Which documents contain URLs?
pprint(search_client.query(AzureSearchQuery(search_client, 
        search="*",
        # searchFields="locations",
        facets=["urls"],
        searchMode= "all",
        queryType= "full",
        count= True,
        filter= "urls/any()",
        select= "urls",
        # orderby="score asc"
        )))

# %%
# Find the key talking points and sentiment score for each review of a hotel in New Yor
res = search_client.query(AzureSearchQuery(search_client, 
        search="locations:New York AND hotel",
        # searchFields="locations",
        facets=['keyPhrases'],
        searchMode= "all",
        queryType= "full",
        count= True,
        select= "sentiment_score, keyPhrases",
        orderby="sentiment_score desc"
        ))
print(f"Found {res.get('@odata.count',None)} results")
print(f"Results contain these fields: {res.keys()}")
print(f"Facets: {res.get('@search.facets')}")
print(f"Context: {res.get('@odata.context')}")

for r in res['value']:
        pprint(r)


# %%
# Find reviews of hotels in New York that mention the location Broadway.
res = search_client.query(AzureSearchQuery(search_client, 
        search="locations:New York AND locations:Broadway AND url:reviews AND hotel",
        # searchFields="locations",
        facets=['locations'],
        searchMode= "all",
        queryType= "full",
        count= True,
        select= "content, locations",
        ))
print(f"Found {res.get('@odata.count',None)} results")
print(f"Results contain these fields: {res.keys()}")
print(f"Facets: {res.get('@search.facets')}")
print(f"Context: {res.get('@odata.context')}")

for r in res['value']:
        pprint(r)

# %%
# Find the key phrases and sentiment scores of reviews written by Matthew Daughtry.
res = search_client.query(AzureSearchQuery(search_client, 
        search="url:reviews AND persons:'Matthew Daughtry",
        facets=['keyPhrases'],
        searchMode= "all",
        queryType= "full",
        count= True,
        select= "sentiment_score, keyPhrases",
        ))
print(f"Found {res.get('@odata.count',None)} results")
print(f"Results contain these fields: {res.keys()}")
print(f"Facets: {res.get('@search.facets')}")
print(f"Context: {res.get('@odata.context')}")

for r in res['value']:
        pprint(r)

# %%
# Filter reviews of hotels in Las Vegas to show only the negative ones 
# (defined as having a sentiment score of 0.5 or lower).
res = search_client.query(AzureSearchQuery(search_client, 
        search="url:reviews AND locations:'Las Vegas' AND hotel",
        searchMode= "all",
        queryType= "full",
        count= True,
        filter="sentiment_score le 0.5",
        select= "file_name, content, sentiment_score",
        ))
print(f"Found {res.get('@odata.count',None)} results")
print(f"Results contain these fields: {res.keys()}")
print(f"Context: {res.get('@odata.context')}")

for r in res['value']:
        pprint(r)

# %%
# Filter search results to include only collateral documents that contain URLs. 
res = search_client.query(AzureSearchQuery(search_client, 
        search="*",
        searchMode= "all",
        queryType= "full",
        count= True,
        filter="urls/any()",
        select= "content",
        ))
print(f"Found {res.get('@odata.count',None)} results")
print(f"Results contain these fields: {res.keys()}")
print(f"Context: {res.get('@odata.context')}")

for r in res['value']:
        pprint(r)

# %%
# The AI-generated image captions and any OCR text extracted from images in 
# collateral documents that match submitted search terms and contain images. 
# For example, a search for "Grand Canyon" should result in a list of documents 
# that include both this term and one or more images; 
# and for each document in the results, the AI-generated caption 
# and OCR extracted text from each image should be displayed.

res = search_client.query(AzureSearchQuery(search_client, 
        search="grand canyon",
        searchMode= "all",
        queryType= "full",
        count= True,
        select= "description/captions/text, myOcrText",
        ))
print(f"Found {res.get('@odata.count',None)} results")
print(f"Results contain these fields: {res.keys()}")
print(f"Context: {res.get('@odata.context')}")

for r in res['value']:
        pprint(r)

# %%
# Documents in which images contain AI-generated captions 
# or tags that match the submitted search terms. 
# For example, a search for "bridge" should return a list of documents 
# that contain an image in which the AI-generated caption 
# or tags contains the word "bridge".
res = search_client.query(AzureSearchQuery(search_client, 
        search="bridge",
        searchFields="description/captions/text, description/tags", 
        searchMode= "all",
        queryType= "full",
        count= True,
        select= "file_name, description/captions/text, description/tags",
        ))
print(f"Found {res.get('@odata.count',None)} results")
print(f"Results contain these fields: {res.keys()}")
print(f"Context: {res.get('@odata.context')}")

for r in res['value']:
        pprint(r)


# %%
# Update your client application so that users can filter search results 
# by specifying a keyword that must be included in the top ten most frequent words.
res = search_client.query(AzureSearchQuery(search_client, 
        search="*",
        # searchFields="description/captions/text, description/tags", 
        searchMode= "all",
        facets=["words"],
        queryType= "full",
        count= True,
        filter="words/any(t: t eq 'great')",
        select= "file_name, words",
        ))
print(f"Found {res.get('@odata.count',None)} results")
print(f"Results contain these fields: {res.keys()}")
print(f"Facets: {res.get('@search.facets')}")
print(f"Context: {res.get('@odata.context')}")

for r in res['value']:
        pprint(r)

# %%
# Return search results based on synonyms - 
# for example, a search for "Britain" should return documents 
# that include "United Kingdom" or "UK".
res1 = search_client.query(AzureSearchQuery(search_client, 
        search="UK",
        searchFields="locations", 
        searchMode= "any",
        queryType= "full",
        count= True,
        select= "file_name, keyPhrases, locations, words",
        ))
res2 = search_client.query(AzureSearchQuery(search_client, 
        search='(UK "United Kingdom" Britain "Great Britain")',
        searchFields="locations", 
        searchMode= "any",
        queryType= "full",
        count= True,
        select= "file_name, keyPhrases, locations, words",
        ))
print(f"Found {res1.get('@odata.count',None)} results with one term")
print(f"Found {res2.get('@odata.count',None)} results with all synonyms")
# print(f"Results contain these fields: {res.keys()}")
# print(f"Context: {res.get('@odata.context')}")

# for r in res['value']:
#         pprint(r)


# %%
# Apply a scoring profile to increase the search score of results based on term 
# inclusion in key phrases, document size, and last modified date. 
# For example, searching for "quiet" should boost results where 
# the word "quiet" is included in the key phrases field.
res = search_client.query(AzureSearchQuery(search_client, 
        search="quiet",
        searchMode= "all",
        queryType= "full",
        facets=["keyPhrases"],
        count= True,
        select= "keyPhrases",
        ))
print(f"Found {res.get('@odata.count',None)} results")
print(f"Facets: {res.get('@search.facets')}")

for r in res['value']:
        pprint(r)


# %%
# Modify your client application so that it displays suggestions and autocomplete options 
# for partial user input based on the Location field. For example, typing "San" should produce 
# suggestions for "San Francisco" and "San Diego".
text = "San D"
res1 = search_client.suggester_query(text)
pprint(res1)
res2 = search_client.autocomplete_query(text)
pprint(res2)


# %%
