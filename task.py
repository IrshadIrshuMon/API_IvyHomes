import string
import requests
import time
from collections import deque

API_URL = "http://35.200.185.69:8000/v1/autocomplete" # we can change v1 to v2 or v3 as we needed

Delay = 0.5
MaxDepth = 10
MaxResultPerQuery = 10  # suitable for v1, change accroding to v2(=12) and v3(=15)

def fetchNames(query, retries=3, backoffFactor=5.0):
    time.sleep(Delay)
    try:
        response = requests.get(API_URL, params={"query": query}, timeout=10)
        if response.status_code == 429:
            if retries > 0:
                print(f"429 rate limit hit for query='{query}' - backing off {backoffFactor}s")
                time.sleep(backoffFactor)
                return fetchNames(query, retries - 1, backoffFactor * 2)
            else:
                print(f"Exceeded max retries for query='{query}'. Skipping.")
                return (0, [])
        response.raise_for_status()
        data = response.json()
        count = data.get("count", 0)
        results = data.get("results", [])
        return (count, results)
    except requests.exceptions.RequestException as e:
        print(f"Request error for query='{query}': {e}")
        return (0, [])

def extractAllNames():
    queue = deque(string.ascii_lowercase)
    visitedPrefixes = set()
    allNames = set()
    totalRequests = 0
    while queue:
        prefix = queue.popleft()
        if prefix in visitedPrefixes:
            continue
        visitedPrefixes.add(prefix)
        count, results = fetchNames(prefix)
        totalRequests += 1
        for name in results:
            allNames.add(name)
        if len(prefix) < MaxDepth and len(results) == MaxResultPerQuery:
            for ch in string.ascii_lowercase:
                newPrefix = prefix + ch
                if newPrefix not in visitedPrefixes:
                    queue.append(newPrefix)
        print(f"Queried '{prefix}': {len(results)} results (count={count}), total requests so far = {totalRequests}")
    return allNames, totalRequests

if __name__ == "__main__":
    startTime = time.time()
    names, requestCount = extractAllNames()
    print("==========================================")
    print(f"Total unique names discovered: {len(names)}")
    print(f"Total requests made: {requestCount}")
    endTime = time.time()  
    print(f"Total execution time: {endTime - startTime:.2f} seconds")

