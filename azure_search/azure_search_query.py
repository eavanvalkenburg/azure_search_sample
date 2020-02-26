"""Classes for querying Azure Search."""

from .azure_search_client import AzureSearchClient

class AzureSearchQuery:
    """Contains the config of a AzureSearchquery class."""

    def __init__(
        self,
        client: AzureSearchClient,
        search: str,
        queryType: str="simple",
        count: bool = False,
        facets: list = [],
        filter: str = "",
        highlight: str = "",
        highlightPreTag: str = "",
        highlightPostTag: str = "",
        minimumCoverage: int = 100,
        orderby: str = "",
        scoringParameters: list = [],
        scoringProfiles: str = "",
        searchFields: str = "",
        searchMode: str = "any",
        select: str = "",
        skip: int = 0,
        top: int = 0,
    ):
        self.client = client
        self.queryType = queryType
        self.count = count
        self.facets = facets
        self.filter = filter
        self.highlight = highlight
        self.highlightPreTag = highlightPreTag
        self.highlightPostTag = highlightPostTag
        self.minimumCoverage = minimumCoverage
        self.orderby = orderby
        self.scoringParameters = scoringParameters
        self.scoringProfiles = scoringProfiles
        self.search = search
        self.searchFields = searchFields
        self.searchMode = searchMode
        self.select = select
        self.skip = skip
        self.top = top

    def __dict__(self):
        ret = {
            "queryType": self.queryType,
            "count": "true" if self.count else "false",
            "facets": self.facets if len(self.facets) > 0 else '',
            "filter": self.filter,
            "highlight": self.highlight,
            "highlightPreTag": self.highlightPreTag,
            "highlightPostTag": self.highlightPostTag,
            "minimumCoverage": self.minimumCoverage,
            "orderby": self.orderby,
            "scoringParameters": self.scoringParameters if len(self.scoringParameters) > 0 else '',
            "scoringProfiles": self.scoringProfiles,
            "search": self.search,
            "searchFields": self.searchFields,
            "searchMode": self.searchMode,
            "select": self.select,
            "skip": self.skip if self.skip > 0 else '',
            "top": self.top if self.top > 0 else '',
        }
        return {k:v for k,v in ret.items() if v != ''}