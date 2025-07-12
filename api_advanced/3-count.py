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
        _initialize_word_count(word_list, word_count, 0)
    
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
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
                _print_results(word_count)
            return
        
        _process_posts(posts, word_count, 0)
        
        after_token = data['data'].get('after')
        
        if after_token:
            return count_words(subreddit, word_list, word_count, after_token)
        else:
            _print_results(word_count)
            
    except (requests.RequestException, ValueError, KeyError):
        return


def _initialize_word_count(word_list, word_count, index):
    """
    Recursively initialize word count dictionary.
    
    Args:
        word_list (list): List of keywords
        word_count (dict): Dictionary to initialize
        index (int): Current index in word_list
    """
    if index >= len(word_list):
        return
    
    word = word_list[index]
    word_lower = word.lower()
    if word_lower in word_count:
        word_count[word_lower] += 0
    else:
        word_count[word_lower] = 0
    
    _initialize_word_count(word_list, word_count, index + 1)


def _process_posts(posts, word_count, index):
    """
    Recursively process posts.
    
    Args:
        posts (list): List of posts to process
        word_count (dict): Dictionary to update with counts
        index (int): Current index in posts
    """
    if index >= len(posts):
        return
    
    post = posts[index]
    if 'data' in post and 'title' in post['data']:
        title = post['data']['title']
        _count_words_in_title(title, word_count, list(word_count.keys()), 0)
    
    _process_posts(posts, word_count, index + 1)


def _count_words_in_title(title, word_count, keywords, index):
    """
    Recursively count occurrences of keywords in a single title.
    
    Args:
        title (str): The title to analyze
        word_count (dict): Dictionary to update with counts
        keywords (list): List of keywords to check
        index (int): Current index in keywords
    """
    if index >= len(keywords):
        return
    
    word = keywords[index]
    title_lower = title.lower()
    pattern = r'\b' + re.escape(word) + r'\b'
    matches = re.findall(pattern, title_lower)
    word_count[word] += len(matches)
    
    _count_words_in_title(title, word_count, keywords, index + 1)


def _print_results(word_count):
    """
    Print results in the required format.
    
    Args:
        word_count (dict): Dictionary with word counts
    """
    filtered_items = []
    _filter_nonzero_counts(word_count, filtered_items)
    
    if not filtered_items:
        return
    
    sorted_items = []
    _sort_results(filtered_items, sorted_items, 0)
    
    _print_sorted_results(sorted_items, 0)


def _filter_nonzero_counts(word_count, filtered_items):
    """
    Recursively filter out words with zero count.
    
    Args:
        word_count (dict): Dictionary with word counts
        filtered_items (list): List to store filtered items
    """
    items = list(word_count.items())
    _filter_helper(items, filtered_items, 0)


def _filter_helper(items, filtered_items, index):
    """
    Helper function to recursively filter items.
    
    Args:
        items (list): List of (word, count) tuples
        filtered_items (list): List to store filtered items
        index (int): Current index
    """
    if index >= len(items):
        return
    
    word, count = items[index]
    if count > 0:
        filtered_items.append((word, count))
    
    _filter_helper(items, filtered_items, index + 1)


def _sort_results(filtered_items, sorted_items, index):
    """
    Recursively sort results by count (desc) then alphabetically (asc).
    
    Args:
        filtered_items (list): List of (word, count) tuples to sort
        sorted_items (list): List to store sorted items
        index (int): Current index
    """
    if index >= len(filtered_items):
        return
    
    item = filtered_items[index]
    _insert_sorted(sorted_items, item, 0)
    _sort_results(filtered_items, sorted_items, index + 1)


def _insert_sorted(sorted_items, item, index):
    """
    Recursively insert item in sorted position.
    
    Args:
        sorted_items (list): Already sorted list
        item (tuple): Item to insert
        index (int): Current index to check
    """
    if index >= len(sorted_items):
        sorted_items.append(item)
        return
    
    word, count = item
    existing_word, existing_count = sorted_items[index]
    
    if (count > existing_count or 
        (count == existing_count and word < existing_word)):
        sorted_items.insert(index, item)
        return
    
    _insert_sorted(sorted_items, item, index + 1)


def _print_sorted_results(sorted_items, index):
    """
    Recursively print sorted results.
    
    Args:
        sorted_items (list): List of sorted (word, count) tuples
        index (int): Current index
    """
    if index >= len(sorted_items):
        return
    
    word, count = sorted_items[index]
    print("{}: {}".format(word, count))
    
    _print_sorted_results(sorted_items, index + 1)
