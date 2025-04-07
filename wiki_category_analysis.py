#!/usr/bin/env python3
"""
Wikipedia Category Word Frequency Analyzer

This script takes a Wikipedia category name as a command-line argument,
retrieves all pages in that category using the MediaWiki API, and calculates
the cumulative frequency of non-common words across all pages.
"""

import argparse
import requests
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import string
import time
import os
import json
import hashlib

# Download NLTK resources if not already downloaded
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

# Cache directory
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

def get_cache_path(category_name):
    """
    Generate a cache file path for a category using MD5 hash.
    
    Args:
        category_name (str): Name of the Wikipedia category
        
    Returns:
        str: Path to the cache file
    """
    # Create MD5 hash of the category name
    hash_obj = hashlib.md5(category_name.encode())
    hash_str = hash_obj.hexdigest()
    
    return os.path.join(CACHE_DIR, f"{hash_str}.json")

def load_from_cache(category_name):
    """
    Load word frequency data from cache if available.
    
    Args:
        category_name (str): Name of the Wikipedia category
        
    Returns:
        tuple: (Counter object with word frequencies, bool indicating if cache was used)
    """
    cache_path = get_cache_path(category_name)
    
    if os.path.exists(cache_path):
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return Counter(data), True
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading cache: {e}")
    
    return Counter(), False

def save_to_cache(category_name, word_count):
    """
    Save word frequency data to cache.
    
    Args:
        category_name (str): Name of the Wikipedia category
        word_count (Counter): Counter object with word frequencies
    """
    cache_path = get_cache_path(category_name)
    
    try:
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(dict(word_count), f, ensure_ascii=False, indent=2)
        print(f"Results cached to {cache_path}")
    except IOError as e:
        print(f"Error saving to cache: {e}")

def get_pages_in_category(category_name):
    """
    Get all pages in a given Wikipedia category using the MediaWiki API.
    
    Args:
        category_name (str): Name of the Wikipedia category
        
    Returns:
        list: List of page titles in the category
    """
    api_url = "https://en.wikipedia.org/w/api.php"
    
    # Format the category name properly
    if not category_name.startswith("Category:"):
        category_name = "Category:" + category_name
    
    pages = []
    cmcontinue = None
    
    while True:
        params = {
            "action": "query",
            "format": "json",
            "list": "categorymembers",
            "cmtitle": category_name,
            "cmlimit": 500,  # Maximum allowed by API
            "cmtype": "page"  # Only get pages, not subcategories
        }
        
        if cmcontinue:
            params["cmcontinue"] = cmcontinue
        
        response = requests.get(api_url, params=params)
        data = response.json()
        
        if "query" in data and "categorymembers" in data["query"]:
            for member in data["query"]["categorymembers"]:
                pages.append(member["title"])
        
        if "continue" in data and "cmcontinue" in data["continue"]:
            cmcontinue = data["continue"]["cmcontinue"]
            # Sleep to avoid hitting API rate limits
            time.sleep(1)
        else:
            break
    
    print(f"Found {len(pages)} pages in category '{category_name}'")
    return pages

def get_page_content(page_title):
    """
    Get the text content of a Wikipedia page using the MediaWiki API.
    
    Args:
        page_title (str): Title of the Wikipedia page
        
    Returns:
        str: Text content of the page
    """
    api_url = "https://en.wikipedia.org/w/api.php"
    
    params = {
        "action": "query",
        "format": "json",
        "titles": page_title,
        "prop": "extracts",
        "explaintext": True,  # Get plain text content
        "exsectionformat": "plain"
    }
    
    response = requests.get(api_url, params=params)
    data = response.json()
    
    # Extract content from response
    if "query" in data and "pages" in data["query"]:
        pages = data["query"]["pages"]
        for page_id in pages:
            if "extract" in pages[page_id]:
                return pages[page_id]["extract"]
    
    return ""

def analyze_text(text):
    """
    Analyze text to count frequencies of non-common words.
    
    Args:
        text (str): Text to analyze
        
    Returns:
        Counter: Counter object with word frequencies
    """
    # Convert to lowercase and tokenize
    text = text.lower()
    tokens = word_tokenize(text)
    
    # Remove punctuation and numbers
    tokens = [word for word in tokens if word not in string.punctuation and not word.isdigit()]
    
    # Remove stopwords (common words)
    stop_words = set(stopwords.words('english'))
    
    # Add additional common words specific to Wikipedia
    wiki_common_words = [
        'cite', 'reference', 'http', 'https', 'www', 'com', 'org', 
        'retrieved', 'isbn', 'doi', 'page', 'pages', 'website', 'link'
    ]
    stop_words.update(wiki_common_words)
    
    # Filter out short words and stopwords
    meaningful_words = [word for word in tokens if len(word) > 2 and word not in stop_words]
    
    # Count frequencies
    return Counter(meaningful_words)

def analyze_category(category):
    """
    Analyze a Wikipedia category and return word frequencies.
    
    Args:
        category (str): Name of the Wikipedia category
        
    Returns:
        Counter: Counter object with word frequencies
    """
    # Try to load from cache first
    word_count, cache_used = load_from_cache(category)
    
    if cache_used:
        print(f"Loaded results from cache for category '{category}'")
        return word_count
    
    # If not in cache, process the category
    print(f"Processing category '{category}'...")
    
    # Get all pages in the category
    pages = get_pages_in_category(category)
    
    # Process each page
    for i, page_title in enumerate(pages):
        print(f"Processing page {i+1}/{len(pages)}: {page_title}")
        
        # Get page content
        content = get_page_content(page_title)
        
        # Analyze text and update word count
        page_word_count = analyze_text(content)
        word_count.update(page_word_count)
        
        # Sleep to avoid hitting API rate limits
        time.sleep(0.5)
    
    # Save results to cache
    save_to_cache(category, word_count)
    
    return word_count

def main():
    """Main function to run the analysis."""
    parser = argparse.ArgumentParser(description='Analyze word frequencies in Wikipedia categories')
    parser.add_argument('category', help='Wikipedia category name')
    
    args = parser.parse_args()
    category = args.category
    
    # Analyze the category
    total_word_count = analyze_category(category)
    
    # Print results
    print("\nTop 50 most frequent non-common words:")
    for word, count in total_word_count.most_common(50):
        print(f"{word}: {count}")

if __name__ == "__main__":
    main()