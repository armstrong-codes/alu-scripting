#!/usr/bin/python3
"""
Recursive function to count keywords in Reddit hot posts
"""
import requests
import re


def count_words(subreddit, word_list, word_count=None, after=None):
    """
    Recursively queries Reddit API and counts keywords in hot post titles
    
    Args:
        subreddit (str): The subreddit to query
        word_list (list): List of keywords to count
        word_count (dict): Dictionary to accumulate word counts (for recursion)
        after (str): Reddit pagination token (for recursion)
    """
    # Initialize word_count dictionary on first call
    if word_count is None:
        word_count = {}
        # Convert word_list to lowercase and initialize counts
        for word in word_list:
            word_lower = word.lower()
            word_count[word_lower] = word_count.get(word_lower, 0)
    
    # Reddit API endpoint for hot posts
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    
    # Set up headers to avoid rate limiting
    headers = {
        'User-Agent': 'python:keyword.counter:v1.0 (by /u/pythonbot)'
    }
    
    # Set up parameters
    params = {
        'limit': 100  # Maximum posts per request
    }
    
    # Add pagination token if provided
    if after:
        params['after'] = after
    
    try:
        # Make request without following redirects
        response = requests.get(url, headers=headers, params=params, 
                              allow_redirects=False)
        
        # Check if we got a redirect (invalid subreddit)
        if response.status_code == 302:
            return
        
        # Check if request was successful
        if response.status_code != 200:
            return
        
        # Parse JSON response
        data = response.json()
        
        # Check if we have valid data structure
        if 'data' not in data or 'children' not in data['data']:
            return
        
        posts = data['data']['children']
        
        # If no posts, we're done
        if not posts:
            # Print results only on the final call (when we have no more posts)
            if after is None or len(posts) == 0:
                print_results(word_count)
            return
        
        # Process each post title
        for post in posts:
            if 'data' in post and 'title' in post['data']:
                title = post['data']['title']
                count_words_in_title(title, word_count)
        
        # Get pagination token for next page
        after_token = data['data'].get('after')
        
        # If there's more data, recursively call for next page
        if after_token:
            count_words(subreddit, word_list, word_count, after_token)
        else:
            # No more pages, print results
            print_results(word_count)
            
    except (requests.RequestException, ValueError, KeyError):
        # Handle any errors silently (print nothing for invalid subreddits)
        return


def count_words_in_title(title, word_count):
    """
    Count occurrences of keywords in a single title
    
    Args:
        title (str): The title to analyze
        word_count (dict): Dictionary to update with counts
    """
    # Convert title to lowercase for case-insensitive matching
    title_lower = title.lower()
    
    # Use regex to find whole words only
    # This ensures 'java' matches 'java' but not 'javascript'
    for word in word_count.keys():
        # Create regex pattern for whole word matching
        pattern = r'\b' + re.escape(word) + r'\b'
        matches = re.findall(pattern, title_lower)
        word_count[word] += len(matches)


def print_results(word_count):
    """
    Print results in the required format
    
    Args:
        word_count (dict): Dictionary with word counts
    """
    # Filter out words with zero count
    filtered_counts = {word: count for word, count in word_count.items() 
                      if count > 0}
    
    # Sort by count (descending) then by word (ascending)
    sorted_words = sorted(filtered_counts.items(), 
                         key=lambda x: (-x[1], x[0]))
    
    # Print results
    for word, count in sorted_words:
        print(f"{word}: {count}")
