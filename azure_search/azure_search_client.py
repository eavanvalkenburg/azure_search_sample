"""Classes for communicating with Azure Search."""
import requests
import time
import json

from .azure_search_config import AzureSearchConfig
# from .azure_search_query import AzureSearchQuery


class AzureSearchClient:
    """Creates an instance of AzureSearchClient."""

    def __init__(self, config: AzureSearchConfig, debug=False):
        """Create an instance of AzureSearchClient."""
        self.config = config
        self.debug = debug
        self.base_payload = {"api-version": self.config.search_api_version}
        self.base_headers = {
            "api-key": self.config.search_api_key,
            "Content-Type": "application/json",
        }

    def create_datasource(self, body, debug=False, **kwargs):
        """Create a datasource in the search service."""
        body["credentials"]["connectionString"] = self.config.storage_connection_string
        body["name"] = self.config.datasource

        if self.debug or debug:
            print(body)
        url = self.config.base_url + f"datasources/{self.config.datasource}"
        req = requests.put(
            url,
            headers=self.base_headers,
            json=body,
            params=self.base_payload,
            **kwargs,
        )
        if self.debug or debug:
            print(req.text)
        req.raise_for_status()

    def create_index(self, body, debug=False, **kwargs):
        """Create a index in the search service."""
        body["name"] = self.config.index
        # try delete
        url = self.config.base_url + f"indexes/{self.config.index}"
        delete = requests.delete(
            url, headers=self.base_headers, params=self.base_payload, **kwargs
        )
        if self.debug or debug:
            print(delete.status_code)
        req = requests.put(
            url,
            headers=self.base_headers,
            json=body,
            params=self.base_payload,
            **kwargs,
        )
        if self.debug or debug or req.status_code == 400:
            print(req.text)
        req.raise_for_status()

    def create_skillset(self, body, debug=False, **kwargs):
        """Create a skillset in the search service."""
        body["name"] = self.config.skillset
        if "cognitiveServices" in body:
            body["cognitiveServices"]["key"] = self.config.cognitive_services_key
        if "knowledgeStore" in body:
            body["knowledgeStore"][
                "storageConnectionString"
            ] = self.config.storage_connection_string

        def replace_uri(skill, urls):
            if "uri" in skill:                
                skill["uri"] = urls[skill['name']]
            return skill

        body["skills"] = [
            replace_uri(s, self.config.custom_skill_url) for s in body["skills"]
        ]
        if self.debug or debug:
            print(f"Skills: {body['skills']}")

        if self.debug or debug:
            print(f"body to be deployed: {body}")
        url = self.config.base_url + f"skillsets/{self.config.skillset}"
        req = requests.put(
            url,
            headers=self.base_headers,
            json=body,
            params=self.base_payload,
            **kwargs,
        )
        if self.debug or debug or req.status_code == 400:
            print(req.text)
        req.raise_for_status()

    def create_indexer(self, body, debug=False, **kwargs):
        """Create a indexer in the search service."""
        body["name"] = self.config.indexer
        body["dataSourceName"] = self.config.datasource
        body["skillsetName"] = self.config.skillset
        body["targetIndexName"] = self.config.index

        url = self.config.base_url + f"indexers/{self.config.indexer}"
        req = requests.put(
            url,
            headers=self.base_headers,
            json=body,
            params=self.base_payload,
            **kwargs,
        )
        if self.debug or debug or req.status_code == 400:
            print(req.text)
        req.raise_for_status()

    def create_synonyms(self, body, debug=False, **kwargs):
        """Create a synonym map in your search service"""
        body["name"] = self.config.synonyms
        body["synonyms"] = "\n".join(body["synonyms"])+"\n"
        url = f"{self.config.base_url}synonymmaps"
        delete = requests.delete(
            url+f"/{self.config.synonyms}", headers=self.base_headers, params=self.base_payload, **kwargs
        )
        if self.debug or debug:
            print(delete.status_code)
        req = requests.post(
            url,
            headers=self.base_headers,
            json=body,
            params=self.base_payload,
            **kwargs,
        )
        if self.debug or debug or req.status_code == 400:
            print(req.text)
        req.raise_for_status()

    def reset_run(self, reset=True, run=True, wait=False, debug=False, **kwargs):
        """Reset and run the indexer."""
        if reset:
            reset_url = self.config.base_url + f"indexers/{self.config.indexer}/reset"
            reset = requests.post(
                reset_url, headers=self.base_headers, params=self.base_payload, **kwargs
            )
            reset.raise_for_status()
        if run:
            run_url = self.config.base_url + f"indexers/{self.config.indexer}/run"
            run = requests.post(
                run_url, headers=self.base_headers, params=self.base_payload, **kwargs
            )
            run.raise_for_status()
            if self.debug or debug or run.status_code == 400:
                print(run.text)
        status_url = self.config.base_url + f"indexers/{self.config.indexer}/status"
        status = requests.get(
            status_url, headers=self.base_headers, params=self.base_payload, **kwargs
        )
        status.raise_for_status()
        out = status.json()
        state = out.get("lastResult").get("status")
        print(state)
        if self.debug or debug:
            print(out)
        if wait:
            while state == "inProgress" or state == "reset":
                time.sleep(10)
                status = requests.get(
                    status_url,
                    headers=self.base_headers,
                    params=self.base_payload,
                    **kwargs,
                )
                if self.debug or debug or status.status_code == 400:
                    print(status.text)
                status.raise_for_status()
                out = status.json()
                state = out.get("lastResult").get("status")
                print(state)

    def advanced_query(self, query: dict, **kwargs):
        """Query the search service."""
        params = self.base_payload.copy()
        query_url = f"{self.config.base_url}indexes/{self.config.index}/docs/search"
        resp = requests.post(
            query_url, headers=self.base_headers, params=params, json=query, **kwargs
        )
        if resp.status_code == 400:
            print(resp.text)
        resp.raise_for_status()
        return resp.json()

    def query(self, query, **kwargs):
        """Query the search service."""
        params = self.base_payload.copy()
        query_url = f"{self.config.base_url}indexes/{self.config.index}/docs/search"
        resp = requests.post(
            query_url,
            headers=self.base_headers,
            params=params,
            json=query.__dict__(),
            **kwargs,
        )
        if resp.status_code == 400:
            print(resp.text)
        resp.raise_for_status()
        return resp.json()

    def simple_query(self, query: str, **kwargs):
        """Query the search service."""
        payload = self.base_payload.copy()
        payload["queryType"] = "simple"
        payload["search"] = query
        query_url = f"{self.config.base_url}indexes/{self.config.index}/docs"
        query = requests.get(
            query_url, headers=self.base_headers, params=payload, **kwargs
        )
        if query.status_code == 400:
            print(query.text)
        query.raise_for_status()
        return query.json()

    def suggester_query(self, query: str, **kwargs):
        """Query the suggester."""
        #GET https://[service name].search.windows.net/indexes/[index name]/docs/autocomplete?[query parameters]  
        payload = self.base_payload.copy()
        payload["search"] = query
        payload["suggesterName"] = "sg"
        query_url = f"{self.config.base_url}indexes/{self.config.index}/docs/suggest"
        # print(query_url)
        query = requests.get(
            query_url, headers=self.base_headers, params=payload, **kwargs
        )
        if query.status_code == 400:
            print(query.text)
        query.raise_for_status()
        return query.json()

    def autocomplete_query(self, query: str, **kwargs):
        """Query the suggester."""
        #GET https://[service name].search.windows.net/indexes/[index name]/docs/autocomplete?[query parameters]  
        payload = self.base_payload.copy()
        payload["search"] = query
        payload["autocompleteMode"] = "twoTerms"
        payload["suggesterName"] = "sg"
        query_url = f"{self.config.base_url}indexes/{self.config.index}/docs/autocomplete"
        # print(query_url)
        query = requests.get(
            query_url, headers=self.base_headers, params=payload, **kwargs
        )
        if query.status_code == 400:
            print(query.text)
        query.raise_for_status()
        return query.json()


