#!/usr/bin/python3
"""
Module for recursively counting keywords in Reddit hot posts.

This module provides functionality to query the Reddit API,
parse hot post titles, and count occurrences of specified keywords.
"""
import re
import requests


def count_words(subreddit, word_list, word_count=None, after=None):
    """
    Recursively queries Reddit API and counts keywords in hot post titles.
    
    Args:
        subreddit (str): The subreddit to query
        word_list (list): List of keywords to count
        word_count (dict): Dictionary to accumulate word counts (for recursion)
        after (str): Reddit pagination token (for recursion)
    """
    if word_count is None:
        word_count = {}
        for word in word_list:
            word_lower = word.lower()
            word_count[word_lower] = word_count.get(word_lower, 0)
    
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {
        'User-Agent': 'python:keyword.counter:v1.0 (by /u/pythonbot)'
    }
    params = {'limit': 100}
    
    if after:
        params['after'] = after
    
    try:
        response = requests.get(url, headers=headers, params=params,
                              allow_redirects=False)
        
        if response.status_code == 302:
            return
        
        if response.status_code != 200:
            return
        
        data = response.json()
        
        if 'data' not in data or 'children' not in data['data']:
            return
        
        posts = data['data']['children']
        
        if not posts:
            if after is None:
                print_results(word_count)
            return
        
        for post in posts:
            if 'data' in post and 'title' in post['data']:
                title = post['data']['title']
                count_words_in_title(title, word_count)
        
        after_token = data['data'].get('after')
        
        if after_token:
            return count_words(subreddit, word_list, word_count, after_token)
        else:
            print_results(word_count)
            
    except (requests.RequestException, ValueError, KeyError):
        return


def count_words_in_title(title, word_count):
    """
    Count occurrences of keywords in a single title.
    
    Args:
        title (str): The title to analyze
        word_count (dict): Dictionary to update with counts
    """
    title_lower = title.lower()
    
    for word in word_count.keys():
        pattern = r'\b' + re.escape(word) + r'\b'
        matches = re.findall(pattern, title_lower)
        word_count[word] += len(matches)


def print_results(word_count):
    """
    Print results in the required format.
    
    Args:
        word_count (dict): Dictionary with word counts
    """
    filtered_counts = {word: count for word, count in word_count.items()
                      if count > 0}
    
    sorted_words = sorted(filtered_counts.items(),
                         key=lambda x: (-x[1], x[0]))
    
    for word, count in sorted_words:
        print(f"{word}: {count}")
