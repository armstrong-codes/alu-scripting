#!/usr/bin/python3
"""
Contains the function top_ten which queries the Reddit API
and prints the titles of the first 10 hot posts of a subreddit.
"""

import requests


def top_ten(subreddit):
    """
    Prints the titles of the first 10 hot posts for a given subreddit.

    Args:
        subreddit (str): The name of the subreddit

    Returns:
        None: Prints titles directly, or "None" if subreddit is invalid
    """
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {
        'User-Agent': 'custom-user-agent'
    }
    params = {
        'limit': 10
    }

    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False)
        if response.status_code != 200:
            print("None")
            return

        data = response.json()
        posts = data.get("data", {}).get("children", [])

        if not posts:
            return  # Do not print None; subreddit is valid but has no hot posts

        for post in posts:
            title = post.get("data", {}).get("title")
            if title:
                print(title)

    except Exception:
        print("None")
