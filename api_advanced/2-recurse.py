#!/usr/bin/python3
"""
Contains the recursive function recurse that retrieves all hot post titles
from a given subreddit using the Reddit API.
"""

import requests


def recurse(subreddit, hot_list=None, after=None):
    """
    Recursively queries the Reddit API and returns a list of titles of all
    hot articles for a given subreddit.

    Args:
        subreddit (str): The name of the subreddit
        hot_list (list): Accumulates titles recursively (default None)
        after (str): Token for pagination (default None)

    Returns:
        list or None: List of post titles or None if subreddit is invalid
    """
    if hot_list is None:
        hot_list = []

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {'User-Agent': 'custom-user-agent'}
    params = {'after': after, 'limit': 100}

    try:
        response = requests.get(
            url, headers=headers, params=params, allow_redirects=False)

        if response.status_code != 200:
            return None

        data = response.json().get("data", {})
        posts = data.get("children", [])

        for post in posts:
            hot_list.append(post.get("data", {}).get("title"))

        after = data.get("after")
        if after is not None:
            return recurse(subreddit, hot_list, after)
        return hot_list

    except requests.RequestException:
        return None
