#!/usr/bin/env python
"""Test the web search detection functionality"""

from tools import should_use_web_search, web_search

print("✓ Tools imported successfully!\n")
print("Testing web search detection:\n")

test_queries = [
    'who is the cm of rajasthan',
    'hello how are you',
    'current news today',
    'latest pm of india',
    'what is python',
    'breaking news in delhi',
    'chief minister of maharashtra 2026',
    'how to cook rice'
]

for query in test_queries:
    should_search = should_use_web_search(query)
    status = "🌐 YES (needs web search)" if should_search else "💾 NO (local knowledge)"
    print(f"  '{query}'")
    print(f"    → {status}\n")

print("\n" + "="*60)
print("Testing actual web search (first 2 queries):")
print("="*60 + "\n")

test_search = [
    'who is cm rajasthan 2026',
    'current prime minister india'
]

for query in test_search:
    print(f"Searching for: '{query}'")
    try:
        result = web_search(query)
        print(f"Result:\n{result[:500]}...\n")  # Print first 500 chars
    except Exception as e:
        print(f"Error: {e}\n")
