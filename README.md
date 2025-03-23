1 - Introduction

This is a python script designed to extract all names from an autocomplete API running at http://35.200.185.69:8000. 

2 - How it Works:

* Uses BFS to systematically explore prefixes(a-z)

* Handle rate limits (HTTP 429) with backoff time for retries, backoff time is exponential with a total of 3 tries

* Adjust queries based on API versions (v1, v2, v3)

* Efficiently fetches all possible names while minimizing requests

3 - Implementation Details:

* Starting Point: The script begins with single-letter queries (a-z)

* Prefix Expansion: If a query returns the maximum allowed results, new prefixes are generated (a → aa, ab, ac...)

* Rate Limit Handling: If the API returns 429 Too Many Requests, the script waits before retrying

* Multi-Version Handling: The script adapts to API versions (v1, v2, v3) by modifying request limits

4 - Results

* Version 1 (v1)

Total Unique Names Discovered: 18,628 |
Total API Requests Made: 31,018 |
Total Execution Time: 20,028.89 seconds

* Version 2 (v2)

Total Unique Names Discovered: 7,364 |
Total API Requests Made: 3,146 |
Total Execution Time: 4,189.82 seconds

* Version 3 (v3)

Total Unique Names Discovered: 5,310 |
Total API Requests Made: 1,222 |
Total Execution Time: 988.64 seconds

5 - Challenges

* Rate Limits: Frequent 429 errors slow down extraction, Solution: Exponential Backoff

* Limited Query Depth: Some longer names might be missing, Solution: Increase MaxDepth



