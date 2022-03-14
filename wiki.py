import os
import json
import requests
import re

def arrayToString(array):
    s = ""
    for item in array:
        s += str(item)
    return s

def queryAdjustRegex(query):
    arr = [c for c in query]
    for c in range(len(arr)):
        # A-Z [65-90], a-z [97-122], 0-9 [48-57]
        if(not (ord(arr[c]) >= 65 and ord(arr[c]) <= 90 or 
            ord(arr[c]) >= 97 and ord(arr[c]) <= 122 or
            ord(arr[c]) >= 48 and ord(arr[c]) <= 57 or 
            ord(arr[c]) == 32)):
            arr[c] = ".*"
        else:
            arr[c] = "" + arr[c]
    query = arrayToString(arr)
    return query

def matchRegex(query, search, regex):
    wiki_link = None
    SEARCH_URL = "https://en.wikipedia.org/?curid="

    for item in search:
        # print(item["title"] + ",line 31")
        res = re.search(regex, item["title"])

        if (res):
            wiki_link = SEARCH_URL + str(item["pageid"])
            break

    return wiki_link

def getWikiURL(query):
    WIKI_URL = "https://en.wikipedia.org/w/api.php"
    srlimit = 20 # number of entries per page
    sroffset = 0
    wiki_link = None
    max_page = 10

    query = queryAdjustRegex(query)

    while(not wiki_link):
        query_params = {
            "action": "query",
            "list": "search",
            "srlimit": srlimit,
            "sroffset": sroffset,
            "srsearch": query,
            "format": "json",
        }
        response = requests.get(
            WIKI_URL,
            params=query_params
        )
        # print(response.json())
        search = response.json()["query"]["search"]

        # print(query + ",line 48")

        # search for regex ".*title.*\(.*film.*\)"
        regex = ".*" + query + ".*\(.*" + "film" + ".*\)"
        wiki_link = matchRegex(query, search, regex)

        if(not wiki_link):
            # print(query + ",line 71")
            # search for regex ^title$
            regex = "^" + query + "$"
            wiki_link = matchRegex(query, search, regex)
            
        sroffset += srlimit
        next_page = sroffset / srlimit

        if(next_page > max_page and not wiki_link):
            break

    return wiki_link