"""Classes for storing Azure Search config"""

class AzureSearchConfig:
    """Contains the config of a AzureSearchClient class."""

    def __init__(
        self,
        search_service_name,
        search_api_key,
        search_api_version,
        cognitive_services_key,
        storage_connection_string,
        custom_skill_url,
        datasource,
        index,
        skillset,
        indexer,
        synonyms,
        **kwargs,
    ):
        """Create a AzureSearchClient config."""
        self.search_service_name = search_service_name
        self.search_api_key = search_api_key
        self.search_api_version = search_api_version
        self.cognitive_services_key = cognitive_services_key
        self.storage_connection_string = storage_connection_string
        self.custom_skill_url = custom_skill_url
        self.datasource = datasource
        self.index = index
        self.skillset = skillset
        self.indexer = indexer
        self.synonyms = synonyms
        if "domain" in kwargs:
            self._domain = kwargs["domain"]
        else:
            self._domain = "search.windows.net/"

    @property
    def base_url(self):
        """Return the base url of the api."""
        return f"https://{self.search_service_name}.{self._domain}"