#!/usr/bin/python3
"""
Module for querying Reddit API to get top 10 hot posts from a subreddit.

This module provides functionality to query the Reddit API and print
the titles of the first 10 hot posts from a specified subreddit.
"""
import requests


def top_ten(subreddit):
    """
    Query the Reddit API and print the titles of the first 10 hot posts.

    Args:
        subreddit (str): The subreddit to query for hot posts

    Returns:
        None: Prints titles directly or "None" if invalid subreddit
    """
    if not subreddit or not isinstance(subreddit, str):
        print("None")
        return

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {
        'User-Agent': 'python:top.ten:v1.0 (by /u/pythonbot)'
    }
    params = {
        'limit': 10
    }

    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False)

        # Check if we got a redirect (invalid subreddit)
        if response.status_code == 302 or response.status_code == 404:
            print("None")
            return

        # Check if request was successful
        if response.status_code != 200:
            print("None")
            return

        # Parse JSON response
        data = response.json()

        # Check for Reddit API errors
        if 'error' in data:
            print("None")
            return

        # Check if we have valid data structure
        if 'data' not in data or 'children' not in data['data']:
            print("None")
            return

        posts = data['data']['children']

        # If no posts found, it might be an invalid subreddit
        if not posts:
            print("None")
            return

        # Print titles of first 10 posts
        count = 0
        for post in posts:
            if count >= 10:
                break
            if 'data' in post and 'title' in post['data']:
                print(post['data']['title'])
                count += 1

    except (requests.RequestException, ValueError, KeyError):
        print("None")
