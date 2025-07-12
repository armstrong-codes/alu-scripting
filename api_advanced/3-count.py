#!/usr/bin/python3
"""
Recursive function that queries the Reddit API, parses hot article titles,
and prints the count of given keywords sorted by frequency and alphabetically.
"""

import requests
import re


def count_words(subreddit, word_list, hot_list=None, after=None, count_dict=None):
    if hot_list is None:
        hot_list = []
    if count_dict is None:
        count_dict = {}
    if word_list:
        word_list = [word.lower() for word in word_list]

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-Agent': 'custom-user-agent'}
    params = {'after': after, 'limit': 100}

    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False)
        if response.status_code != 200:
            return

        data = response.json().get("data", {})
        children = data.get("children", [])

        # Extract and accumulate titles
        for post in children:
            title = post.get("data", {}).get("title", "").lower()
            hot_list.append(title)

        # If there's another page, recurse again
        after = data.get("after")
        if after:
            return count_words(subreddit, word_list, hot_list, after, count_dict)

        # Count words recursively after fetching all titles
        for word in word_list:
            if word not in count_dict:
                count_dict[word] = 0
            for title in hot_list:
                # Match full word occurrences using regex
                count_dict[word] += len(re.findall(rf'\b{re.escape(word)}\b', title))

        # Filter out zero-count words
        filtered = {k: v for k, v in count_dict.items() if v > 0}

        # Sort by count desc, then alphabetically
        for word, count in sorted(filtered.items(), key=lambda x: (-x[1], x[0])):
            print(f"{word}: {count}")

    except requests.RequestException:
        return
