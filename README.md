# Database_comparison
quick comparison of paper databases aginst openalex

A sample of articles from IEEE can be used to check if OpenAlex provides the same result. Both CSV files should be ccreated using the same search string.

Topics.py allows for each unique topics from the OpenAlex results to be collected

API_fetch.py allows for a more filtered search than is avaliable in the GUI. The unique topics list is used as the default input but this can be changed directly. The Search string is also an input which can be written directly in the file.

Merge_results.py is used to combine the batches and remove duplicates fetched by API_fetch.py
