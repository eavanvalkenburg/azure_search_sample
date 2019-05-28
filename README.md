# Azure Search Sample scripts
Use the python script in this repo to do calls to Azure Search, you can create datasources, indexes, skillsets and indexers.

### Config
It uses a config script in each of the subdirectories, copy the sample_config.json to a folder with your own definitions, rename it to search_config.json and fill in the values that are appropriate. If you have additional keys with secrets in your json definitions, follow the body['']... lines to add those in the right places.

### Caselaw case
If you want to run the caselaw case, go to https://case.law/bulk/download/ and download one of the files, and put the unzipped *.jsonl file in a blob storage and put those blob credentials in your config and the container name in the datasource definition. Be carefull of the fill size, it might be too large for your Search SKU.

### Bootcamp case
This case is based on the dataset in [this repo](https://github.com/Azure/LearnAI-KnowledgeMiningBootcamp) and follows roughly the structure from that, the only thing that was added was Image Analysis Skill (Microsoft.Skills.Vision.ImageAnalysisSkill) with mapping the output of that completely to the index (successfully!).