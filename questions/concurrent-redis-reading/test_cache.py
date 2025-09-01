#!/usr/bin/env python3
"""
Test script to demonstrate Redis caching for PostgreSQL queries
"""
import requests
import time
import json

BASE_URL = "http://localhost:5000"

def test_query_caching():
    """Test that identical queries are served from cache"""
    print("Testing query caching...")
    
    # First query (should hit database)
    start_time = time.time()
    response1 = requests.post(f"{BASE_URL}/query", json={
        "query": "SELECT * FROM users WHERE name LIKE %s",
        "params": ["%Alice%"],
        "cache_ttl": 30
    })
    time1 = time.time() - start_time
    
    # Second identical query (should hit cache)
    start_time = time.time()
    response2 = requests.post(f"{BASE_URL}/query", json={
        "query": "SELECT * FROM users WHERE name LIKE %s",
        "params": ["%Alice%"],
        "cache_ttl": 30
    })
    time2 = time.time() - start_time
    
    data1 = response1.json()
    data2 = response2.json()
    
    print(f"First query time: {time1:.3f}s (from_cache: {data1['from_cache']})")
    print(f"Second query time: {time2:.3f}s (from_cache: {data2['from_cache']})")
    print(f"Performance improvement: {time1/time2:.1f}x faster")
    
    assert not data1['from_cache'], "First query should not be from cache"
    assert data2['from_cache'], "Second query should be from cache"
    assert data1['result'] == data2['result'], "Results should be identical"
    print("✓ Query caching test passed!")

def test_cache_invalidation():
    """Test that cache is invalidated on data changes"""
    print("\nTesting cache invalidation...")
    
    # First, cache a query
    requests.post(f"{BASE_URL}/query", json={
        "query": "SELECT COUNT(*) FROM users",
        "cache_ttl": 60
    })
    
    # Get initial count
    response1 = requests.post(f"{BASE_URL}/query", json={
        "query": "SELECT COUNT(*) FROM users"
    })
    initial_count = response1.json()['result']['rows'][0][0]
    
    # Add new user (should invalidate cache)
    requests.post(f"{BASE_URL}/users", json={
        "name": "Test User",
        "email": "test@example.com"
    })
    
    # Query again (should hit database due to invalidation)
    response2 = requests.post(f"{BASE_URL}/query", json={
        "query": "SELECT COUNT(*) FROM users"
    })
    
    new_count = response2.json()['result']['rows'][0][0]
    from_cache = response2.json()['from_cache']
    
    print(f"Initial count: {initial_count}")
    print(f"New count: {new_count}")
    print(f"From cache: {from_cache}")
    
    assert new_count == initial_count + 1, "Count should increase by 1"
    assert not from_cache, "Query should not be from cache after invalidation"
    print("✓ Cache invalidation test passed!")

def test_different_queries():
    """Test that different queries have different cache keys"""
    print("\nTesting different query caching...")
    
    # Query 1
    response1 = requests.post(f"{BASE_URL}/query", json={
        "query": "SELECT * FROM users WHERE id = %s",
        "params": [1]
    })
    
    # Query 2 (different parameter)
    response2 = requests.post(f"{BASE_URL}/query", json={
        "query": "SELECT * FROM users WHERE id = %s",
        "params": [2]
    })
    
    # Both should not be from cache initially
    assert not response1.json()['from_cache'], "First query should not be cached"
    assert not response2.json()['from_cache'], "Second query should not be cached"
    
    # Repeat first query - should be cached
    response1_cached = requests.post(f"{BASE_URL}/query", json={
        "query": "SELECT * FROM users WHERE id = %s",
        "params": [1]
    })
    
    assert response1_cached.json()['from_cache'], "Repeated query should be cached"
    print("✓ Different query caching test passed!")

if __name__ == "__main__":
    print("Running Redis-PostgreSQL caching tests...")
    print("Make sure the Flask app is running on localhost:5000")
    print("=" * 50)
    
    try:
        test_query_caching()
        test_cache_invalidation()
        test_different_queries()
        print("\n" + "=" * 50)
        print("All tests passed! 🎉")
        print("The Redis caching layer is working correctly with PostgreSQL.")
        
    except Exception as e:
        print(f"\nTest failed: {e}")
        print("Make sure both Redis and PostgreSQL are running and the database is initialized.")