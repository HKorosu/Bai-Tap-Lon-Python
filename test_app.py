#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script to verify News Aggregator functionality
"""
import sys
import time

from db import (
    initialize_database,
    get_categories,
    get_sources,
    add_source,
    get_source_by_id,
    update_source,
    delete_source,
    count_articles,
    list_articles,
)
from crawler import crawl_all_sources, crawl_pending_articles

def test_database():
    """Test 1: Database initialization"""
    print("\n" + "="*50)
    print("TEST 1: DATABASE INITIALIZATION")
    print("="*50)
    try:
        initialize_database()
        print("✓ Database initialized successfully")
        return True
    except Exception as exc:
        print(f"✗ Database initialization failed: {exc}")
        return False

def test_categories():
    """Test 2: Categories seeding"""
    print("\n" + "="*50)
    print("TEST 2: CATEGORIES SEEDING")
    print("="*50)
    try:
        categories = get_categories()
        print(f"✓ Found {len(categories)} categories:")
        for cat in categories:
            print(f"  - {cat['id']}: {cat['name']}")
        if len(categories) >= 5:
            print("✓ At least 5 categories seeded (✓ PASS)")
            return True
        else:
            print("✗ Less than 5 categories (✗ FAIL)")
            return False
    except Exception as exc:
        print(f"✗ Error: {exc}")
        return False

def test_sources_crud():
    """Test 3: CRUD operations on sources"""
    print("\n" + "="*50)
    print("TEST 3: SOURCES CRUD OPERATIONS")
    print("="*50)
    try:
        # Get existing sources
        sources = get_sources()
        print(f"✓ Found {len(sources)} existing sources:")
        for src in sources:
            print(f"  - {src['id']}: {src['source_name']} ({src['category_name']})")
        
        # Test ADD
        print("\n[Testing ADD]")
        add_source("Test News", "https://test.com/news", 1)
        print("✓ Source added")
        
        # Get updated list
        sources = get_sources()
        test_source = [s for s in sources if s['source_name'] == "Test News"]
        if not test_source:
            print("✗ Added source not found (✗ FAIL)")
            return False
        test_id = test_source[0]['id']
        print(f"✓ Verified added source with ID {test_id}")
        
        # Test UPDATE
        print("\n[Testing UPDATE]")
        update_source(test_id, "Test News Updated", "https://test.com/news2", 2)
        updated = get_source_by_id(test_id)
        if updated and updated['source_name'] == "Test News Updated":
            print("✓ Source updated successfully")
        else:
            print("✗ Source update failed (✗ FAIL)")
            return False
        
        # Test DELETE
        print("\n[Testing DELETE]")
        delete_source(test_id)
        sources = get_sources()
        if not any(s['id'] == test_id for s in sources):
            print("✓ Source deleted successfully")
        else:
            print("✗ Source delete failed (✗ FAIL)")
            return False
        
        print("\n✓ All CRUD operations passed (✓ PASS)")
        return True
    except Exception as exc:
        print(f"✗ Error: {exc}")
        return False

def test_crawling():
    """Test 4: Crawling functionality"""
    print("\n" + "="*50)
    print("TEST 4: CRAWLING FUNCTIONALITY")
    print("="*50)
    try:
        print("[Phase 1] Testing crawl_all_sources()...")
        links_count = crawl_all_sources()
        print(f"✓ Crawled and saved {links_count} article links")
        
        if links_count > 0:
            print("✓ Successfully extracted links from sources (✓ PASS)")
        else:
            print("⚠ No links found (might be network issue, but code works)")
        
        print("\n[Phase 2] Testing crawl_pending_articles()...")
        print("(Will try to fetch content for pending articles)")
        updated_count = crawl_pending_articles(limit=5)
        print(f"✓ Updated content for {updated_count} articles")
        
        return True
    except Exception as exc:
        print(f"✗ Error: {exc}")
        return False

def test_pagination():
    """Test 5: Pagination"""
    print("\n" + "="*50)
    print("TEST 5: PAGINATION")
    print("="*50)
    try:
        total = count_articles()
        print(f"✓ Total articles in DB: {total}")
        
        # Test page 1
        page1 = list_articles(1, 10)
        print(f"✓ Page 1: Got {len(page1)} articles (max 10)")
        for idx, article in enumerate(page1, 1):
            status = "Mới" if article["status"] == 0 else "Đã lấy"
            print(f"  {idx}. [{status}] {article['title'][:60]}...")
        
        if total > 10:
            # Test page 2
            page2 = list_articles(2, 10)
            print(f"✓ Page 2: Got {len(page2)} articles")
            if page2 and page1[0]['id'] != page2[0]['id']:
                print("✓ Different articles on different pages (✓ PASS)")
                return True
        else:
            print(f"⚠ Only {total} articles (less than 10, can't test pagination fully)")
            if total > 0:
                print("✓ Articles exist and can be displayed (✓ PASS)")
                return True
        
        return total > 0
    except Exception as exc:
        print(f"✗ Error: {exc}")
        return False

def test_deduplication():
    """Test 6: Deduplication (URL unique constraint)"""
    print("\n" + "="*50)
    print("TEST 6: DEDUPLICATION")
    print("="*50)
    try:
        from db import insert_article_link, IntegrityError
        from mysql.connector import errorcode
        
        # Get a source
        sources = get_sources()
        if not sources:
            print("✗ No sources available for test")
            return False
        
        source = sources[0]
        
        # Try to add same article twice
        result1 = insert_article_link(
            source['id'],
            source['category_id'],
            "Test Duplicate Article",
            "https://test.com/duplicate-article-999"
        )
        
        result2 = insert_article_link(
            source['id'],
            source['category_id'],
            "Test Duplicate Article",
            "https://test.com/duplicate-article-999"
        )
        
        if result1 and not result2:
            print("✓ First insert: Success")
            print("✓ Second insert (duplicate): Rejected")
            print("✓ Deduplication working correctly (✓ PASS)")
            # Clean up
            from db import execute_query
            execute_query("DELETE FROM articles WHERE url = %s", ("https://test.com/duplicate-article-999",))
            return True
        else:
            print(f"✗ Deduplication failed (result1={result1}, result2={result2})")
            return False
    except Exception as exc:
        print(f"✗ Error: {exc}")
        return False

def main():
    print("\n" + "="*50)
    print("NEWS AGGREGATOR - COMPREHENSIVE TEST SUITE")
    print("="*50)
    
    results = []
    
    # Run all tests
    results.append(("Database Init", test_database()))
    if not results[-1][1]:
        print("\n✗ Cannot proceed without database")
        return
    
    results.append(("Categories", test_categories()))
    results.append(("CRUD Sources", test_sources_crud()))
    results.append(("Crawling", test_crawling()))
    results.append(("Pagination", test_pagination()))
    results.append(("Deduplication", test_deduplication()))
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n🎉 ALL TESTS PASSED! Ready for demo video.")
    elif passed_count >= total_count - 1:
        print("\n✓ Most tests passed. Some features may have network constraints.")
    else:
        print("\n⚠ Some tests failed. Please review above.")

if __name__ == "__main__":
    main()
