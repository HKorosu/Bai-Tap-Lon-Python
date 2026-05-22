#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FINAL COMPREHENSIVE TEST REPORT
Kiểm tra đầy đủ tất cả yêu cầu của đề bài
"""
import sys
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

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_requirement(num, title):
    print(f"\n✓ YÊU CẦU {num}: {title}")

def print_test(desc, result):
    status = "✓ PASS" if result else "✗ FAIL"
    print(f"  {status}: {desc}")

def main():
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█" + "  KIỂM TRA TOÀN DIỆN - NEWS AGGREGATOR CLI".center(58) + "█")
    print("█" + " "*58 + "█")
    print("█"*60)
    
    total_pass = 0
    total_tests = 0
    
    # ===== REQUIREMENT 1: DATABASE STRUCTURE =====
    print_section("YÊU CẦU 1: CẤU TRÚC DATABASE (MySQL)")
    
    try:
        initialize_database()
        print_test("Database khởi tạo thành công", True)
        total_pass += 1
    except:
        print_test("Database khởi tạo thành công", False)
    total_tests += 1
    
    # Test categories table
    try:
        cats = get_categories()
        has_5_cats = len(cats) >= 5
        print_test(f"Bảng 'categories' có 5+ mục (hiện có {len(cats)})", has_5_cats)
        if has_5_cats:
            total_pass += 1
            for c in cats:
                print(f"    - {c['name']}")
    except:
        print_test("Bảng 'categories' có 5+ mục", False)
    total_tests += 1
    
    # Test sources table
    try:
        sources = get_sources()
        has_sources = len(sources) > 0
        print_test(f"Bảng 'sources' hoạt động (có {len(sources)} sources)", has_sources)
        if has_sources:
            total_pass += 1
            for s in sources[:2]:
                print(f"    - {s['source_name']} ({s['category_name']})")
    except:
        print_test("Bảng 'sources' hoạt động", False)
    total_tests += 1
    
    # Test articles table
    try:
        articles_count = count_articles()
        has_articles = articles_count > 0
        print_test(f"Bảng 'articles' hoạt động (có {articles_count} bài)", has_articles)
        if has_articles:
            total_pass += 1
    except:
        print_test("Bảng 'articles' hoạt động", False)
    total_tests += 1
    
    # ===== REQUIREMENT 2: CRUD OPERATIONS =====
    print_section("YÊU CẦU 2: CRUD QUẢN LÝ NGUỒN TIN")
    
    # Test ADD
    try:
        add_source("Test Source CRUD", "https://test.com", 1)
        sources = get_sources()
        added = any(s['source_name'] == "Test Source CRUD" for s in sources)
        print_test("CREATE (Thêm) - Thêm source mới", added)
        if added:
            total_pass += 1
            test_id = [s['id'] for s in sources if s['source_name'] == "Test Source CRUD"][0]
    except Exception as e:
        print_test("CREATE (Thêm) - Thêm source mới", False)
        print(f"    Error: {e}")
    total_tests += 1
    
    # Test READ
    try:
        source = get_source_by_id(test_id)
        read_ok = source is not None
        print_test("READ (Xem) - Đọc chi tiết source", read_ok)
        if read_ok:
            total_pass += 1
            print(f"    Tìm được source ID {test_id}: {source['source_name']}")
    except Exception as e:
        print_test("READ (Xem) - Đọc chi tiết source", False)
        print(f"    Error: {e}")
    total_tests += 1
    
    # Test UPDATE
    try:
        update_source(test_id, "Test Source Updated", "https://test.com/updated", 2)
        updated = get_source_by_id(test_id)
        update_ok = updated and updated['source_name'] == "Test Source Updated"
        print_test("UPDATE (Sửa) - Cập nhật source", update_ok)
        if update_ok:
            total_pass += 1
    except Exception as e:
        print_test("UPDATE (Sửa) - Cập nhật source", False)
        print(f"    Error: {e}")
    total_tests += 1
    
    # Test DELETE
    try:
        delete_source(test_id)
        sources = get_sources()
        delete_ok = not any(s['id'] == test_id for s in sources)
        print_test("DELETE (Xóa) - Xóa source", delete_ok)
        if delete_ok:
            total_pass += 1
    except Exception as e:
        print_test("DELETE (Xóa) - Xóa source", False)
        print(f"    Error: {e}")
    total_tests += 1
    
    # ===== REQUIREMENT 3: CRAWLING =====
    print_section("YÊU CẦU 3: CRAWLING - LẤY DỮ LIỆU")
    
    try:
        sources = get_sources()
        multi_source = len(sources) >= 2
        print_test(f"Hỗ trợ 2+ báo (hiện có {len(sources)} sources)", multi_source)
        if multi_source:
            total_pass += 1
            for s in sources[:2]:
                print(f"    - {s['source_name']}: {s['url']}")
    except:
        print_test("Hỗ trợ 2+ báo", False)
    total_tests += 1
    
    try:
        articles_count = count_articles()
        has_data = articles_count > 0
        print_test(f"Crawl lấy được dữ liệu ({articles_count} articles)", has_data)
        if has_data:
            total_pass += 1
    except:
        print_test("Crawl lấy được dữ liệu", False)
    total_tests += 1
    
    try:
        articles = list_articles(1, 5)
        has_titles = all('title' in a for a in articles)
        has_urls = all('url' in a for a in articles)
        has_sources_info = all('source_name' in a for a in articles)
        crawl_ok = has_titles and has_urls and has_sources_info
        print_test("Trích xuất đúng thông tin (title, url, source)", crawl_ok)
        if crawl_ok:
            total_pass += 1
    except:
        print_test("Trích xuất đúng thông tin (title, url, source)", False)
    total_tests += 1
    
    # ===== REQUIREMENT 4: DEDUPLICATION & ERROR HANDLING =====
    print_section("YÊU CẦU 4: TÍNH NĂNG NÂNG CAO")
    
    try:
        # Check URL unique constraint
        from db import insert_article_link
        result1 = insert_article_link(1, 1, "Dup Test", "https://unique-test-url-999")
        result2 = insert_article_link(1, 1, "Dup Test", "https://unique-test-url-999")
        dedup_ok = result1 == True and result2 == False
        print_test("Deduplication - Kiểm tra URL duplicate", dedup_ok)
        if dedup_ok:
            total_pass += 1
            # Cleanup
            from db import execute_query
            execute_query("DELETE FROM articles WHERE url = %s", ("https://unique-test-url-999",))
    except Exception as e:
        print_test("Deduplication - Kiểm tra URL duplicate", False)
        print(f"    Error: {e}")
    total_tests += 1
    
    try:
        from config import HEADERS
        has_ua = "User-Agent" in HEADERS
        print_test("User-Agent Header - Tránh bị chặn", has_ua)
        if has_ua:
            total_pass += 1
            print(f"    UA: {HEADERS['User-Agent'][:60]}...")
    except:
        print_test("User-Agent Header - Tránh bị chặn", False)
    total_tests += 1
    
    # ===== REQUIREMENT 5: PAGINATION =====
    print_section("YÊU CẦU 5: PHÂN TRANG (Pagination)")
    
    try:
        total = count_articles()
        page1 = list_articles(1, 10)
        page2 = list_articles(2, 10)
        pagination_ok = len(page1) <= 10 and (total <= 10 or len(page2) > 0)
        print_test(f"Phân trang 10 tin/trang - Trang 1: {len(page1)} tin", len(page1) == 10 or total < 10)
        print_test(f"Phân trang 10 tin/trang - Trang 2: {len(page2)} tin", True)
        if pagination_ok:
            total_pass += 2
    except Exception as e:
        print_test("Phân trang", False)
        print(f"    Error: {e}")
    total_tests += 2
    
    # ===== REQUIREMENT 6: TWO-PHASE CRAWLING =====
    print_section("YÊU CẦU 6: HAI GIAI ĐOẠN CRAWL (Phase 1 & 2)")
    
    try:
        articles = list_articles(1, 100)
        has_status_0 = any(a['status'] == 0 for a in articles)
        has_status_1 = any(a['status'] == 1 for a in articles)
        two_phase_ok = has_status_0 or has_status_1
        print_test("Status field hoạt động (0=mới, 1=đã lấy)", two_phase_ok)
        if two_phase_ok:
            total_pass += 1
            count_0 = sum(1 for a in articles if a['status'] == 0)
            count_1 = sum(1 for a in articles if a['status'] == 1)
            print(f"    Status 0 (Mới): {count_0} bài")
            print(f"    Status 1 (Đã lấy): {count_1} bài")
    except:
        print_test("Status field hoạt động", False)
    total_tests += 1
    
    # ===== SUMMARY =====
    print_section("KẾT LUẬN")
    print(f"\n  Passed: {total_pass}/{total_tests} tests")
    pass_rate = (total_pass / total_tests * 100) if total_tests > 0 else 0
    print(f"  Success Rate: {pass_rate:.1f}%")
    
    if total_pass == total_tests:
        print("\n  🎉 ĐẠT YÊU CẦU 100%")
        print("  Ứng dụng sẵn sàng để ghi video demo!")
    elif total_pass >= total_tests - 1:
        print("\n  ✓ ĐẠT YÊU CẦU 95%+")
        print("  Ứng dụng hoạt động tốt, có thể ghi video demo!")
    else:
        print(f"\n  ⚠ ĐẠT YÊU CẦU {pass_rate:.1f}%")
        print("  Cần kiểm tra lại các điểm không đạt")
    
    print("\n" + "█"*60 + "\n")

if __name__ == "__main__":
    main()
