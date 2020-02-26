# Azure Cognitive Search Python SDK-ish and Samples
Use the python script in this repo to do calls to [Azure Search](https://azure.microsoft.com/en-us/services/search/), you can create datasources, indexes, skillsets, indexers, synonyms and add custom skills.

## Important note
This code is supplied as in and there are no garantues it will still work with newer version of the Azure Search SDK, it is also not feature complete but rather a attempt to speed up development for the common things encountered when working with Azure Search. Contributions are welcome if you added other components to this. The code that interacts with Azure Search is all in the azure_search folder, the manage_service.py and query_index.py can be used from code, they use #%% to interact with Python Interactive in [VSCode](https://code.visualstudio.com/).

## Getting started
To get started create a project folder and copy over any of the sample file you want. It uses a config script in each of the project directories, copy the sample_config.json to the project folder, rename it to search_config.json and fill in the values that are appropriate. If you have additional keys with secrets in your json definitions, follow the body['']... lines to add those in the right places. Next, use the `manage_service.py` script to create the right components in the service. Finally after indexing was successful you can use the `query_index.py` to run queries against your new index.

### Caselaw case
If you want to run the caselaw case, go to https://case.law/bulk/download/ and download one of the files, and put the unzipped *.jsonl file in a blob storage and put those blob credentials in your config and the container name in the datasource definition. Be carefull of the fill size, it might be too large for your Search SKU.

### Bootcamp case
This case is based on the dataset in [this repo](https://github.com/Azure/LearnAI-KnowledgeMiningBootcamp) and follows roughly the structure from that, the only thing that was added was Image Analysis Skill (Microsoft.Skills.Vision.ImageAnalysisSkill) with mapping the output of that completely to the index (successfully!).
