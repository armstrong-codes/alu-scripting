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
        None
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {
        "User-Agent": "python:top.ten:v1.0.0 (by /u/alx_student)"
    }
    params = {
        "limit": 10
    }

    try:
        response = requests.get(
            url, headers=headers, params=params, allow_redirects=False)

        # Subreddit does not exist or forbidden
        if response.status_code != 200:
            print("None")
            return

        results = response.json().get("data", {}).get("children", [])
        if not results:
            return  # Valid subreddit but no posts, do nothing

        for post in results:
            title = post.get("data", {}).get("title")
            if title:
                print(title)

    except Exception:
        print("None")
