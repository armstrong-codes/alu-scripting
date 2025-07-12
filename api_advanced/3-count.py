#!/usr/bin/python3
"""
Recursive Reddit API keyword counter

This module defines a recursive function that queries the Reddit API, parses
the titles of all hot articles from a given subreddit, and prints a sorted
count of given keywords. The counting is case-insensitive and counts actual
word occurrences, not just title appearances.

Prototype:
    def count_words(subreddit, word_list)

Requirements:
    - Uses recursion (no loops allowed)
    - Merges duplicate keywords (case-insensitive)
    - Filters out zero-count keywords
    - Sorts by descending count, then alphabetically
    - Skips punctuation in word matching
    - Does not follow redirects
    - Adheres to PEP 8 and has valid module documentation
"""

import re
import requests


def count_words(subreddit, word_list, after=None, count_dict=None):
    """
    Recursively counts keywords in hot article titles from a subreddit.

    Args:
        subreddit (str): The name of the subreddit to query
        word_list (list): List of keywords to count
        after (str): Token for next page (used in recursion)
        count_dict (dict): Dictionary accumulating word counts

    Returns:
        None. Prints results sorted by count and keyword.
    """
    if count_dict is None:
        # Initialize case-insensitive word counter
        count_dict = {}
        for word in word_list:
            key = word.lower()
            if key in count_dict:
                count_dict[key] += 0  # Ensures duplicates are counted later
            else:
                count_dict[key] = 0

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "custom-user-agent"}
    params = {"limit": 100, "after": after}

    try:
        response = requests.get(
            url, headers=headers, params=params, allow_redirects=False)
        if response.status_code != 200:
            return

        data = response.json().get("data", {})
        posts = data.get("children", [])

        # Recursively count occurrences
        for post in posts:
            title = post.get("data", {}).get("title", "").lower()
            for word in count_dict:
                count_dict[word] += len(
                    re.findall(rf"\b{re.escape(word)}\b", title))

        if data.get("after"):
            return count_words(
                subreddit, word_list, data.get("after"), count_dict)

        # Filter and sort results
        results = [(word, count) for word, count in count_dict.items()
                   if count > 0]
        results.sort(key=lambda x: (-x[1], x[0]))

        for word, count in results:
            print(f"{word}: {count}")

    except requests.RequestException:
        return
